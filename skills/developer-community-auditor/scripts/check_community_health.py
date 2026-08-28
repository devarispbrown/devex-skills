#!/usr/bin/env python3
"""Compute the Community Health Score and named gate checks from a community-health JSON input. Stdlib only."""

import argparse
import json
import sys
from pathlib import Path

CONSTANTS = {
    # Canonical community thresholds (dx-standards/community.md; generated into references/standards.md).
    "COMMUNITY_ONBOARDING_PATH_MAX_MIN": 30,
    "COMMUNITY_ISSUE_RESPONSE_P50_H": 24,
    "COMMUNITY_ISSUE_RESPONSE_P90_H": 72,
    "COMMUNITY_FIRST_PR_REVIEW_P50_H": 24,
    "COMMUNITY_FIRST_PR_REVIEW_P90_H": 72,
    "COMMUNITY_USEFUL_ANSWER_P90_H": 48,
    "COMMUNITY_UNACKNOWLEDGED_PR_MAX_DAYS": 7,
    "CHS_HEALTHY_MIN": 85,
    "CHS_DEVELOPING_MIN": 70,
    # Scoring calibration (see references/health-score.md).
    "FUNNEL_HEALTH_WEIGHT": 15,
    "RESPONSIVENESS_WEIGHT": 15,
    "STANDARDS_PRESENCE_WEIGHT": 10,
    "CONTRIBUTION_OPPORTUNITIES_WEIGHT": 10,
    "GOVERNANCE_LADDER_WEIGHT": 10,
    "REVIEW_EXPERIENCE_WEIGHT": 10,
    "CONTRIBUTOR_RETENTION_WEIGHT": 10,
    "MAINTAINER_SUSTAINABILITY_WEIGHT": 10,
    "QA_SUPPORT_WEIGHT": 5,
    "RECOGNITION_AUTOMATION_WEIGHT": 5,
    "FUNNEL_ACTIVATION_W": 0.35,
    "FUNNEL_ACCEPTANCE_W": 0.35,
    "FUNNEL_RETURN_W": 0.30,
    "CLOSURE_RATIO_TARGET": 0.7,
    "RETENTION_TARGET": 0.5,
    "NEW_CONTRIBUTOR_SHARE_TARGET": 0.5,
    "STALE_PENALTY": 0.5,
    "QUEUED_PENALTY": 0.7,
    "SLO_DEGRADE_SLOPE": 50.0,
    "BUS_FACTOR_MIN": 2,
    "MAINTAINER_COUNT_TARGET": 3,
}

STAGES = {"founder-led": 0, "early": 1, "growing": 2, "scale": 3, "foundation": 4}
FILES = ["license", "contributing", "code_of_conduct", "security", "support", "governance", "maintainers", "ladder"]

DIMENSIONS = [
    ("funnel_health", "FUNNEL_HEALTH_WEIGHT"),
    ("responsiveness", "RESPONSIVENESS_WEIGHT"),
    ("standards_presence", "STANDARDS_PRESENCE_WEIGHT"),
    ("contribution_opportunities", "CONTRIBUTION_OPPORTUNITIES_WEIGHT"),
    ("governance_and_ladder", "GOVERNANCE_LADDER_WEIGHT"),
    ("review_experience", "REVIEW_EXPERIENCE_WEIGHT"),
    ("contributor_retention", "CONTRIBUTOR_RETENTION_WEIGHT"),
    ("maintainer_sustainability", "MAINTAINER_SUSTAINABILITY_WEIGHT"),
    ("qa_support", "QA_SUPPORT_WEIGHT"),
    ("recognition_and_automation", "RECOGNITION_AUTOMATION_WEIGHT"),
]

FORCE_FAIL = {"NO_CONTRIBUTING_WHILE_WELCOMING", "NO_CODE_OF_CONDUCT", "BROKEN_CONTRIBUTION_PATH", "DEAD_END_COMMUNITY"}

REASONS = {
    "NO_CONTRIBUTING_WHILE_WELCOMING": "contributions claimed welcome with no CONTRIBUTING.md",
    "NO_CODE_OF_CONDUCT": "stage >=1 without a Code of Conduct",
    "UNRESPONSIVE_ISSUES": "issue first-response P50 exceeds the SLO constant",
    "UNREVIEWED_FIRST_PR": "first-time-PR first-review P50 exceeds the SLO constant",
    "BROKEN_CONTRIBUTION_PATH": "Community Magic Path exceeds the onboarding limit",
    "DEAD_END_COMMUNITY": "non-maintainer PRs submitted but none merged",
    "OPAQUE_GOVERNANCE": "stage >=2 without governance and ladder, or aspirational governance",
    "STALE_GOOD_FIRST_ISSUES": "stale good-first issues or queued newcomer PRs unreviewed",
    "NO_GOOD_FIRST_ISSUES": "stage >=2 with no usable newcomer tasks",
    "NO_RECOGNITION_PATH": "stage >=2 with no contributor recognition",
    "UNACKNOWLEDGED_PRS": "a first-time-contributor PR has gone unacknowledged beyond the max-days constant",
    "NO_LICENSE": "no open-source LICENSE file present",
}


def num(d, key, default=0.0):
    v = d.get(key)
    return default if v is None else float(v)


def denom(a, b):
    return a / b if b and b > 0 else 0.0


def clamp(x, lo=0.0, hi=1.0):
    return max(lo, min(hi, x))


def stage_index(d):
    s = d.get("stage")
    if isinstance(s, int):
        return max(0, min(4, s))
    if isinstance(s, str):
        return STAGES.get(s.lower().strip(), 0)
    return 0


def slo_score(value, limit, slope):
    """Score 100 at the SLO limit, degrading linearly toward 0 above it. Returns (score, measured)."""
    if value is None or not limit:
        return 0.0, False
    ratio = value / limit
    if ratio <= 1.0:
        return 100.0, True
    return max(0.0, 100.0 - slope * (ratio - 1.0)), True


def score_funnel(d, c):
    f = d.get("funnel", {})
    participants = num(f, "participants")
    first_prs = num(f, "first_prs")
    merged = num(f, "merged")
    second = num(f, "second_contributions")
    if participants <= 0 or first_prs <= 0 or merged <= 0:
        return 0.0, False
    activation = clamp(denom(first_prs, participants))
    acceptance = clamp(denom(merged, first_prs))
    ret = clamp(denom(second, merged))
    score = 100.0 * (
        c["FUNNEL_ACTIVATION_W"] * activation
        + c["FUNNEL_ACCEPTANCE_W"] * acceptance
        + c["FUNNEL_RETURN_W"] * ret
    )
    return score, True


def score_responsiveness(d, c):
    r = d.get("responsiveness", {})
    if num(r, "non_bot_activity_30d") <= 0:
        return 0.0, False
    subs = [
        slo_score(r.get("issue_first_response_p50_h"), c["COMMUNITY_ISSUE_RESPONSE_P50_H"], c["SLO_DEGRADE_SLOPE"]),
        slo_score(r.get("first_pr_review_p50_h"), c["COMMUNITY_FIRST_PR_REVIEW_P50_H"], c["SLO_DEGRADE_SLOPE"]),
        slo_score(r.get("useful_answer_p90_h"), c["COMMUNITY_USEFUL_ANSWER_P90_H"], c["SLO_DEGRADE_SLOPE"]),
    ]
    measured = [s for s, ok in subs if ok]
    if not measured:
        return 0.0, False
    return sum(measured) / len(measured), True


def score_standards(d, c):
    f = d.get("files", {})
    total = 0.0
    for name in FILES:
        if f.get(name):
            q = f.get(name + "_quality")
            total += q if q is not None else 1.0
    return 100.0 * total / len(FILES), True


def score_opportunities(d, c):
    i = d.get("issues", {})
    open_count = num(i, "good_first_issues_open")
    if open_count <= 0:
        return 0.0, True
    base = 100.0 * clamp(denom(num(i, "usable_good_first_issues"), open_count))
    if num(i, "stale_good_first_issues") > 0:
        base *= c["STALE_PENALTY"]
    if num(i, "queued_newcomer_prs_unreviewed") > 0:
        base *= c["QUEUED_PENALTY"]
    return base, True


def score_governance(d, c):
    f = d.get("files", {})
    gov = f.get("governance_quality")
    gov = gov if gov is not None else (1.0 if f.get("governance") else 0.0)
    ladder = f.get("ladder_quality")
    ladder = ladder if ladder is not None else (1.0 if f.get("ladder") else 0.0)
    return 50.0 * gov + 50.0 * ladder, True


def score_review(d, c):
    a = d.get("activity", {})
    r = d.get("responsiveness", {})
    submitted = num(a, "non_maintainer_prs_submitted_90d")
    merged = num(a, "non_maintainer_prs_merged_90d")
    if submitted <= 0:
        closure, closure_ok = 0.0, False
    else:
        closure = 100.0 * clamp(denom(merged, submitted) / c["CLOSURE_RATIO_TARGET"])
        closure_ok = True
    speed, speed_ok = slo_score(r.get("first_pr_review_p50_h"), c["COMMUNITY_FIRST_PR_REVIEW_P50_H"], c["SLO_DEGRADE_SLOPE"])
    if not (closure_ok or speed_ok):
        return 0.0, False
    return 0.5 * closure + 0.5 * speed, True


def score_retention(d, c):
    a = d.get("activity", {})
    prior = num(a, "contributors_prior_90d")
    returning = num(a, "returning_contributors_90d")
    unique = num(a, "unique_contributors_90d")
    new = num(a, "new_contributors_90d")
    if prior <= 0:
        ret, ret_ok = 0.0, False
    else:
        ret = 100.0 * clamp(denom(returning, prior) / c["RETENTION_TARGET"])
        ret_ok = True
    if unique <= 0:
        new_share, new_ok = 0.0, False
    else:
        new_share = 100.0 * clamp(denom(new, unique) / c["NEW_CONTRIBUTOR_SHARE_TARGET"])
        new_ok = True
    if not (ret_ok or new_ok):
        return 0.0, False
    return 0.6 * ret + 0.4 * new_share, True


def score_sustainability(d, c):
    a = d.get("activity", {})
    bf = num(a, "bus_factor")
    bus = 100.0 if bf >= c["BUS_FACTOR_MIN"] else 50.0 * bf
    maint = 100.0 * clamp(denom(num(a, "core_maintainers"), c["MAINTAINER_COUNT_TARGET"]))
    areas = num(a, "critical_areas")
    multi = num(a, "areas_with_multiple_owners")
    if areas <= 0:
        return 0.0, False
    coverage = 100.0 * clamp(denom(multi, areas))
    return 0.4 * bus + 0.3 * maint + 0.3 * coverage, True


def score_qa(d, c):
    a = d.get("activity", {})
    r = d.get("responsiveness", {})
    questions = num(a, "community_questions_30d")
    answers = num(a, "useful_answers_30d")
    if questions <= 0:
        rate, rate_ok = 0.0, False
    else:
        rate = 100.0 * clamp(denom(answers, questions))
        rate_ok = True
    speed, speed_ok = slo_score(r.get("useful_answer_p90_h"), c["COMMUNITY_USEFUL_ANSWER_P90_H"], c["SLO_DEGRADE_SLOPE"])
    if not (rate_ok or speed_ok):
        return 0.0, False
    share = r.get("community_answer_share")
    if share is not None:
        share_score = 100.0 * clamp(float(share))
        return 0.5 * rate + 0.3 * speed + 0.2 * share_score, True
    return 0.6 * rate + 0.4 * speed, True


def score_recognition(d, c):
    p = d.get("process", {})
    recognition = 100.0 if p.get("recognition_program") else 0.0
    present = sum(1 for key in ("issue_templates", "pr_templates") if p.get(key))
    automation = 100.0 if present == 2 else (50.0 if present == 1 else 0.0)
    return 0.5 * recognition + 0.5 * automation, True


SCORERS = {
    "funnel_health": score_funnel,
    "responsiveness": score_responsiveness,
    "standards_presence": score_standards,
    "contribution_opportunities": score_opportunities,
    "governance_and_ladder": score_governance,
    "review_experience": score_review,
    "contributor_retention": score_retention,
    "maintainer_sustainability": score_sustainability,
    "qa_support": score_qa,
    "recognition_and_automation": score_recognition,
}


def gate(name, severity, failed):
    return {"name": name, "severity": severity, "failed": failed, "force_fail": name in FORCE_FAIL}


def check_gates(d, c):
    files = d.get("files", {})
    issues = d.get("issues", {})
    activity = d.get("activity", {})
    r = d.get("responsiveness", {})
    journey = d.get("journey", {})
    process = d.get("process", {})
    stage = stage_index(d)
    welcomes = bool(d.get("welcomes_contributions", False))

    gov_q = files.get("governance_quality")
    gov_q = gov_q if gov_q is not None else (1.0 if files.get("governance") else 0.0)

    results = [
        gate("NO_CONTRIBUTING_WHILE_WELCOMING", "P1", welcomes and not files.get("contributing")),
        gate("NO_CODE_OF_CONDUCT", "P1", stage >= 1 and not files.get("code_of_conduct")),
        gate("UNRESPONSIVE_ISSUES", "P1", r.get("issue_first_response_p50_h") is not None and num(r, "issue_first_response_p50_h") > c["COMMUNITY_ISSUE_RESPONSE_P50_H"]),
        gate("UNREVIEWED_FIRST_PR", "P1", r.get("first_pr_review_p50_h") is not None and num(r, "first_pr_review_p50_h") > c["COMMUNITY_FIRST_PR_REVIEW_P50_H"]),
        gate("BROKEN_CONTRIBUTION_PATH", "P1", journey.get("contribution_path_minutes") is not None and num(journey, "contribution_path_minutes") > c["COMMUNITY_ONBOARDING_PATH_MAX_MIN"]),
        gate("DEAD_END_COMMUNITY", "P1", num(activity, "non_maintainer_prs_submitted_90d") > 0 and num(activity, "non_maintainer_prs_merged_90d") <= 0),
        gate("OPAQUE_GOVERNANCE", "P1", stage >= 2 and (not files.get("governance") or not files.get("ladder") or gov_q < 0.5)),
        gate("STALE_GOOD_FIRST_ISSUES", "P1", num(issues, "stale_good_first_issues") > 0 or num(issues, "queued_newcomer_prs_unreviewed") > 0),
        gate("NO_GOOD_FIRST_ISSUES", "P2", stage >= 2 and num(issues, "usable_good_first_issues") <= 0),
        gate("NO_RECOGNITION_PATH", "P2", stage >= 2 and not process.get("recognition_program")),
        gate("UNACKNOWLEDGED_PRS", "P1", r.get("unacknowledged_pr_max_days") is not None and num(r, "unacknowledged_pr_max_days") > c["COMMUNITY_UNACKNOWLEDGED_PR_MAX_DAYS"]),
        gate("NO_LICENSE", "P1", not files.get("license")),
    ]
    return results


def tier_for(chs, c):
    if chs >= c["CHS_HEALTHY_MIN"]:
        return "HEALTHY", c["CHS_HEALTHY_MIN"]
    if chs >= c["CHS_DEVELOPING_MIN"]:
        return "DEVELOPING", c["CHS_DEVELOPING_MIN"]
    return "AT RISK", None


def verdict_for(gates):
    failed = [g for g in gates if g["failed"]]
    if any(g["force_fail"] or g["severity"] == "P1" for g in failed):
        return "FAIL"
    if failed:
        return "PASS WITH DEBT"
    return "PASS"


def main():
    ap = argparse.ArgumentParser(
        description="Compute the Community Health Score and named community gate checks from a community-health JSON file."
    )
    ap.add_argument("input", help="path to the community-health JSON (see assets/community-health.example.json)")
    a = ap.parse_args()

    try:
        d = json.loads(Path(a.input).read_text())
    except (OSError, ValueError) as e:
        raise SystemExit(f'ERROR: cannot read {a.input}: {e}')
    if not isinstance(d, dict):
        raise SystemExit(f'ERROR: {a.input} must contain a JSON object')
    c = dict(CONSTANTS)
    c.update(d.get("constants", {}))

    labels = {k: v for k, v in d.get("evidence", {}).items()}
    scores = {}
    measured = {}
    for name, wkey in DIMENSIONS:
        s, ok = SCORERS[name](d, c)
        scores[name] = s
        measured[name] = ok

    chs = sum(c[wkey] * scores[name] for name, wkey in DIMENSIONS) / 100.0
    tier, tier_min = tier_for(chs, c)
    maintainers = d.get("maintainers", [])
    concentration = None
    if maintainers:
        shares = [max(clamp(float(m.get("review_share", 0) or 0)),
                      clamp(float(m.get("merge_share", 0) or 0)),
                      clamp(float(m.get("response_share", 0) or 0))) for m in maintainers]
        top = max(shares) if shares else 0.0
        concentration = top if top > 0 else None
    gates = check_gates(d, c)
    verdict = verdict_for(gates)
    failed_gates = [g for g in gates if g["failed"]]

    unverified = [name for name, _ in DIMENSIONS if not measured[name] or labels.get(name, "UNVERIFIED") == "UNVERIFIED"]

    print(f"Community Health Report - {d.get('repo', '<repo>')}")
    print(f"Stage: {d.get('stage', '?')}   Window: trailing 90d activity/funnel, trailing 30d responsiveness")
    print()
    print(f"{'Dimension':<28}{'Weight':>7}{'Score':>8}{'Contrib':>9}  Evidence")
    for name, wkey in DIMENSIONS:
        label = labels.get(name, "UNVERIFIED")
        if not measured[name]:
            label = "UNVERIFIED"
        print(f"{name:<28}{c[wkey]:>7}{scores[name]:>8.1f}{c[wkey] * scores[name] / 100.0:>9.1f}  {label}")
    print()
    tier_suffix = f" (>= {tier_min})" if tier_min is not None else ""
    print(f"Community Health Score: {chs:.1f}  Tier: {tier}{tier_suffix}")
    if concentration is not None:
        print(f"Maintainer Concentration Index: {concentration:.2f} (max single-maintainer share across review/merge/response)")
    else:
        print("Maintainer Concentration Index: not reported (no maintainers input)")
    if unverified:
        print(f"UNVERIFIED dimensions: {', '.join(unverified)}")
    print()
    print("Gates:")
    for g in gates:
        mark = " *" if g["force_fail"] else ""
        print(f"  {'FAIL' if g['failed'] else 'PASS':<5} {g['name']} ({g['severity']}){mark}")
    print()
    print(f"Verdict: {verdict}")
    for g in failed_gates:
        print(f"GATE FAILURE: {g['name']} ({g['severity']}) - {REASONS[g['name']]}")
    code = 1 if failed_gates else 0
    print(f"EXIT CODE: {code}")
    raise SystemExit(code)


if __name__ == "__main__":
    main()

# Responsiveness SLO Monitoring

## Measurement window

All responsiveness metrics are measured over the trailing 30 days ending at audit time. Do not use lifetime aggregates or rolling averages; they hide current behavior.

## Denominators

Count only human activity. Bots never count toward responsiveness, per `COMMUNITY_BOT_RESPONSE_EXCLUDED`. Remove bot actors by identity list and by behavior signature: template replies, auto-labels, auto-comments, no reviewable content. Report the non-bot event count used as the denominator.

## First human response

For new issues, the first response is the first human message, comment, or actionable reaction. Do not count:

- bot replies or auto-comments
- label-only or triage-only automation
- redirects without substance

Measure P50 and P90 in hours over the window's new issues and compare to `COMMUNITY_ISSUE_RESPONSE_P50_H` and `COMMUNITY_ISSUE_RESPONSE_P90_H`. An issue first-response P50 above the P50 constant triggers `UNRESPONSIVE_ISSUES`.

## First human review

For first-time-contributor PRs, the first review is the first human review action or comment from a non-author. Measure P50 and P90 and compare to `COMMUNITY_FIRST_PR_REVIEW_P50_H` and `COMMUNITY_FIRST_PR_REVIEW_P90_H`. A P50 above the P50 constant triggers `UNREVIEWED_FIRST_PR`.

## Useful answers

For community questions, determine the first useful answer per question. A useful answer addresses the asker's stated question: it answers or resolves it. It is not:

- an acknowledgment without substance
- a redirect that does not answer
- a bot reply
- a link dump with no explanation

Measure the P90 in hours and compare to `COMMUNITY_USEFUL_ANSWER_P90_H`. Questions with no useful answer at all are recorded separately and counted against the Q&A dimension.

## Detection procedure

1. Enumerate all issue, PR, and question events in the window.
2. Classify each actor as human or bot; exclude bots.
3. For each item, find the first qualifying human event per the definitions above.
4. Compute the percentiles in hours from open to that event.
5. Record item counts, actor counts, percentiles, and the evidence label.

Never substitute lifetime percentiles for the trailing window. Never let a bot reply stand as the first response. Never count a non-answer as a useful answer.

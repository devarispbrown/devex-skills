#!/usr/bin/env python3
"""Static inventory of observability instrumentation signals in a code tree. Stdlib only."""
import argparse
import os
import re
from pathlib import Path

TEXT_EXTS = {
    ".go", ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".rb",
    ".php", ".cs", ".rs", ".c", ".cc", ".cpp", ".h", ".hpp", ".scala", ".swift",
}
CONFIG_EXTS = {".yaml", ".yml", ".json", ".tf", ".toml"}
DEFAULT_EXCLUDES = (
    "node_modules", "vendor", "__pycache__", ".venv", "venv", "target",
    "dist", "build", ".terraform", ".idea",
)

SURFACE_PATTERNS = {
    "logs": [
        re.compile(
            r"\b(?:logger|log|logging|slog|logrus|zap|_logger|LOGGER)"
            r"\.(?:debug|info|warn|warning|error|fatal|exception|critical)\s*\("
        ),
        re.compile(r"\blog\.(?:Debug|Info|Warn|Error|Fatal|Printf|Println)\s*\("),
        re.compile(r"\bslog\.(?:Debug|Info|Warn|Error)\s*\("),
        re.compile(r"\bLog(?:Information|Error|Warning|Debug|Trace)\s*\("),
        re.compile(r"\bconsole\.(?:log|info|warn|error)\s*\("),
    ],
    "metrics": [
        re.compile(r"\bprometheus(?:\.|_)"),
        re.compile(r"\b(?:prometheus\.New|otel\.New)(?:Counter|Gauge|Histogram|Summary)"),
        re.compile(r"\b(?:Counter|Gauge|Histogram|Summary)\s*\(\s*(?:Name|name)"),
        re.compile(r"\bfrom prometheus_client import"),
        re.compile(r"\bstatsd|datadog|micrometer|dropwizard|newrelic"),
        re.compile(r"\bmeter\.(?:create_)?(?:counter|histogram|gauge)"),
        re.compile(r"\bMeterProvider|get_meter|create_counter"),
    ],
    "traces": [
        re.compile(r"\b(?:otel|opentelemetry|tracer|trace)\.(?:Tracer|Start|Span)"),
        re.compile(r"\btracer\.Start(?:Span)?\s*\("),
        re.compile(r"\b(?:start_as_current_span|with_span|withSpan|startSpan|begin_span)"),
        re.compile(r"\bspan\s*[:=]?\s*[^;\n]*\.(?:Start|Begin)"),
        re.compile(r"\bfrom opentelemetry import"),
        re.compile(r"\bTracerProvider|get_tracer"),
    ],
    "health": [
        re.compile(r"\b(?:healthz|readyz|livez)\b"),
        re.compile(r"\b/(?:health|ready|live|ping)\b"),
        re.compile(
            r"\b(?:HealthCheck|health_check|check_health|is_healthy|get_health|"
            r"healthHandler|healthEndpoint)"
        ),
        re.compile(r"actuator/health"),
        re.compile(r"grpc\.health"),
    ],
    "correlation": [
        re.compile(r"x-request-id", re.IGNORECASE),
        re.compile(r"correlation[-_ ]?id", re.IGNORECASE),
        re.compile(r"request[-_ ]?id", re.IGNORECASE),
        re.compile(r"\b(?:requestId|correlationId|reqId|requestID|correlationID)\b"),
        re.compile(r"traceparent|tracestate", re.IGNORECASE),
        re.compile(r"x-amzn-trace-id", re.IGNORECASE),
    ],
}

ALERT_NAME = re.compile(
    r"(?:alert|alerts|rule|rules|monitor|monitors|slo|prometheus|grafana)", re.IGNORECASE
)
ALERT_DECL = re.compile(r"(?m)^\s*(?:alert|rule_group)\s*:", re.IGNORECASE)
ALERT_GROUPS = re.compile(r"(?m)^\s*groups\s*:", re.IGNORECASE)
ALERT_RULES = re.compile(r"(?m)^\s*rules\s*:", re.IGNORECASE)
PRINT_CALL = re.compile(r"\bprint\s*\(")

HASH_COMMENT = re.compile(r"#[^\n]*")
SLASH_LINE_COMMENT = re.compile(r"//[^\n]*")
BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
HASH_LANGS = {".py", ".rb", ".sh", ".php", ".yaml", ".yml", ".toml"}
SLASH_LANGS = {
    ".go", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".cs", ".rs",
    ".c", ".cc", ".cpp", ".h", ".hpp", ".scala", ".swift",
}


def strip_comments(text, suffix):
    """Remove comments so prose never counts as instrumentation. Heuristic."""
    if suffix in HASH_LANGS:
        return HASH_COMMENT.sub("", text)
    if suffix in SLASH_LANGS:
        return BLOCK_COMMENT.sub("", SLASH_LINE_COMMENT.sub("", text))
    return text


def walk(root, skip):
    """Yield (dirpath, sorted filenames), pruning skipped and hidden directories."""
    for dirpath, dirnames, filenames in os.walk(root):
        keep = []
        for name in sorted(dirnames):
            if name in skip or name.startswith("."):
                continue
            keep.append(name)
        dirnames[:] = keep
        yield Path(dirpath), sorted(filenames)


def is_alert_config(path, text):
    """Heuristic: alert config by filename or by Prometheus/Grafana rule shape."""
    if path.suffix not in CONFIG_EXTS:
        return False
    if ALERT_NAME.search(path.name):
        return True
    if ALERT_DECL.search(text):
        return True
    return bool(ALERT_GROUPS.search(text) and ALERT_RULES.search(text))


def main():
    ap = argparse.ArgumentParser(
        description="Inventory observability instrumentation signals (logs, metrics, traces, "
                    "health, correlation, alerts) in a code tree. Informational; always exits 0."
    )
    ap.add_argument("path", nargs="?", default=".", help="tree to scan (default: .)")
    ap.add_argument("--exclude", default="", help="extra directory names to skip, comma-separated")
    ap.add_argument("--verbose", action="store_true", help="print per-file surface hits")
    args = ap.parse_args()

    root = Path(args.path)
    if not root.is_dir():
        raise SystemExit(f"error: not a directory: {root}")
    skip = set(DEFAULT_EXCLUDES) | {s.strip() for s in args.exclude.split(",") if s.strip()}

    per_file = {}   # relpath -> set of surfaces hit
    alert_files = []
    unstructured = []   # relpaths with bare print() calls
    scanned = configs = 0

    for dirpath, filenames in walk(root, skip):
        for name in filenames:
            path = dirpath / name
            rel = path.relative_to(root)
            if path.suffix in TEXT_EXTS:
                scanned += 1
                raw = path.read_text(errors="replace")
                text = strip_comments(raw, path.suffix)
                hits = {s for s, pats in SURFACE_PATTERNS.items()
                        if any(p.search(text) for p in pats)}
                per_file[rel] = hits
                if PRINT_CALL.search(text):
                    unstructured.append(rel)
            elif path.suffix in CONFIG_EXTS:
                configs += 1
                raw = path.read_text(errors="replace")
                text = strip_comments(raw, path.suffix)
                if is_alert_config(path, text):
                    alert_files.append(rel)

    print("Observability readiness inventory")
    print("=================================")
    print(f"Tree: {root.resolve()}")
    print(f"Files scanned: {scanned} source, {configs} config (hidden and excluded dirs pruned)")

    print()
    print("Coverage by surface")
    print("-------------------")
    for surface in ("logs", "metrics", "traces", "health", "correlation", "alerts"):
        files = alert_files if surface == "alerts" else sorted(
            rel for rel, hits in per_file.items() if surface in hits
        )
        status = "COVERED" if files else "GAP"
        listing = ", ".join(str(f) for f in files[:6])
        if len(files) > 6:
            listing += ", ..."
        detail = f": {listing}" if files else ""
        print(f"  {surface:11} {status:8} ({len(files)} file(s)){detail}")
        if args.verbose:
            for rel, hits in sorted(per_file.items()):
                if surface in hits:
                    print(f"      {rel}")

    gaps = []
    for surface in ("logs", "metrics", "traces", "health", "correlation"):
        if not any(surface in hits for hits in per_file.values()):
            gaps.append(f"{surface}: no {surface} instrumentation found in any scanned file")
    if not alert_files:
        gaps.append(
            "alerts: no alert rules, monitors, or alert config files found "
            "(look for *_rules.yml, *_alerts.yml, datadog monitors, grafana rules)"
        )
    for rel in sorted(per_file):
        hits = per_file[rel]
        if hits & {"logs", "traces", "health"} and "correlation" not in hits:
            gaps.append(f"correlation: {rel} emits logs/traces/health signals without a correlation ID")

    print()
    print("Gaps")
    print("----")
    if gaps:
        for gap in gaps:
            print(f"  - {gap}")
    else:
        print("  none")

    print()
    print("Notes")
    print("-----")
    if unstructured:
        for rel in unstructured:
            print(f"  - {rel}: unstructured logging via print(); no structured logger detected")
    else:
        print("  none")

    print()
    print("Result: INFORMATIONAL (exit 0). The scan is a signal, never a verdict; "
          "confirm every hit and gap in source before reporting.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()

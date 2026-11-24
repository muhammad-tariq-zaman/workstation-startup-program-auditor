"""Audit startup programs on workstations for risk.

Usage: python3 main.py startup.csv
CSV columns: workstation,program,publisher,impact,enabled.
Impact is high, medium or low; enabled is yes or no. Known
publishers are Microsoft, Google, Adobe, Intel, Realtek, Cisco,
Mozilla, Zoom, HP, Dell, Lenovo, Apple and TeamViewer. Verdicts:
- REVIEW: publisher is not a known publisher.
- SLOW BOOT: known publisher, high impact, enabled.
- DISABLED: not enabled at startup.
- OK: anything else.
REVIEW first, then SLOW BOOT, OK, DISABLED; within a verdict
by workstation, then program.
"""
import argparse, csv, sys

KNOWN_PUBLISHERS = {"Microsoft", "Google", "Adobe", "Intel", "Realtek",
                    "Cisco", "Mozilla", "Zoom", "HP", "Dell", "Lenovo",
                    "Apple", "TeamViewer"}
VERDICT_ORDER = {"REVIEW": 0, "SLOW BOOT": 1, "OK": 2, "DISABLED": 3}

def audit(rows):
    out = []
    for row in rows:
        workstation = row["workstation"].strip()
        program = row["program"].strip()
        publisher = row["publisher"].strip()
        impact = row["impact"].strip().lower()
        enabled = row["enabled"].strip().lower() == "yes"
        if publisher not in KNOWN_PUBLISHERS:
            verdict, detail = "REVIEW", "unknown publisher"
            if impact == "high":
                detail += ", high impact"
        elif not enabled:
            verdict, detail = "DISABLED", "not enabled at startup"
        elif impact == "high":
            verdict, detail = "SLOW BOOT", "high startup impact"
        else:
            verdict, detail = "OK", ""
        out.append((workstation, program, publisher, verdict, detail))
    return sorted(out, key=lambda r: (VERDICT_ORDER[r[3]], r[0], r[1]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        results = audit(list(csv.DictReader(f)))
    for workstation, program, publisher, verdict, detail in results:
        if detail:
            print(f"{workstation} {program} ({publisher}): {verdict} - {detail}")
        else:
            print(f"{workstation} {program} ({publisher}): {verdict}")
    counts = {v: sum(1 for *_, verdict, _ in results if verdict == v)
              for v in ("REVIEW", "SLOW BOOT", "OK", "DISABLED")}
    print(f"{counts['REVIEW']} to review, {counts['SLOW BOOT']} slowing boot, "
          f"{counts['OK']} ok, {counts['DISABLED']} disabled out of "
          f"{len(results)} program(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())

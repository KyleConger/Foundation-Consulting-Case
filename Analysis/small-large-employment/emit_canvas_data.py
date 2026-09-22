import json
from pathlib import Path

s = json.loads(Path("Analysis/small-large-employment/out/summary.json").read_text(encoding="utf-8"))
out = Path("Analysis/small-large-employment/out/canvas_snippets.txt")
lines = []
lines.append("STATE_ROWS = [")
for r in s["states"]["all_sorted_by_lt500_desc"]:
    name = r["geo_name"].replace("District of Columbia", "D.C.")
    lines.append(
        f'  ["{name}", "{r["share_lt500_pct_1dp"]}%", "{r["share_ge500_pct_1dp"]}%", '
        f'"{r["employment_total"]:,}", "{r["employment_lt500"]:,}"],'
    )
lines.append("]")
lines.append("METRO_HIGH = [")
for r in s["metros"]["highest_10"]:
    short = r["geo_name"].replace(" Metro Area", "")
    lines.append(
        f'  ["{short}", "{r["share_lt500_pct_1dp"]}%", "{r["employment_total"]:,}", '
        f'"{r["employment_lt500"]:,}"],'
    )
lines.append("]")
lines.append("METRO_LOW = [")
for r in s["metros"]["lowest_10"]:
    short = r["geo_name"].replace(" Metro Area", "")
    lines.append(
        f'  ["{short}", "{r["share_lt500_pct_1dp"]}%", "{r["employment_total"]:,}", '
        f'"{r["employment_lt500"]:,}"],'
    )
lines.append("]")
# extremes for bar chart
lines.append("EXTREME_CATS = " + repr(
    [r["geo_name"] for r in s["states"]["top5"]]
    + [r["geo_name"] for r in s["states"]["bottom5"]]
))
lines.append("EXTREME_SHARES = " + repr(
    [r["share_lt500_pct_1dp"] for r in s["states"]["top5"]]
    + [r["share_lt500_pct_1dp"] for r in s["states"]["bottom5"]]
))
out.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {out}")

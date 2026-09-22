import csv
import pathlib

p = pathlib.Path(r"c:\Users\Owner\Desktop\MAN6930 Case\Analysis\work-from-home\out\acs2024_wfh_by_state.csv")
rows = list(csv.DictReader(p.open(encoding="utf-8")))
states = [r for r in rows if r["geo_level"] == "state"]
print("n states", len(states))
print("TOP")
for r in states[:8]:
    print(
        f"{r['rank_desc']:>2} {r['geography']:<28} {float(r['wfh_rate_pct']):5.1f}  "
        f"workers={int(float(r['workers_16_plus'])):,}"
    )
print("BOTTOM")
for r in states[-8:]:
    print(
        f"{r['rank_desc']:>2} {r['geography']:<28} {float(r['wfh_rate_pct']):5.1f}  "
        f"workers={int(float(r['workers_16_plus'])):,}"
    )
for name in [
    "Colorado",
    "Texas",
    "North Carolina",
    "Florida",
    "California",
    "New York",
    "Massachusetts",
    "Washington",
]:
    m = next((r for r in states if r["geography"] == name), None)
    if m:
        print("FOCAL", name, f"{float(m['wfh_rate_pct']):.1f}")

# emit JS-ready arrays for canvas
chart = states[:5] + states[-5:]
print("CHART_CATS", [r["geography"].replace("District of Columbia", "D.C.") for r in chart])
print("CHART_VALS", [round(float(r["wfh_rate_pct"]), 1) for r in chart])

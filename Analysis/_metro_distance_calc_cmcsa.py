"""One-off: location-weighted miles from Comcast BEAD state centroids to nearest MSA >=250k."""
import math

# Representative rural points (lat, lon). USGS/Census geographic centers.
# Same coordinates as CHTR script for overlapping states so distances match.
STATES = {
    "FL": ("Florida", 28.6305, -82.4497, "state centroid"),
    "VA": ("Virginia", 37.5215, -78.8537, "state centroid"),
    "PA": ("Pennsylvania", 40.8781, -77.7996, "state centroid"),
    "AZ": ("Arizona", 34.2744, -111.6602, "state centroid"),
    "IL": ("Illinois", 40.0417, -89.1965, "state centroid"),
    "MS": ("Mississippi", 32.7364, -89.6678, "state centroid"),
    "LA": ("Louisiana", 31.0689, -91.9968, "state centroid"),
    "KY": ("Kentucky", 37.5347, -85.3021, "state centroid"),
    "AR": ("Arkansas", 34.8938, -92.4426, "state centroid"),
    "NM": ("New Mexico", 34.4071, -106.1126, "state centroid"),
    "MN": ("Minnesota", 46.2807, -94.3053, "state centroid"),
    "UT": ("Utah", 39.3055, -111.6703, "state centroid"),
    "MO": ("Missouri", 38.3566, -92.4580, "state centroid"),
    "CO": ("Colorado", 38.9972, -105.5478, "state centroid"),
    "OH": ("Ohio", 40.2862, -82.7937, "state centroid"),
    "NH": ("New Hampshire", 43.6805, -71.5714, "state centroid"),
    "NY": ("New York", 42.9538, -75.5268, "state centroid"),
    "ME": ("Maine", 45.3695, -69.2428, "state centroid"),
}

LOCS = {
    "FL": 35772,
    "VA": 24343,
    "PA": 20835,
    "AZ": 13495,
    "IL": 13023,
    "MS": 10809,
    "LA": 6561,
    "KY": 5777,
    "AR": 3242,
    "NM": 2760,
    "MN": 2760,
    "UT": 1787,
    "MO": 1357,
    "CO": 1047,
    "OH": 835,
    "NH": 573,
    "NY": 390,
    "ME": 71,
}

# Principal-city lat/lon + 2020 CBSA pop (filter >=250k). Same set as CHTR + Little Rock.
RAW_MSAS = [
    ("New York-Newark-Jersey City", 40.7128, -74.0060, 20140270),
    ("Los Angeles-Long Beach-Anaheim", 34.0522, -118.2437, 13214799),
    ("Chicago-Naperville-Elgin", 41.8781, -87.6298, 9618502),
    ("Dallas-Fort Worth-Arlington", 32.7767, -96.7970, 7638332),
    ("Houston-The Woodlands-Sugar Land", 29.7604, -95.3698, 7122240),
    ("Washington-Arlington-Alexandria", 38.9072, -77.0369, 6385162),
    ("Philadelphia-Camden-Wilmington", 39.9526, -75.1652, 6245051),
    ("Miami-Fort Lauderdale-Pompano Beach", 25.7617, -80.1918, 6138333),
    ("Atlanta-Sandy Springs-Alpharetta", 33.7490, -84.3880, 6089815),
    ("Boston-Cambridge-Newton", 42.3601, -71.0589, 4941632),
    ("Phoenix-Mesa-Chandler", 33.4484, -112.0740, 4845832),
    ("San Francisco-Oakland-Berkeley", 37.7749, -122.4194, 4749008),
    ("Riverside-San Bernardino-Ontario", 33.9806, -117.3755, 4599839),
    ("Detroit-Warren-Dearborn", 42.3314, -83.0458, 4392041),
    ("Seattle-Tacoma-Bellevue", 47.6062, -122.3321, 4018762),
    ("Minneapolis-St. Paul-Bloomington", 44.9778, -93.2650, 3693850),
    ("San Diego-Chula Vista-Carlsbad", 32.7157, -117.1611, 3298634),
    ("Tampa-St. Petersburg-Clearwater", 27.9506, -82.4572, 3175275),
    ("Denver-Aurora-Lakewood", 39.7392, -104.9903, 2963821),
    ("Baltimore-Columbia-Towson", 39.2904, -76.6122, 2844510),
    ("St. Louis", 38.6270, -90.1994, 2820253),
    ("Orlando-Kissimmee-Sanford", 28.5383, -81.3792, 2673376),
    ("Charlotte-Concord-Gastonia", 35.2271, -80.8431, 2660329),
    ("San Antonio-New Braunfels", 29.4241, -98.4936, 2558143),
    ("Portland-Vancouver-Hillsboro", 45.5152, -122.6784, 2512859),
    ("Sacramento-Roseville-Folsom", 38.5816, -121.4944, 2397382),
    ("Pittsburgh", 40.4406, -79.9959, 2370930),
    ("Austin-Round Rock-Georgetown", 30.2672, -97.7431, 2283371),
    ("Las Vegas-Henderson-Paradise", 36.1699, -115.1398, 2265461),
    ("Cincinnati", 39.1031, -84.5120, 2256884),
    ("Kansas City", 39.0997, -94.5786, 2192035),
    ("Columbus", 39.9612, -82.9988, 2138926),
    ("Indianapolis-Carmel-Anderson", 39.7684, -86.1581, 2111040),
    ("Cleveland-Elyria", 41.4993, -81.6944, 2080885),
    ("Nashville-Davidson--Murfreesboro--Franklin", 36.1627, -86.7816, 1989895),
    ("San Jose-Sunnyvale-Santa Clara", 37.3382, -121.8863, 2000468),
    ("Virginia Beach-Norfolk-Newport News", 36.8529, -75.9780, 1799682),
    ("Providence-Warwick", 41.8240, -71.4128, 1676769),
    ("Jacksonville", 30.3322, -81.6557, 1605848),
    ("Milwaukee-Waukesha", 43.0389, -87.9065, 1574731),
    ("Oklahoma City", 35.4676, -97.5164, 1425695),
    ("Raleigh-Cary", 35.7796, -78.6382, 1413982),
    ("Memphis", 35.1495, -90.0490, 1346037),
    ("Richmond", 37.5407, -77.4360, 1314434),
    ("Louisville/Jefferson County", 38.2527, -85.7585, 1285162),
    ("New Orleans-Metairie", 29.9511, -90.0715, 1270570),
    ("Salt Lake City", 40.7608, -111.8910, 1257873),
    ("Hartford-East Hartford-Middletown", 41.7658, -72.6734, 1213863),
    ("Buffalo-Cheektowaga", 42.8864, -78.8784, 1166902),
    ("Birmingham-Hoover", 33.5207, -86.8025, 1115189),
    ("Rochester", 43.1566, -77.6088, 1090135),
    ("Grand Rapids-Kentwood", 42.9634, -85.6681, 1087692),
    ("Tucson", 32.2226, -110.9747, 1043453),
    ("Fresno", 36.7378, -119.7871, 1008888),
    ("Tulsa", 36.1540, -95.9928, 1015186),
    ("Worcester", 42.2626, -71.8023, 978529),
    ("Bridgeport-Stamford-Norwalk", 41.1865, -73.1952, 957419),
    ("Albuquerque", 35.0844, -106.6504, 916528),
    ("Albany-Schenectady-Troy", 42.6526, -73.7562, 899262),
    ("Knoxville", 35.9606, -83.9207, 879275),
    ("Bakersfield", 35.3733, -119.0187, 909235),
    ("New Haven-Milford", 41.3083, -72.9279, 864835),
    ("McAllen-Edinburg-Mission", 26.2034, -98.2300, 870815),
    ("Oxnard-Thousand Oaks-Ventura", 34.1975, -119.1771, 843843),
    ("El Paso", 31.7619, -106.4850, 868859),
    ("Allentown-Bethlehem-Easton", 40.6084, -75.4902, 861889),
    ("Baton Rouge", 30.4515, -91.1871, 870569),
    ("Columbia", 34.0007, -81.0348, 829470),
    ("Dayton-Kettering", 39.7589, -84.1917, 814049),
    ("Charleston-North Charleston", 32.7765, -79.9311, 799155),
    ("Greensboro-High Point", 36.0726, -79.7920, 775602),
    ("Omaha-Council Bluffs", 41.2565, -95.9345, 967604),
    ("North Port-Sarasota-Bradenton", 27.3364, -82.5307, 833996),
    ("Stockton", 37.9577, -121.2908, 779233),
    ("Boise City", 43.6150, -116.2023, 764718),
    ("Colorado Springs", 38.8339, -104.8214, 755105),
    ("Cape Coral-Fort Myers", 26.6406, -81.8723, 760822),
    ("Lakeland-Winter Haven", 28.0395, -81.9498, 725046),
    ("Akron", 41.0814, -81.5190, 702442),
    ("Winston-Salem", 36.0999, -80.2442, 675966),
    ("Ogden-Clearfield", 41.2230, -111.9738, 694863),
    ("Madison", 43.0731, -89.4012, 680796),
    ("Durham-Chapel Hill", 35.9940, -78.8986, 649903),
    ("Syracuse", 43.0481, -76.1474, 662057),
    ("Wichita", 37.6872, -97.3301, 647610),
    ("Des Moines-West Des Moines", 41.5868, -93.6250, 709466),
    ("Toledo", 41.6528, -83.5379, 646604),
    ("Augusta-Richmond County", 33.4735, -82.0105, 611000),
    ("Palm Bay-Melbourne-Titusville", 28.0800, -80.6081, 606612),
    ("Harrisburg-Carlisle", 40.2732, -76.8867, 591048),
    ("Spokane-Spokane Valley", 47.6588, -117.4260, 585841),
    ("Provo-Orem", 40.2338, -111.6585, 671185),
    ("Jackson", 32.2988, -90.1848, 591978),
    ("Chattanooga", 35.0456, -85.3097, 562647),
    ("Scranton--Wilkes-Barre", 41.4090, -75.6624, 567559),
    ("Modesto", 37.6391, -120.9969, 552878),
    ("Deltona-Daytona Beach-Ormond Beach", 29.2108, -81.0228, 668971),
    ("Lancaster", 40.0379, -76.3055, 552984),
    ("Portland-South Portland", 43.6591, -70.2568, 551740),
    ("Youngstown-Warren-Boardman", 41.0998, -80.6495, 541320),
    ("Fayetteville-Springdale-Rogers", 36.0626, -94.1574, 546725),
    ("Lexington-Fayette", 38.0406, -84.5037, 516811),
    ("Springfield", 42.1015, -72.5898, 699162),
    ("Fort Wayne", 41.0793, -85.1394, 419453),
    ("Corpus Christi", 27.8006, -97.3964, 429024),
    ("Pensacola-Ferry Pass-Brent", 30.4213, -87.2169, 509525),
    ("Santa Rosa-Petaluma", 38.4404, -122.7141, 488863),
    ("Huntsville", 34.7304, -86.5861, 491723),
    ("Mobile", 30.6954, -88.0399, 430201),
    ("Asheville", 35.5951, -82.5515, 469015),
    ("Salinas", 36.6777, -121.6555, 439035),
    ("Killeen-Temple", 31.1171, -97.7278, 475367),
    ("Brownsville-Harlingen", 25.9017, -97.4975, 421666),
    ("Springfield MO", 37.2090, -93.2923, 475432),
    ("Beaumont-Port Arthur", 30.0802, -94.1266, 397562),
    ("Rockford", 42.2711, -89.0940, 338610),
    ("Davenport-Moline-Rock Island", 41.5236, -90.5776, 384324),
    ("Salem", 44.9429, -123.0351, 433380),
    ("Fayetteville", 35.0527, -78.8784, 520508),
    ("Visalia", 36.3302, -119.2921, 473117),
    ("York-Hanover", 39.9626, -76.7277, 456438),
    ("Reno", 39.5296, -119.8138, 490903),
    ("Santa Barbara", 34.4208, -119.6982, 448229),
    ("Huntington-Ashland", 38.4192, -82.4452, 359190),
    ("Fort Collins", 40.5853, -105.0844, 359066),
    ("Manchester-Nashua", 42.9956, -71.4548, 422613),
    ("Greenville-Anderson", 34.8526, -82.3940, 928195),
    ("Spartanburg", 34.9493, -81.9320, 327997),
    ("Myrtle Beach-Conway-North Myrtle Beach", 33.6891, -78.8867, 487185),
    ("Savannah", 32.0809, -81.0912, 404798),
    ("Tallahassee", 30.4383, -84.2807, 384298),
    ("Gainesville", 29.6516, -82.3248, 339247),
    ("Ocala", 29.1872, -82.1401, 375665),
    ("Green Bay", 44.5133, -88.0133, 328268),
    ("Duluth", 46.7867, -92.1005, 291638),
    ("Roanoke", 37.2710, -79.9414, 315251),
    ("Lynchburg", 37.4138, -79.1422, 261593),
    ("Shreveport-Bossier City", 32.5252, -93.7502, 393406),
    ("Lafayette", 30.2241, -92.0198, 478384),
    ("Lake Charles", 30.2266, -93.2174, 254652),
    ("Gulfport-Biloxi", 30.3674, -89.0928, 416259),
    ("Montgomery", 32.3792, -86.3077, 386047),
    ("Tuscaloosa", 33.2098, -87.5692, 268666),
    ("Evansville", 37.9716, -87.5711, 314788),
    ("South Bend-Mishawaka", 41.6764, -86.2520, 324501),
    ("Clarksville", 36.5298, -87.3595, 320367),
    ("Kingsport-Bristol", 36.5484, -82.5618, 307824),
    ("Eugene", 44.0521, -123.0868, 382959),
    ("Yakima", 46.6021, -120.5059, 256728),
    ("Kennewick-Richland", 46.2112, -119.1372, 303501),
    ("Olympia-Lacey-Tumwater", 47.0379, -122.9007, 294793),
    ("Bremerton-Silverdale", 47.5673, -122.6329, 275419),
    ("Merced", 37.3022, -120.4829, 281202),
    ("Santa Cruz-Watsonville", 36.9741, -122.0308, 270632),
    ("Vallejo-Fairfield", 38.1041, -122.2566, 453491),
    ("Trenton-Princeton", 40.2171, -74.7429, 387340),
    ("Atlantic City-Hammonton", 39.3643, -74.4229, 274534),
    ("Reading", 40.3356, -75.9269, 428849),
    ("Erie", 42.1292, -80.0851, 270876),
    ("Peoria", 40.6936, -89.5890, 402391),
    ("Flint", 43.0125, -83.6875, 406892),
    ("Kalamazoo-Portage", 42.2917, -85.5872, 261670),
    ("Lansing-East Lansing", 42.7325, -84.5555, 541297),
    ("Ann Arbor", 42.2808, -83.7430, 372258),
    ("Portsmouth", 43.0718, -70.7626, 259056),
    ("Little Rock-North Little Rock-Conway", 34.7465, -92.2896, 748031),
]


def haversine_mi(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


SHORT = {
    "New York-Newark-Jersey City": "New York",
    "Los Angeles-Long Beach-Anaheim": "Los Angeles",
    "Chicago-Naperville-Elgin": "Chicago",
    "Dallas-Fort Worth-Arlington": "Dallas-Fort Worth",
    "Houston-The Woodlands-Sugar Land": "Houston",
    "Washington-Arlington-Alexandria": "Washington DC",
    "Philadelphia-Camden-Wilmington": "Philadelphia",
    "Miami-Fort Lauderdale-Pompano Beach": "Miami",
    "Atlanta-Sandy Springs-Alpharetta": "Atlanta",
    "Boston-Cambridge-Newton": "Boston",
    "Phoenix-Mesa-Chandler": "Phoenix",
    "San Francisco-Oakland-Berkeley": "San Francisco",
    "Minneapolis-St. Paul-Bloomington": "Minneapolis",
    "Tampa-St. Petersburg-Clearwater": "Tampa",
    "Denver-Aurora-Lakewood": "Denver",
    "Orlando-Kissimmee-Sanford": "Orlando",
    "Portland-Vancouver-Hillsboro": "Portland OR",
    "Indianapolis-Carmel-Anderson": "Indianapolis",
    "Cleveland-Elyria": "Cleveland",
    "Nashville-Davidson--Murfreesboro--Franklin": "Nashville",
    "Virginia Beach-Norfolk-Newport News": "Virginia Beach",
    "Louisville/Jefferson County": "Louisville",
    "New Orleans-Metairie": "New Orleans",
    "Grand Rapids-Kentwood": "Grand Rapids",
    "Harrisburg-Carlisle": "Harrisburg",
    "Portland-South Portland": "Portland ME",
    "Fayetteville-Springdale-Rogers": "Fayetteville AR",
    "Springfield MO": "Springfield, MO",
    "Little Rock-North Little Rock-Conway": "Little Rock",
    "Albany-Schenectady-Troy": "Albany",
    "Buffalo-Cheektowaga": "Buffalo",
    "Scranton--Wilkes-Barre": "Scranton",
    "Gulfport-Biloxi": "Gulfport-Biloxi",
    "Shreveport-Bossier City": "Shreveport-Bossier City",
    "Durham-Chapel Hill": "Durham-Chapel Hill",
    "Manchester-Nashua": "Manchester-Nashua",
    "Ogden-Clearfield": "Ogden",
    "Provo-Orem": "Provo",
    "Colorado Springs": "Colorado Springs",
    "Fort Collins": "Fort Collins",
    "Salt Lake City": "Salt Lake City",
    "Duluth": "Duluth",
    "Rochester": "Rochester NY",
    "Syracuse": "Syracuse",
}


seen = set()
msas = []
for m in RAW_MSAS:
    if m[3] >= 250000 and m[0] not in seen:
        seen.add(m[0])
        msas.append(m)

rows = []
for ab, (name, lat, lon, point_note) in STATES.items():
    best_name, best_d, best_pop = None, 1e9, None
    for mname, mlat, mlon, pop in msas:
        d = haversine_mi(lat, lon, mlat, mlon)
        if d < best_d:
            best_name, best_d, best_pop = mname, d, pop
    short = SHORT.get(best_name, best_name.split("-")[0] if best_name else "?")
    # Prefer known short labels; for remainder use first city token
    if best_name in SHORT:
        short = SHORT[best_name]
    else:
        short = best_name.split(",")[0].split("-")[0].strip() if best_name else "?"
        # keep a few that CHTR style uses as-is
        if best_name in (
            "Ocala",
            "Peoria",
            "Albuquerque",
            "Lafayette",
            "Lynchburg",
            "Columbus",
            "Jackson",
            "Tucson",
            "Memphis",
            "St. Louis",
            "Kansas City",
            "Cincinnati",
            "Pittsburgh",
            "Richmond",
            "Green Bay",
            "Eugene",
            "Yakima",
            "Worcester",
            "Fresno",
            "Montgomery",
            "Baton Rouge",
        ):
            short = best_name
    rows.append(
        {
            "ab": ab,
            "name": name,
            "loc": LOCS[ab],
            "metro": short,
            "metro_full": best_name,
            "mi": round(best_d, 1),
            "metro_pop": best_pop,
            "point": point_note,
        }
    )

rows.sort(key=lambda r: -r["loc"])
total = sum(r["loc"] for r in rows)
wavg = sum(r["loc"] * r["mi"] for r in rows) / total

sorted_d = sorted(rows, key=lambda r: r["mi"])
cum = 0
wmed = None
for r in sorted_d:
    cum += r["loc"]
    if cum >= total / 2:
        wmed = r["mi"]
        break

bands = {"lt25": 0, "b25_50": 0, "b50_100": 0, "gte100": 0}
for r in rows:
    d = r["mi"]
    if d < 25:
        bands["lt25"] += r["loc"]
    elif d < 50:
        bands["b25_50"] += r["loc"]
    elif d < 100:
        bands["b50_100"] += r["loc"]
    else:
        bands["gte100"] += r["loc"]

print(f"MSA_COUNT={len(msas)}")
print(f"TOTAL_LOCS={total}")
print(f"WAVG={wavg:.1f}")
print(f"WMED={wmed}")
print(f"MIN={min(rows, key=lambda r: r['mi'])}")
print(f"MAX={max(rows, key=lambda r: r['mi'])}")
print("BANDS_PCT=" + str({k: round(100 * v / total, 1) for k, v in bands.items()}))
print("BANDS_LOC=" + str(bands))
print("TOP5_FAR")
for r in sorted(rows, key=lambda r: -r["mi"])[:5]:
    print(f"  {r['ab']} {r['mi']} mi -> {r['metro']} ({r['loc']} locs)")
print("SHARE_WITHIN_50=" + str(round(100 * (bands["lt25"] + bands["b25_50"]) / total, 1)))
print("SHARE_100PLUS=" + str(round(100 * bands["gte100"] / total, 1)))
print("---ROWS---")
for r in rows:
    print(f"{r['ab']}|{r['name']}|{r['loc']}|{r['metro']}|{r['mi']}|{r['point']}|{r['metro_full']}")

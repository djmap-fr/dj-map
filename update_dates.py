"""Met à jour events.json avec les vraies dates (API Ticketmaster Discovery).
Utilisation :  TICKETMASTER_KEY=ta_cle python3 update_dates.py
Aucune installation : uniquement la bibliothèque standard de Python."""
import json, os, sys, time, unicodedata, urllib.parse, urllib.request
from datetime import date

KEY = os.environ.get("TICKETMASTER_KEY")
API = "https://app.ticketmaster.com/discovery/v2/"
TODAY = date.today().isoformat()

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum())

def get(path, **params):
    params["apikey"] = KEY
    url = API + path + "?" + urllib.parse.urlencode(params)
    for essai in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(2 * (essai + 1))
    return {}

def main():
    if not KEY:
        sys.exit("Il manque la clé : TICKETMASTER_KEY=... python3 update_dates.py")
    djs = json.load(open("djs.json", encoding="utf-8"))
    manual = json.load(open("manual_events.json", encoding="utf-8"))   # dates saisies à la main
    venues = dict(manual["venues"])
    events = [e for e in manual["events"] if e["date"] >= TODAY]
    found = {}
    for name in djs:
        # 1) on retrouve l'artiste EXACT (nom identique) pour ne jamais mélanger deux DJ
        res = get("attractions.json", keyword=name, classificationName="music", size=10)
        atts = [a for a in res.get("_embedded", {}).get("attractions", []) if norm(a["name"]) == norm(name)]
        time.sleep(0.25)
        if not atts:
            continue
        # 2) ses dates à venir
        res = get("events.json", attractionId=atts[0]["id"], size=100, sort="date,asc",
                  startDateTime=TODAY + "T00:00:00Z")
        time.sleep(0.25)
        for ev in res.get("_embedded", {}).get("events", []):
            ven = (ev.get("_embedded", {}).get("venues") or [None])[0]
            d = ev.get("dates", {}).get("start", {}).get("localDate")
            loc = (ven or {}).get("location") or {}
            if not (ven and d and loc.get("latitude") and ev.get("url")):
                continue
            vid = "tm_" + ven["id"]
            venues[vid] = {"n": ven["name"], "city": ven.get("city", {}).get("name", ""),
                           "country": ven.get("country", {}).get("name", ""),
                           "lat": float(loc["latitude"]), "lon": float(loc["longitude"])}
            events.append({"dj": name, "venue": vid, "date": d, "ticketUrl": ev["url"]})
            found[name] = found.get(name, 0) + 1
    # on retire les doublons (même DJ, même jour)
    uniq = {}
    for e in events:
        uniq.setdefault((e["dj"], e["date"]), e)
    events = sorted(uniq.values(), key=lambda e: (e["date"], e["dj"]))
    used = {e["venue"] for e in events}
    out = {"updated": TODAY, "venues": {k: v for k, v in venues.items() if k in used}, "events": events}
    json.dump(out, open("events.json", "w", encoding="utf-8"), ensure_ascii=False)
    print(len(events), "dates,", len({e['dj'] for e in events}), "DJ ; Ticketmaster a trouvé des dates pour", len(found), "DJ")

main()

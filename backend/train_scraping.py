import sys
import json
import requests
from datetime import datetime


HAFAS_URL = "https://fahrplan.oebb.at/bin/mgate.exe"
HAFAS_PAYLOAD = {
    "client": {"id": "OEBB", "v": "6030600", "type": "IPH", "name": "oebb"},
    "ver": "1.57",
    "lang": "en",
    "auth": {"aid": "OWDL4fE4ixNiPBBm", "type": "AID"}
}


def search_journeys(from_city, to_city, date):
    """date format: YYYYMMDD"""
    payload = {
        **HAFAS_PAYLOAD,
        "svcReqL": [{
            "meth": "TripSearch",
            "req": {
                "depLocL": [{"name": from_city, "type": "S"}],
                "arrLocL": [{"name": to_city, "type": "S"}],
                "outDate": date,
                "outTime": "000000",
                "jnyFltrL": [{"type": "PROD", "mode": "INC", "value": "1023"}],
                "getPasslist": False,
                "getTariff": True,
                "numF": 10
            }
        }]
    }
    try:
        resp = requests.post(HAFAS_URL, json=payload, timeout=15,
                             headers={"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        svc = data.get("svcResL", [{}])[0]
        if svc.get("err") != "OK":
            return None
        return svc.get("res")
    except Exception:
        return None


def parse_journeys(res):
    common = res.get("common", {})
    locations = common.get("locL", [])
    products = common.get("prodL", [])
    results = []

    for trip in res.get("outConL", []):
        dep = trip.get("dep", {})
        arr = trip.get("arr", {})
        dep_time = dep.get("dTimeS", "")
        arr_time = arr.get("aTimeS", "")
        trip_date = trip.get("date", "")

        dep_loc = locations[dep.get("locX", 0)]["name"] if dep.get("locX", 0) < len(locations) else ""
        arr_loc = locations[arr.get("locX", 0)]["name"] if arr.get("locX", 0) < len(locations) else ""

        # Train names from journey sections
        trains = []
        for sec in trip.get("secL", []):
            if sec.get("type") == "JNY":
                prod_idx = sec.get("jny", {}).get("prodX", -1)
                if 0 <= prod_idx < len(products):
                    trains.append(products[prod_idx].get("name", ""))

        # Duration
        dur = trip.get("dur", "")
        duration_str = "N/A"
        if len(dur) >= 4:
            h = int(dur[:2]) if dur[:2].isdigit() else 0
            m = int(dur[2:4]) if dur[2:4].isdigit() else 0
            duration_str = f"{h}h {m}m" if h > 0 else f"{m}m"

        transfers = trip.get("chg", 0)

        # Build ISO datetime strings
        departure_iso = ""
        arrival_iso = ""
        if trip_date and dep_time:
            departure_iso = f"{trip_date[:4]}-{trip_date[4:6]}-{trip_date[6:8]}T{dep_time[:2]}:{dep_time[2:4]}:00"
        if trip_date and arr_time:
            arrival_iso = f"{trip_date[:4]}-{trip_date[4:6]}-{trip_date[6:8]}T{arr_time[:2]}:{arr_time[2:4]}:00"

        # Booking link from tariff response
        trf = trip.get("trfRes", {})
        link = trf.get("clickout", "")

        results.append({
            "origin": dep_loc,
            "destination": arr_loc,
            "departure": departure_iso,
            "arrival": arrival_iso,
            "duration": duration_str,
            "trains": trains,
            "transfers": transfers,
            "link": link
        })

    return results


def main():
    from_city = sys.argv[1]
    to_city = sys.argv[2]
    date = sys.argv[3]  # YYYY-MM-DD

    hafas_date = date.replace("-", "")
    res = search_journeys(from_city, to_city, hafas_date)

    if not res:
        print(json.dumps({"success": False, "error": "Train service temporarily unavailable. Please try again later."}))
        return

    trips = parse_journeys(res)

    print(json.dumps({
        "success": True if trips else False,
        "trips": trips,
        "error": None if trips else "No train routes found",
        "search_params": {"from": from_city, "to": to_city, "date": date}
    }))


if __name__ == "__main__":
    main()

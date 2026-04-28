import sys
import json
import requests
from datetime import datetime


FLIXBUS_API = "https://global.api.flixbus.com"


def find_city(city_name):
    try:
        resp = requests.get(f"{FLIXBUS_API}/search/autocomplete/cities",
                            params={"q": city_name, "lang": "en",
                                    "country": "de"}, timeout=10)
        resp.raise_for_status()
        results = resp.json()
        if results:
            return results[0]["id"], results[0]["name"]
    except Exception:
        pass
    return None, None


def search_trips_api(from_id, to_id, date):
    try:
        resp = requests.get(f"{FLIXBUS_API}/search/service/v4/search", params={
            "from_city_id": from_id,
            "to_city_id": to_id,
            "departure_date": date,
            "products": json.dumps({"adult": 1}),
            "currency": "EUR",
            "search_by": "cities"
        }, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        stations = data.get("stations", {})
        trips = data.get("trips", [])
        if trips:
            return trips[0].get("results", {}), stations
    except Exception:
        pass
    return {}, {}


def search_trips_playwright(from_id, to_id, flix_date):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {}, {}

    results = {}
    stations = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            def handle_resp(response):
                nonlocal results, stations
                if ('/search/service/v4/search' in response.url and
                        response.status == 200):
                    try:
                        data = response.json()
                        stations = data.get("stations", {})
                        trips = data.get("trips", [])
                        if trips:
                            results = trips[0].get("results", {})
                    except Exception:
                        pass

            page.on('response', handle_resp)
            url = (f"https://shop.flixbus.com/search?departureCity={from_id}"
                   f"&arrivalCity={to_id}&rideDate={flix_date}"
                   f"&adult=1&_locale=en")
            page.goto(url, timeout=30000)
            page.wait_for_timeout(8000)
            browser.close()
    except Exception:
        pass
    return results, stations


def parse_trips(results, stations, from_id, to_id, flix_date):
    parsed = []
    for uid, trip in results.items():
        if trip.get("status") != "available":
            continue

        dep = trip["departure"]["date"]
        arr = trip["arrival"]["date"]
        dep_station = stations.get(trip["departure"].get("station_id"),
                                   {}).get("name", "")
        arr_station = stations.get(trip["arrival"].get("station_id"),
                                   {}).get("name", "")
        dur = trip.get("duration", {})
        price_info = trip.get("price", {})
        legs = trip.get("legs", [])

        h = dur.get("hours", 0)
        m = dur.get("minutes", 0)
        duration_str = (f"{h}h {m}m" if h > 0 else
                        f"{m}m" if (h or m) else "N/A")

        link = (f"https://shop.flixbus.com/search?departureCity={from_id}"
                f"&arrivalCity={to_id}&rideDate={flix_date}"
                f"&adult=1&_locale=en&_sp=search-form")

        parsed.append({
            "departure": dep,
            "arrival": arr,
            "departure_station": dep_station,
            "arrival_station": arr_station,
            "duration": duration_str,
            "price": price_info.get("total_with_platform_fee") or
            price_info.get("total"),
            "currency": "EUR",
            "transfers": max(len(legs) - 1, 0),
            "provider": "FlixBus",
            "link": link
        })

    return sorted(parsed, key=lambda x: x["price"] or 9999)


def main():
    from_city = sys.argv[1]
    to_city = sys.argv[2]
    date = sys.argv[3]

    from_id, from_name = find_city(from_city)
    to_id, to_name = find_city(to_city)

    if not from_id or not to_id:
        print(json.dumps({"success": False, "error": "Could not find cities"}))
        return

    dt = datetime.strptime(date, "%Y-%m-%d")
    flix_date = dt.strftime("%d.%m.%Y")

    # Playwright gives accurate website prices, API may show lower prices
    results, stations = search_trips_playwright(from_id, to_id, flix_date)
    if not results:
        results, stations = search_trips_api(from_id, to_id, flix_date)

    trips = parse_trips(results, stations, from_id, to_id, flix_date)

    print(json.dumps({
        "success": True if trips else False,
        "trips": trips,
        "error": (None if trips else
                  "No bus routes found or service unavailable"),
        "search_params": {"from": from_name, "to": to_name, "date": date}
    }))


if __name__ == "__main__":
    main()

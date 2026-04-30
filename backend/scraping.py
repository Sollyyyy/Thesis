import sys
import json
import requests
import os

SKYSCANNER_API_KEY = os.environ.get('FLIGHT_API_KEY', '')


def get_comparisons(from_city, to_city, departure_date):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    req = requests.get(
        f'https://api.flightapi.io/onewaytrip/'
        f'{SKYSCANNER_API_KEY}/{from_city}/{to_city}/'
        f'{departure_date}/1/0/0/Economy/EUR',
        headers=headers, timeout=30)
    return req


def format_duration(minutes):
    if not minutes:
        return "N/A"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m" if hours > 0 else f"{mins}m"


def get_price_list(data):
    agent_map = {}
    for a in data.get('agents', []):
        agent_map[a['id']] = a['name']
    for c in data.get('carriers', []):
        agent_map[c.get('id', '')] = c.get('name', 'Unknown')

    legs_map = {}
    for leg in data.get('legs', []):
        legs_map[leg['id']] = leg

    results = []
    for flight in data.get('itineraries', []):
        leg_ids = flight.get('leg_ids', [])
        total_duration = 0
        for lid in leg_ids:
            dur = legs_map.get(lid, {}).get('duration')
            if dur:
                total_duration += dur

        for option in flight.get('pricing_options', []):
            agent_ids = option.get('agent_ids', [])
            agent_name = agent_map.get(agent_ids[0],
                                       "Unknown") if agent_ids else "Unknown"

            try:
                price = option['price']['amount']
                url_path = option['items'][0]['url']
                if not url_path or url_path == '/':
                    continue
                link = 'https://www.skyscanner.net' + url_path
            except (KeyError, IndexError):
                continue

            results.append({
                "agent": agent_name,
                "price": price,
                "duration": format_duration(total_duration if total_duration > 0 else None),
                "duration_minutes": total_duration if total_duration > 0 else None,
                "link": link
            })

    return sorted(results, key=lambda x: x['price'])


def main():
    departure = sys.argv[1]
    destination = sys.argv[2]
    depart_date = sys.argv[3]

    try:
        response = get_comparisons(departure, destination, depart_date)
        response.raise_for_status()
        data = response.json()

        if 'message' in data and 'itineraries' not in data:
            raise Exception(data['message'])

        price_list = get_price_list(data)

        result = {
            "success": True,
            "flights": price_list,
            "search_params": {
                "departure_airport": departure,
                "arrival_airport": destination,
                "departure_date": depart_date
            }
        }
    except Exception as e:
        result = {
            "success": False,
            "error": str(e),
            "flights": []
        }
    print(json.dumps(result))


if __name__ == "__main__":
    main()

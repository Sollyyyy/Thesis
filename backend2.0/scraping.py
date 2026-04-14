import sys
import json
import re
import requests
import os


def get_comparisons(from_city, to_city, departure_date, count_of_people,
                    count_of_kids, cabin_class, currency, returning_date=None):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    req = requests.get(f'https://api.flightapi.io/onewaytrip/'
                       f'69b44b1ad2b34942323b9882/{from_city}/{to_city}/'
                       f'{departure_date}/{count_of_people}/'
                       f'{count_of_kids}/0/{cabin_class}/{currency}',
                       headers=headers, timeout=30)
    # For a round trip
    # if returning_date:
    #     req = requests.get(f'https://api.flightapi.io/roundtrip/'
    #                        f'69b435d24767f41cdba06331/{from_city}/{to_city}/'
    #                        f'{departure_date}/{returning_date}/'
    #                        f'{count_of_people}/0/0/{cabin_class}'
    #                        f'/{currency}')
    return req


def parse_duration_from_segments(option):
    """Extract total duration in minutes from segment data in the URL."""
    try:
        url = option['items'][0]['url']
        # Match duration values like |105| or |65| from itinerary segments
        segments = re.findall(r'flight\|[^&]+', url)
        total_minutes = 0
        for seg in segments:
            parts = seg.split('|')
            # Duration is typically at index 7 in the segment
            for part in parts:
                if part.isdigit() and 10 <= int(part) <= 1500:
                    total_minutes += int(part)
                    break
        return total_minutes if total_minutes > 0 else None
    except (KeyError, IndexError):
        return None


def format_duration(minutes):
    if not minutes:
        return "N/A"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m" if hours > 0 else f"{mins}m"


def get_price_list(data):
    agent_map = {a['id']: a['name'] for a in data.get('agents', [])}

    results = []
    for flight in data.get('itineraries', []):
        for option in flight.get('pricing_options', []):
            agent_id = option['agent_ids'][0]
            agent_name = agent_map.get(agent_id, "Unknown")
            try:
                price = option['price']['amount']
                link = 'https://www.skyscanner.net' + option['items'][0]['url']
            except KeyError:
                continue

            duration_mins = parse_duration_from_segments(option)

            results.append({
                "agent": agent_name,
                "price": price,
                "duration": format_duration(duration_mins),
                "duration_minutes": duration_mins,
                "link": link
            })
    return sorted(results, key=lambda x: x['price'])


def grab_cmdln_args():
    cmd_line_data = {}
    cmd_line_data["departure_airport"] = str(sys.argv[1])
    cmd_line_data["arrival_airport"] = sys.argv[2]
    cmd_line_data["departure_date"] = sys.argv[3]
    cmd_line_data["return_date"] = sys.argv[4] if len(sys.argv) > 4 else None
    return cmd_line_data


def main():
    command_line_data = grab_cmdln_args()
    try:
        response = get_comparisons(
            command_line_data["departure_airport"],
            command_line_data["arrival_airport"],
            command_line_data["departure_date"],
            '1', '0', 'Economy', 'EUR',
            command_line_data["return_date"])
        response.raise_for_status()
        data = response.json()
        price_list = get_price_list(data)

        result = {
            "success": True,
            "flights": price_list,
            "search_params": command_line_data
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

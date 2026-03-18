import sys
import json
import requests


def get_comparisons(from_city, to_city, departure_date, count_of_people,
                    count_of_kids, cabin_class, currency, returning_date=None):
    req = requests.get(f'https://api.flightapi.io/onewaytrip/'
                       f'69b435d24767f41cdba06331/{from_city}/{to_city}/'
                       f'{departure_date}/{count_of_people}/'
                       f'{count_of_kids}/0/{cabin_class}/{currency}')
    # For a round trip
    # if returning_date:
    #     req = requests.get(f'https://api.flightapi.io/roundtrip/'
    #                        f'69b435d24767f41cdba06331/{from_city}/{to_city}/'
    #                        f'{departure_date}/{returning_date}/'
    #                        f'{count_of_people}/0/0/{cabin_class}'
    #                        f'/{currency}')
    return req


# Assuming 'data' is your JSON object
def get_price_list(data):
    # 1. Create a lookup dictionary for agent names
    agent_map = {a['id']: a['name'] for a in data.get('agents', [])}

    results = []
    # 2. Iterate through itineraries to find prices
    for flight in data.get('itineraries', []):
        for option in flight.get('pricing_options', []):
            # Get the first agent ID for this price point
            agent_id = option['agent_ids'][0]
            agent_name = agent_map.get(agent_id, "Unknown")
            try:
                price = option['price']['amount']
                link = 'https://www.skyscanner.net' + option['items'][0]['url']
            except KeyError:
                continue
            results.append({
                "agent": agent_name,
                "price": price,
                "link": link
            })
    # Sort by price ascending
    return sorted(results, key=lambda x: x['price'])


def grab_cmdln_args():
    command_line_data = {}
    command_line_data["departure_airport"] = str(sys.argv[1])
    command_line_data["arrival_airport"] = sys.argv[2]
    command_line_data["departure_date"] = sys.argv[3]
    command_line_data["return_date"] = sys.argv[4] if len(sys.argv) > 4 else None
    return command_line_data


def main():
    command_line_data = grab_cmdln_args()
    data = get_comparisons(
        command_line_data["departure_airport"],
        command_line_data["arrival_airport"],
        command_line_data["departure_date"],
        '1', '0', 'Economy', 'EUR',
        command_line_data["return_date"])
    price_list = get_price_list(data.json())
    
    # Output as JSON for the backend to parse
    result = {
        "success": True,
        "flights": price_list,
        "search_params": command_line_data
    }
    print(json.dumps(result))


if __name__ == "__main__":
    # Print the results
    # with open('../data.json', 'r') as f:
    #     your_json_data = json.load(f)
    main()

import urllib.parse
import requests
from datetime import datetime, timedelta

print("=============================================")
print("\t\tCANVAS RIDE")
print("=============================================")

def get_route(orig, dest):
    main_api = "http://www.mapquestapi.com/directions/v2/route?"
    key = "D3evZAsYffWCgU0I5uHPXsSGivbtdjmu"  # Your API key here
    
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            print("Error: Unauthorized access. Please check your API key.")
        else:
            print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")
    return None

def display_route_info(json_data, orig, dest):
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print(f"API Status: {json_status} = A successful route call.\n")
        print("=============================================")
        print(f"Directions from {orig} to {dest}")
        
        # Trip Duration
        
        print(f"Trip Duration: {json_data['route']['formattedTime']}")
        
        # Distance
        distance = json_data["route"]["distance"]
        print(f"Distance: {distance:.2f} kilometers")
        
        # Estimated Arrival Time
        trip_duration_seconds = json_data["route"]["realTime"]
        current_time = datetime.now()
        arrival_time = current_time + timedelta(seconds=trip_duration_seconds)
        print(f"Estimated Arrival Time: {arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Display detailed maneuvers
        print("=============================================")
        print("Routes to Go:\n")

        for each in json_data["route"]["legs"][0]["maneuvers"]:
            narrative = each['narrative']
            maneuver_distance = each['distance'] * 1.61  # Convert miles to kilometers if needed
            print(f"{narrative} ({maneuver_distance:.2f} km)")
        
        print("=============================================")
        print("\t\tEND OF RIDE")
        print("=============================================")

    elif json_status == 402:
        print("**********************************************")
        print(f"Status Code: {json_status}; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    
    elif json_status == 611:
        print("**********************************************")
        print(f"Status Code: {json_status}; Missing an entry for one or both locations.")
        print("**********************************************\n")
    
    else:
        print("************************************************************************")
        print(f"For Status Code: {json_status}; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")



def main():
    while True:
        orig = input("Starting Location (type 'quit' or 'q' to exit): ")
        if orig.lower() in ["quit", "q"]:
            break
        
        dest = input("Destination (type 'quit' or 'q' to exit): ")
        if dest.lower() in ["quit", "q"]:
            break
        
        json_data = get_route(orig, dest)
        
        if json_data is not None:
            display_route_info(json_data, orig, dest)


if __name__ == "__main__":
    main()
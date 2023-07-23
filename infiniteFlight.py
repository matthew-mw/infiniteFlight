import requests
import time
import matplotlib.pyplot as plt

# Constants
server_ids = [server["id"] for server in requests.get("https://api.liveflight.dev/v7/sessions").json()["responseData"] if server["name"] == "All Servers"][0]

def get_flight_id(callsign):
    response_data = requests.get(f"https://api.liveflight.dev/v7/flights/{server_ids}").json()["responseData"]
    flight_ids = [flight["flightId"] for flight in response_data if flight["callsign"] == callsign]
    if flight_ids:
        if len(flight_ids) > 1:
            print("Multiple flights found")
            for i, flight in enumerate(flight_ids):
                print(f"{i+1}. {flight}")
            flight_id = flight_ids[int(input("Enter flight number: ")) - 1]
        else:
            flight_id = flight_ids[0]
        return flight_id
    else:
        return None

def plot_flight_data(flight_id):
    response_data = requests.get(f"https://api.liveflight.dev/v7/flight/{flight_id}/info").json()["responseData"]
    position_reports = response_data["positionReports"]
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("time (20s)")
    color = "gold"
    ax1.set_ylabel("GROUND SPEED (kts)", color=color)
    ax1.plot([report["speed"] for report in position_reports], color=color)
    ax1.tick_params(axis="y", labelcolor=color)
    ax2 = ax1.twinx()
    color = "royalblue"
    ax2.set_ylabel("ALTITUDE (ft)", color=color)
    ax2.plot([report["altitude"] for report in position_reports], color=color)
    ax2.tick_params(axis="y", labelcolor=color)
    fig.tight_layout()
    plt.savefig("infiniteFlight.png")
    plt.close()

if __name__ == "__main__":
    flight_id = get_flight_id(input("Enter callsign: "))
    while flight_id:
        plot_flight_data(flight_id)
        time.sleep(60)
        flight_id = get_flight_id(input("Enter callsign: "))

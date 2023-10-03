import pandas as pd
import sys
from bluesky.__main__ import main
from calculator import calculate_bearing
from calculator import calculate_distance
from calculator import calculate_new_point

flights = pd.read_csv("Flights.csv")

# Load airport data from your airport file into a DataFrame
airport_data = pd.read_csv("airports.csv")


def get_airport_info(code, info_type):
    matching_row = airport_data[airport_data["icao"] == code]
    if not matching_row.empty:
        # Extract latitude and longitude coordinates from the matching row
        lat = matching_row.iloc[0]["lat"]
        lon = matching_row.iloc[0]["lon"]

        if info_type == "LAT":
            return lat
        elif info_type == "LON":
            return lon
    return None  # Airport code not found in the airport data


# Remove duplicates from the CALLSIGN column
flights = flights.drop_duplicates(subset="CALLSIGN", keep="first")
flights["ORIG_LATITUDE"] = flights["ADEP"].apply(get_airport_info, args=("LAT",))
flights["ORIG_LONGITUDE"] = flights["ADEP"].apply(get_airport_info, args=("LON",))
flights["DEST_LATITUDE"] = flights["DEST"].apply(get_airport_info, args=("LAT",))
flights["DEST_LONGITUDE"] = flights["DEST"].apply(get_airport_info, args=("LON",))
flightCallSign = flights["CALLSIGN"]
flightProvider = flights["OPERATOR"]
flightType = flights["ICAO_ACTYPE"]
flightDest = flights["DEST"]
flightOrig = flights["ADEP"]
flightSpeed = flights["TAS"]
flightAltitude = flights["RFL"]
flightWeight = flights["TYPE_OF_TRANSPONDER"]
flightArrival = flights["T0"]
flightDeparture = flights["T_UPDATE"]


def has_required_data(x):
    # Check if all required columns have non-empty values
    return all([
        pd.notna(flightCallSign.iloc[x]) and flightCallSign.iloc[x] != "",
        pd.notna(flightType.iloc[x]) and flightType.iloc[x] != "",
        pd.notna(flightOrig.iloc[x]) and flightOrig.iloc[x] != "" and flightOrig.iloc[x] != flightDest.iloc[x] and flightOrig.iloc[x] != "ZZZZ",
        pd.notna(flightAltitude.iloc[x]) and flightAltitude.iloc[x] != 0,
        pd.notna(flightSpeed.iloc[x]) and flightSpeed.iloc[x] != 0,
        pd.notna(flightDest.iloc[x]) and flightDest.iloc[x] != "" and flightDest.iloc[x] != flightOrig.iloc[x] and flightDest.iloc[x] != "ZZZZ"
    ])


def airlines():
    providers = flightProvider.drop_duplicates(keep="first").astype(str).to_list()
    return providers


def write_scene_file(filename):
    with open(filename, 'w') as file:
        for x in range(flights.shape[0]):
            if has_required_data(x):
                orig_lat = flights["ORIG_LATITUDE"].iloc[x]
                orig_lon = flights["ORIG_LONGITUDE"].iloc[x]
                dest_lat = flights["DEST_LATITUDE"].iloc[x]
                dest_lon = flights["DEST_LONGITUDE"].iloc[x]
                dist = calculate_distance(orig_lat, orig_lon, dest_lat, dest_lon)
                f = 1-50000/dist  # You can adjust the fraction as needed
                delta = 1  # Calculate the angular distance based on your data
                new_lat, new_lon = calculate_new_point(orig_lat, orig_lon, dest_lat, dest_lon, f, delta)
                brng = calculate_bearing(new_lat, new_lon, dest_lat, dest_lon)
                scenetext = (
                    f"00:00:00.00>CRE {flightCallSign.iloc[x]} {flightType.iloc[x]} {new_lat} {new_lon} {brng} "
                    f"FL{int(flightAltitude.iloc[x])} {flightSpeed.iloc[x]}\n"
                    f"00:00:00.00>DEST {flightCallSign.iloc[x]} {flightDest.iloc[x]}\n"
                    f"00:00:00.00>{flightCallSign.iloc[x]} ATDIST {flightDest.iloc[x]} DO DEL {flightCallSign.iloc[x]}\n"
                )
                file.write(scenetext)


if __name__ == "__main__":
    write_scene_file("scenefile.scn")
    # airlines()
    # sys.exit(main())

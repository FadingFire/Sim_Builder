import pandas as pd
import sys
from bluesky.__main__ import main
from calculator import calculate_bearing, calculate_distance, calculate_new_point


# Load airport data from your airport file into a DataFrame
airport_data = pd.read_csv("airports.csv")

combined_df = pd.read_excel("complete.xlsx")


def get_airport_info(code, info_type):
    matching_row = airport_data[airport_data["# code"] == code]
    if not matching_row.empty:
        # Extract latitude and longitude coordinates from the matching row
        lat = matching_row.iloc[0]["lat"]
        lon = matching_row.iloc[0]["lon"]

        # Check if lat and lon are valid (not NaN)
        if pd.notna(lat) and pd.notna(lon):
            if info_type == "LAT":
                return lat
            elif info_type == "LON":
                return lon
    return None


# Remove duplicates from the CALLSIGN column
flights_copy = combined_df.copy()
flights_copy["ORIG_LATITUDE"] = combined_df["ADEP"].apply(lambda x: get_airport_info(x, "LAT"))
flights_copy["ORIG_LONGITUDE"] = combined_df["ADEP"].apply(lambda x: get_airport_info(x, "LON"))
flights_copy["DEST_LATITUDE"] = combined_df["DEST"].apply(lambda x: get_airport_info(x, "LAT"))
flights_copy["DEST_LONGITUDE"] = combined_df["DEST"].apply(lambda x: get_airport_info(x, "LON"))
flightCallSign = combined_df["CALLSIGN"]
flightProvider = combined_df["OPERATOR"]
flightType = combined_df["ICAO_ACTYPE"]
flightDest = combined_df["DEST"]
flightOrig = combined_df["ADEP"]
flightSpeed = combined_df["TAS"]
flightAltitude = combined_df["RFL"]
flightWeight = combined_df["TYPE_OF_TRANSPONDER"]
flightArrival = combined_df["T0"]
flightDeparture = combined_df["T_UPDATE"]


def has_required_data(x):
    # Check if all required columns have non-empty values
    return all([
        pd.notna(flightCallSign.iloc[x]) and flightCallSign.iloc[x] != "",
        pd.notna(flightType.iloc[x]) and flightType.iloc[x] != "",
        pd.notna(flightOrig.iloc[x]) and flightOrig.iloc[x] != "" and flightOrig.iloc[x] != flightDest.iloc[x] and flightOrig.iloc[x] != "ZZZZ",
        pd.notna(flightAltitude.iloc[x]) and flightAltitude.iloc[x] != 0,
        pd.notna(flightSpeed.iloc[x]) and flightSpeed.iloc[x] != 0,
        pd.notna(flightDest.iloc[x]) and flightDest.iloc[x] != "" and flightDest.iloc[x] != flightOrig.iloc[x] and flightDest.iloc[x] != "ZZZZ",
        pd.notna(flights_copy["DEST_LATITUDE"].iloc[x]),
        pd.notna(flights_copy["DEST_LONGITUDE"].iloc[x]),
        pd.notna(flights_copy["ORIG_LATITUDE"].iloc[x]),
        pd.notna(flights_copy["ORIG_LONGITUDE"].iloc[x])
    ])


def airlines():
    providers = flightProvider.drop_duplicates(keep="first").astype(str).to_list()
    return providers


def write_scene_file(filename):
    with open(filename, 'w') as file:
        for x in range(combined_df.shape[0]):
            if has_required_data(x):
                orig_lat = flights_copy["ORIG_LATITUDE"].iloc[x]
                orig_lon = flights_copy["ORIG_LONGITUDE"].iloc[x]
                dest_lat = flights_copy["DEST_LATITUDE"].iloc[x]
                dest_lon = flights_copy["DEST_LONGITUDE"].iloc[x]
                dist = calculate_distance(orig_lat, orig_lon, dest_lat, dest_lon)
                f = 1 - 50000 / dist  # You can adjust the fraction as needed
                delta = 1  # Calculate the angular distance based on your data
                new_lat, new_lon = calculate_new_point(orig_lat, orig_lon, dest_lat, dest_lon, f, delta)
                brng = calculate_bearing(new_lat, new_lon, dest_lat, dest_lon)

                # Convert flightAltitude to an integer after converting it to a string
                flight_altitude = int(float(flightAltitude.iloc[x]))

                scenetext = (
                    f"00:00:00.00>CRE {flightCallSign.iloc[x]} {flightType.iloc[x]} {new_lat} {new_lon} {brng} "
                    f"FL{flight_altitude} {flightSpeed.iloc[x]}\n"
                    f"00:00:00.00>DEST {flightCallSign.iloc[x]} {flightDest.iloc[x]}\n"
                    f"00:00:00.00>{flightCallSign.iloc[x]} AT {flightDest.iloc[x]} DO DEL {flightCallSign.iloc[x]}\n"
                )
                file.write(scenetext)


write_scene_file("scenefile.scn")
# airlines()
# sys.exit(main())

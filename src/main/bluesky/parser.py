import pandas as pd
from calculator import calculate_bearing


# Load airport data from your airport file into a DataFrame
airport_data = pd.read_csv("Data/airports.csv")


airport_info_dict = airport_data.set_index("# code")[["lat", "lon"]].to_dict(orient="index")


combined_df = pd.read_excel("Data/complete.xlsx")


def get_airport_info(code, info_type):
    airport_info = airport_info_dict.get(code)
    if airport_info:
        if info_type == "LAT":
            return airport_info["lat"]
        elif info_type == "LON":
            return airport_info["lon"]
    return None


# Remove duplicates from the CALLSIGN column
combined_df = combined_df.drop_duplicates(subset="CALLSIGN", keep="first")
combined_df["DEST_LATITUDE"] = combined_df["DEST"].map(lambda x: get_airport_info(x, "LAT"))
combined_df["DEST_LONGITUDE"] = combined_df["DEST"].map(lambda x: get_airport_info(x, "LON"))
flightCallSign = combined_df["CALLSIGN"]
flightProvider = combined_df["OPERATOR"]
flightType = combined_df["ICAO_ACTYPE"]
flightDest = combined_df["DEST"]
flightOrig = combined_df["ADEP"]
flightSpeed = combined_df["TAS"]
flightAltitude = combined_df["RFL"]
flightWeight = combined_df["TYPE_OF_TRANSPONDER"]
flightarrival = combined_df["STACK"]



def has_required_data(x):
    # Check if all required columns have non-empty values
    return all([
        pd.notna(flightCallSign.iloc[x]) and flightCallSign.iloc[x] != "",
        pd.notna(flightType.iloc[x]) and flightType.iloc[x] != "",
        pd.notna(flightOrig.iloc[x]) and flightOrig.iloc[x] != "" and flightOrig.iloc[x] != flightDest.iloc[x] and flightOrig.iloc[x] != "ZZZZ",
        pd.notna(flightAltitude.iloc[x]) and flightAltitude.iloc[x] != 0,
        pd.notna(flightSpeed.iloc[x]) and flightSpeed.iloc[x] != 0,
        pd.notna(flightDest.iloc[x]) and flightDest.iloc[x] != "" and flightDest.iloc[x] != flightOrig.iloc[x] and flightDest.iloc[x] != "ZZZZ",
        pd.notna(combined_df["DEST_LATITUDE"].iloc[x]),
        pd.notna(combined_df["DEST_LONGITUDE"].iloc[x]),
    ])


def airlines():
    providers = flightProvider.drop_duplicates(keep="first").astype(str).to_list()
    print(providers)
    return providers


def write_scene_file(filename):
    with (open(filename, 'w') as file):
        for x in range(combined_df.shape[0]):
            if has_required_data(x):
                dest_lat = combined_df["DEST_LATITUDE"].iloc[x]
                dest_lon = combined_df["DEST_LONGITUDE"].iloc[x]
                sugolLat = 52.525
                sugolLon = 3.967
                artipLat = 52.511
                artipLon = 5.569
                riverLat = 51.912
                riverLon = 4.132
                ehamLat = 52.309
                ehamLon = 4.764
                if flightarrival.iloc[x] == "RIVER":
                    brng = calculate_bearing(riverLat, riverLon, ehamLat, ehamLon)
                elif flightarrival.iloc[x] == "SUGOL":
                    brng = calculate_bearing(sugolLat, sugolLon, ehamLat, ehamLon)
                elif flightarrival.iloc[x] == "ARTIP":
                    brng = calculate_bearing(artipLat, artipLon, ehamLat, ehamLon)
                else:
                    brng = calculate_bearing(ehamLat, ehamLon, dest_lat, dest_lon)
                # Convert flightAltitude to an integer after converting it to a string
                flight_altitude = int(float(flightAltitude.iloc[x]))
                if flightOrig.iloc[x] == 'EHAM':
                    scenetext = (
                        f"00:00:00.00>CRE {flightCallSign.iloc[x]} {flightType.iloc[x]} EHAM {brng} "
                        f"FL{flight_altitude} {flightSpeed.iloc[x]}\n"
                        f"00:00:00.00>DEST {flightCallSign.iloc[x]} {flightDest.iloc[x]}\n"
                        f"00:00:00.00>{flightCallSign.iloc[x]} ATDIST {flightOrig.iloc[x]} 30 DEL {flightCallSign.iloc[x]}\n"
                    )
                    file.write(scenetext)
                elif pd.notna(flightarrival.iloc[x]):
                    scenetext = (
                        f"00:00:00.00>CRE {flightCallSign.iloc[x]} {flightType.iloc[x]} {flightarrival.iloc[x]} {brng} "
                        f"FL{flight_altitude} {flightSpeed.iloc[x]}\n"
                        f"00:00:00.00>DEST {flightCallSign.iloc[x]} {flightDest.iloc[x]}\n"
                        f"00:00:00.00>{flightCallSign.iloc[x]} AT {flightDest.iloc[x]} DO DEL {flightCallSign.iloc[x]}\n"
                    )
                    file.write(scenetext)


write_scene_file("Data/scenefile.scn")
# airlines()

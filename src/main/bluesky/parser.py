import numpy as np
import pandas as pd
import math


# Read the airport data and store it in a global variable
airport_data = pd.read_csv("Data/airports.csv")
airport_info_dict = airport_data.set_index("# code")[["lat", "lon"]].to_dict(orient="index")


def get_dutch_airports():
    dutch_airports = airport_data[airport_data[" country code"].str.strip() == "NL"]
    airports = dutch_airports["# code"].astype(str).to_list()
    return airports


def get_airport_info(code, info_type):
    # making the airport info into a dictionary
    airport_info = airport_info_dict.get(code)
    if airport_info:
        return airport_info.get(info_type, None)
    return None


def calculate_bearing(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Calculate bearing
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    theta = math.atan2(y, x)
    bearing = (theta * 180 / math.pi + 360) % 360  # in degrees
    return round(0 if np.isnan(bearing) else bearing, 2)


def has_required_data(row):
    # Check if the row has all required data
    return all([
        pd.notna(row["CALLSIGN"]) and row["CALLSIGN"] != "",
        pd.notna(row["ICAO_ACTYPE"]) and row["ICAO_ACTYPE"] != "",
        pd.notna(row["ADEP"]) and row["ADEP"] != row["DEST"] and row["ADEP"] != "ZZZZ",
        pd.notna(row["RFL"]) and row["RFL"] != 0,
        pd.notna(row["TAS"]) and row["TAS"] != 0,
        pd.notna(row["DEST"]) and row["DEST"] != row["ADEP"] and row["DEST"] != "ZZZZ",
        pd.notna(row["DEST_LATITUDE"]),
        pd.notna(row["DEST_LONGITUDE"])
    ])


def write_scene_file(filename, combined_df):
    with open(filename, 'w') as file:
        for index, row in combined_df.iterrows():
            scenetext = ""
            if has_required_data(row):
                lat, lon = get_airport_info(row["DEST"], "lat"), get_airport_info(row["DEST"], "lon")
                ehamLat, ehamLon = 52.309, 4.764
                stack = row.get("STACK", None)
                # check if stack is not empty and set stack and brng
                if lat is not None and lon is not None:
                    if stack in ["RIVER", "SUGOL", "ARTIP"]:
                        lat, lon = {
                            "RIVER": (51.912, 4.132),
                            "SUGOL": (52.525, 3.967),
                            "ARTIP": (52.511, 5.569)
                        }.get(stack, (lat, lon))
                        brng = calculate_bearing(lat, lon, ehamLat, ehamLon)
                    # else brng is calculated from origin
                    else:
                        brng = calculate_bearing(ehamLat, ehamLon, lat, lon)
                    flight_altitude = int(float(row["RFL"]))
                    # if origin is Amsterdam, set the origin to EHAM and delete at a distance of 30
                    Nederland = get_dutch_airports()
                    if row['ADEP'] in Nederland:
                        scenetext = (
                            f"00:00:00.00>CRE {row['CALLSIGN']} {row['ICAO_ACTYPE']} {row['ADEP']} {brng} "
                            f"FL{flight_altitude} {row['TAS']}\n"
                            f"00:00:00.00>DEST {row['CALLSIGN']} {row['DEST']}\n"
                            f"00:00:00.00>{row['CALLSIGN']} ATDIST {row['ADEP']} 30 DEL {row['CALLSIGN']}\n"
                        )
                    # else if stack is not empty set origin as the correct stack and delete at Amsterdam
                    elif pd.notna(stack):
                        scenetext = (
                            f"00:00:00.00>CRE {row['CALLSIGN']} {row['ICAO_ACTYPE']} {stack} {brng} "
                            f"FL{flight_altitude} {row['TAS']}\n"
                            f"00:00:00.00>DEST {row['CALLSIGN']} {row['DEST']}\n"
                            f"00:00:00.00>{row['CALLSIGN']} AT {row['DEST']} DO DEL {row['CALLSIGN']}\n"
                        )
                    # write to the scenefile
                    file.write(scenetext)


def getdata(input_file, output_file, sort_amount):
    # read the complete Csv file and drop all duplicate Callsigns
    combined_df = pd.read_csv(input_file)
    combined_df.drop_duplicates(subset="CALLSIGN", keep="first", inplace=True)

    def get_dest_lat_lon(dest):
        # get the lat and lon of the destinations from the dictionary
        airport_info = airport_info_dict.get(dest)
        if airport_info:
            return airport_info.get("lat", None), airport_info.get("lon", None)
        else:
            return None, None

    combined_df["DEST_LATITUDE"], combined_df["DEST_LONGITUDE"] = zip(*combined_df["DEST"].map(get_dest_lat_lon))

    # Create an empty DataFrame to store the selected rows
    selected_rows = pd.DataFrame(columns=combined_df.columns)
    Nederland = get_dutch_airports()

    # Loop through the DataFrame and select the given amount that meet the criteria
    for index, row in combined_df.iterrows():
        if len(selected_rows) >= sort_amount:
            break  # Exit the loop if given amount has been selected
        if has_required_data(row) and (row["ADEP"] in Nederland or pd.notna(row["STACK"])):
            selected_rows = pd.concat([selected_rows, pd.DataFrame(row).T])
    # run write function with correct files
    write_scene_file(output_file, selected_rows)

import pandas as pd
from calculator import calculate_bearing

# Read the airport data and store it in a global variable
airport_data = pd.read_csv("Data/airports.csv")
airport_info_dict = airport_data.set_index("# code")[["lat", "lon"]].to_dict(orient="index")


def get_airport_info(code, info_type):
    airport_info = airport_info_dict.get(code)
    if airport_info:
        return airport_info.get(info_type, None)
    return None


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
                ehamLat, ehamLon = 52.309, 4.764  # Replace with actual values
                stack = row.get("STACK", None)
                if lat is not None and lon is not None:  # Check if lat and lon are valid
                    if stack in ["RIVER", "SUGOL", "ARTIP"]:
                        lat, lon = {
                            "RIVER": (51.912, 4.132),
                            "SUGOL": (52.525, 3.967),
                            "ARTIP": (52.511, 5.569)
                        }.get(stack, (lat, lon))
                        brng = calculate_bearing(lat, lon, ehamLat, ehamLon)
                    else:
                        brng = calculate_bearing(ehamLat, ehamLon, lat, lon)
                    flight_altitude = int(float(row["RFL"]))
                    if row['ADEP'] == 'EHAM':
                        scenetext = (
                            f"00:00:00.00>CRE {row['CALLSIGN']} {row['ICAO_ACTYPE']} {row['ADEP']} {brng} "
                            f"FL{flight_altitude} {row['TAS']}\n"
                            f"00:00:00.00>DEST {row['CALLSIGN']} {row['DEST']}\n"
                            f"00:00:00.00>{row['CALLSIGN']} ATDIST {row['ADEP']} 30 DEL {row['CALLSIGN']}\n"
                        )
                    elif pd.notna(stack):
                        scenetext = (
                            f"00:00:00.00>CRE {row['CALLSIGN']} {row['ICAO_ACTYPE']} {stack} {brng} "
                            f"FL{flight_altitude} {row['TAS']}\n"
                            f"00:00:00.00>DEST {row['CALLSIGN']} {row['DEST']}\n"
                            f"00:00:00.00>{row['CALLSIGN']} AT {row['DEST']} DO DEL {row['CALLSIGN']}\n"
                        )
                    file.write(scenetext)


def getdata(input_file, output_file):
    combined_df = pd.read_excel(input_file)
    combined_df.drop_duplicates(subset="CALLSIGN", keep="first", inplace=True)

    def get_dest_lat_lon(dest):
        airport_info = airport_info_dict.get(dest)
        if airport_info:
            return airport_info.get("lat", None), airport_info.get("lon", None)
        else:
            # Provide default values (you can replace these with appropriate defaults)
            return None, None

    combined_df["DEST_LATITUDE"], combined_df["DEST_LONGITUDE"] = zip(*combined_df["DEST"].map(get_dest_lat_lon))

    write_scene_file(output_file, combined_df)


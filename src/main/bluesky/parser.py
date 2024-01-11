import numpy as np
import pandas as pd
import math


# Read the airport data and store it in a global variable
airport_data = pd.read_csv("src/main/bluesky/Data/airports.csv")
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


def write_scene_file(filename, combined_df, total_time):
    with open(filename, 'w') as file:
        current_time = 0
        time_step = int(total_time) / len(combined_df)

        for index, row in combined_df.iterrows():
            scenetext = ""
            lat, lon = get_airport_info(row["DEST"], "lat"), get_airport_info(row["DEST"], "lon")
            ehamLat, ehamLon = 52.309, 4.764
            stack = row.get("STACK", None)

            # Calculate time stamp
            current_time += time_step
            hours = int(current_time // 3600)
            minutes = int((current_time % 3600) // 60)
            seconds = current_time % 60
            time_stamp = f"{hours:02d}:{minutes:02d}:{seconds:.2f}"

            if lat is not None and lon is not None and stack in ["RIVER", "SUGOL", "ARTIP"]:
                lat, lon = {
                    "RIVER": (51.912, 4.132),
                    "SUGOL": (52.525, 3.967),
                    "ARTIP": (52.511, 5.569)
                }.get(stack, (lat, lon))
                brng = calculate_bearing(lat, lon, ehamLat, ehamLon)
            else:
                brng = calculate_bearing(ehamLat, ehamLon, lat, lon)

            flight_altitude = int(float(row["RFL"]))

            Netherlands = get_dutch_airports()
            if row['ADEP'] in Netherlands:
                scenetext = (
                    f"{time_stamp}>CRE {row['CALLSIGN']} {row['ICAO_ACTYPE']} {row['ADEP']} {brng} "
                    f"FL{flight_altitude} {row['TAS']}\n"
                    f"{time_stamp}>DEST {row['CALLSIGN']} {row['DEST']}\n"
                    f"{time_stamp}>{row['CALLSIGN']} ATDIST {row['ADEP']} 30 DEL {row['CALLSIGN']}\n"
                )
            elif pd.notna(stack):
                scenetext = (
                    f"{time_stamp}>CRE {row['CALLSIGN']} {row['ICAO_ACTYPE']} {stack} {brng} "
                    f"FL{flight_altitude} {row['TAS']}\n"
                    f"{time_stamp}>DEST {row['CALLSIGN']} {row['DEST']}\n"
                    f"{time_stamp}>{row['CALLSIGN']} AT {row['DEST']} DO DEL {row['CALLSIGN']}\n"
                )

            file.write(scenetext)


def getdata(input_file, output_file, sort_amount, diramount, wtc_amount, app_value, total_time):
    combined_df = pd.read_csv(input_file)
    combined_df.drop_duplicates(subset="CALLSIGN", keep="first", inplace=True)

    def get_dest_lat_lon(dest):
        airport_info = airport_info_dict.get(dest)
        if airport_info:
            return airport_info.get("lat", None), airport_info.get("lon", None)
        else:
            return None, None

    combined_df["DEST_LATITUDE"], combined_df["DEST_LONGITUDE"] = zip(*combined_df["DEST"].map(get_dest_lat_lon))
    selected_rows_list = []
    weights = {
        'L': [],
        'M': [],
        'H': [],
        'J': [],
    }
    Netherlands = get_dutch_airports()

    percRiver, percArtip, percSugol = diramount.split(sep=",")
    percSTACK, percEHAM = app_value.split(sep=",")
    wtc_percentages = wtc_amount.split(sep=",")
    wtc_labels = ["L", "M", "H", "J"]
    stacksort_amount = sort_amount * int(percSTACK) / 100
    for wtc, percwtc in zip(wtc_labels, wtc_percentages):
        if percwtc <= "0":
            percwtc = "1"
        weights[wtc].append(percwtc)
    combined_df['weightswtc'] = combined_df['WTC'].apply(lambda x: weights[x])
    combined_df['weightswtc'] = combined_df['weightswtc'].apply(lambda x: int(x[0]) if isinstance(x, list) and len(x) > 0 else x)

    for stack, perc in [("RIVER", percRiver), ("ARTIP", percArtip), ("SUGOL", percSugol)]:
        stack_amount = stacksort_amount * float(perc) / 100
        if stack_amount > 0:
            stack_amount = math.ceil(stack_amount)
            filtered_df = combined_df[(combined_df["STACK"] == stack) &
                                      pd.notna(combined_df["DEST_LATITUDE"]) &
                                      pd.notna(combined_df["DEST_LONGITUDE"])]
            if len(filtered_df) > 0:
                wtc_df = filtered_df.sample(n=int(stack_amount), weights='weightswtc')
                selected_rows_list.append(wtc_df)

    EHAM_amount = sort_amount * float(percEHAM) / 100
    if EHAM_amount > 0:
        filtered_df = combined_df[(combined_df["ADEP"] == "EHAM") &
                                  pd.notna(combined_df["DEST_LATITUDE"]) &
                                  pd.notna(combined_df["DEST_LONGITUDE"])]

        wtc_df = filtered_df.sample(n=int(EHAM_amount), weights='weightswtc')
        selected_rows_list.append(wtc_df)

    selected_rows = pd.concat(selected_rows_list).head(sort_amount)
    selected_rows = selected_rows.sample(frac=1)

    # run write function with correct files
    write_scene_file(output_file, selected_rows, total_time)

import pandas as pd

flights = pd.read_csv("Flights.csv")

flightCallSign = flights["CALLSIGN"]
flightProvider = flights["OPERATOR"]
flightType = flights["ICAO_ACTYPE"]
flightDest = flights["DEST"]
flightOrig = flights["ADEP"]
flightAltitude = flights["RFL"]
flightWeight = flights["TYPE_OF_TRANSPONDER"]
flightArrival = flights["T0"]
flightDeparture = flights["T_UPDATE"]


def has_required_data(x):
    # Check if all required columns have non-empty values
    return all([
        pd.notna(flightCallSign[x]) and flightCallSign[x] != "",
        pd.notna(flightType[x]) and flightType[x] != "",
        pd.notna(flightOrig[x]) and flightOrig[x] != "" and flightOrig[x] != flightDest[x],
        pd.notna(flightAltitude[x]) and flightAltitude[x] != 0,
        pd.notna(flightDest[x]) and flightDest[x] != "" and flightDest[x] != flightOrig[x]
    ])


def write_scene_file(filename):
    with open(filename, 'w') as f:
        for x in range(flights.shape[0]):
            if has_required_data(x):
                scenetext = (
                    f"00:00:00.00>CRE {flightCallSign[x]} {flightType[x]} {flightOrig[x]} 0 "
                    f"{flightAltitude[x]} {flightAltitude[x]}\n"
                    f"00:00:00.00>DEST {flightCallSign[x]} {flightDest[x]}\n"
                )
                f.write(scenetext)


if __name__ == "__main__":
    write_scene_file("scenefile.scn")

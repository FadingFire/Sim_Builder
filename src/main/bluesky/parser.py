import pandas as pd
import sys
from bluesky.__main__ import main

flights = pd.read_csv("Flights.csv")

# Remove duplicates from the CALLSIGN column
flights = flights.drop_duplicates(subset="CALLSIGN", keep="first")

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
        pd.notna(flightOrig.iloc[x]) and flightOrig.iloc[x] != "" and flightOrig.iloc[x] != flightDest.iloc[x],
        pd.notna(flightAltitude.iloc[x]) and flightAltitude.iloc[x] != 0,
        pd.notna(flightSpeed.iloc[x]) and flightSpeed.iloc[x] != 0,
        pd.notna(flightDest.iloc[x]) and flightDest.iloc[x] != "" and flightDest.iloc[x] != flightOrig.iloc[x]
    ])


def write_scene_file(filename):
    with open(filename, 'w') as f:
        for x in range(flights.shape[0]):
            if has_required_data(x):
                scenetext = (
                    f"00:00:00.00>CRE {flightCallSign.iloc[x]} {flightType.iloc[x]} {flightOrig.iloc[x]} 0 "
                    f"FL{int(flightAltitude.iloc[x])} {flightSpeed.iloc[x]}\n"
                    f"00:00:00.00>DEST {flightCallSign.iloc[x]} {flightDest.iloc[x]}\n"
                )
                f.write(scenetext)


if __name__ == "__main__":
    write_scene_file("scenefile.scn")
    sys.exit(main())

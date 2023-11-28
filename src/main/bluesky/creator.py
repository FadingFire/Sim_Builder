import pandas as pd


# temp file setup
# inputfile = "Data/Flights4.csv"
# outputfile = "Data/complete.csv"
# landingsfile = "Data/Landings4.csv"
scenefile = "Data/scenefile.scn"
sort_amount = 50


def parsefiles(inputfile, landingsfile, outputfile):
    from src.main.bluesky.filePreparer import filepreparer
    from src.main.bluesky.merger import process_and_save_data
    # running functions with correct files
    flightsfile, landingfile = filepreparer(inputfile, landingsfile)
    process_and_save_data(flightsfile, landingfile, outputfile)


def airlineslist():
    combined_df = pd.read_csv(outputfile)
    allproviders = combined_df["OPERATOR"]
    providers = allproviders.drop_duplicates(keep="first").astype(str).to_list()
    return providers


def makescene():
    from parser import getdata
    getdata(outputfile, scenefile, sort_amount)


def runall():
    parsefiles()
    airlineslist()
    makescene()


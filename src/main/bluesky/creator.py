import pandas as pd


def parsefiles(inputfile, landingsfile, outputfile):
    from src.main.bluesky.filePreparer import filepreparer
    from src.main.bluesky.merger import process_and_save_data
    # running functions with correct files
    flightsfile, landingfile = filepreparer(inputfile, landingsfile)
    process_and_save_data(flightsfile, landingfile, outputfile)


def airlineslist(outputfile):
    combined_df = pd.read_csv(outputfile)
    allproviders = combined_df["OPERATOR"]
    providers = allproviders.drop_duplicates(keep="first").astype(str).to_list()
    return providers

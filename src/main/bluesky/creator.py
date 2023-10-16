from filePreparer import filepreparer
from merger import process_and_save_data
from parser import getdata

# temp file setup
inputfile = "Data/Flights4.csv"
outputfile = "Data/complete.xlsx"
landingsfile = "Data/Landings4.csv"
scenefile = "Data/scenefile.scn"

# running functions with correct files
flightsfile, landingsfile = filepreparer(inputfile, landingsfile)
completefile = process_and_save_data(flightsfile, landingsfile, outputfile)
getdata(completefile, scenefile)

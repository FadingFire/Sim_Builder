from filePreparer import filepreparer
from merger import process_and_save_data
from parser import getdata

inputfile = "Data/Flights4.csv"
outputfile = "Data/complete.xlsx"
landingsfile = "Data/Landings4.csv"
scenefile = "Data/scenefile.scn"

preparedfile = filepreparer(inputfile, landingsfile)
completefile = process_and_save_data(preparedfile[0], preparedfile[1], outputfile)
getdata(completefile, scenefile)

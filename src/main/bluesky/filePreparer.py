import pandas as pd


def filepreparer(filename, landingsfile):
    info = pd.read_csv(filename, sep=None, engine="python")
    landings = pd.read_csv(landingsfile, sep=None, engine="python")

    # Specify the columns you want to delete
    columns_to_delete = ['STATUS', 'T_UPDATE', 'T0', 'SFPL_ID', 'REGISTRATION', 'WTC', 'CFMU_DELAY', 'CONTROL', 'FPOS_TRACK_ID', 'TIME']

    # Check if each column in 'columns_to_delete' exists in the DataFrame
    for column in columns_to_delete:
        if column in info.columns:
            # If it exists, delete the column
            info.drop(columns=[column], inplace=True)

            # Check if each column in 'columns_to_delete' exists in the DataFrame
    for column in columns_to_delete:
        if column in landings.columns:
            # If it exists, delete the column
            landings.drop(columns=[column], inplace=True)

    # Save the modified DataFrame back to the same CSV file

    info.to_csv(filename, index=False)
    landings.to_csv(landingsfile, index=False)
    return filename, landingsfile



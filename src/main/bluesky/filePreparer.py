import pandas as pd


def filepreparer(filename, landingsfile):
    info = pd.read_csv(filename, sep=None, engine="python")
    landings = pd.read_csv(landingsfile, sep=None, engine="python")

    # Specify the columns you want to delete
    columns_to_delete = ['STATUS', 'T_UPDATE', 'T0', 'SFPL_ID', 'REGISTRATION', 'WTC', 'CFMU_DELAY', 'CONTROL', 'FPOS_TRACK_ID', 'TIME']

    # Remove the specified columns from 'info' DataFrame
    info = info.drop(columns=columns_to_delete, errors='ignore')

    # Remove the specified columns from 'landings' DataFrame
    landings = landings.drop(columns=columns_to_delete, errors='ignore')

    # Save the modified DataFrames back to the same CSV files
    info.to_csv(filename, index=False)
    landings.to_csv(landingsfile, index=False)

    return filename, landingsfile

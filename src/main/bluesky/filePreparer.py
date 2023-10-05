import pandas as pd


def filepreparer(filename):
    # Read the CSV file into the 'flights' DataFrame
    flights = pd.read_csv(filename, delimiter=';')

    # Specify the columns you want to delete
    columns_to_delete = ['STATUS', 'FLIGHT_ID', 'SFPL_ID', 'REGISTRATION', 'SSR', 'FLIGHT_RULES', 'FLIGHT_TYPE', 'WTC', 'NFL', 'XFL', 'CFMU_DELAY', 'CONTROL', 'FPOS_TRACK_ID']

    # Check if each column in 'columns_to_delete' exists in the DataFrame
    for column in columns_to_delete:
        if column in flights.columns:
            # If it exists, delete the column
            flights.drop(columns=[column], inplace=True)

    # Save the modified DataFrame back to the same CSV file
    flights.to_csv(filename, index=False)


filepreparer("Flights4.csv")

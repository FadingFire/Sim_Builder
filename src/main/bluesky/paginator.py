import pandas as pd
from flask import jsonify


def paginate_dataframe(page_size, page_number, sortby, deleteafter, completefile, deleterow, order):
    # Check if the specified column exists in the DataFrame
    df = pd.read_csv(completefile)
    df.fillna(value=pd.NA, inplace=True)

    if sortby in df.columns:
        if order == "asc":
            df = df.sort_values(by=sortby)
        else:
            df = df.sort_values(by=sortby, ascending=False)
    else:
        df = df.sort_values(by="FLIGHT_ID")

    res = df[~(df['Date_Added'] < deleteafter)]
    res = res[~(res['FLIGHT_ID'] == deleterow)]  # Exclude rows with FLIGHT_ID equal to deleterow

    # Save the modified DataFrame to CSV
    res.to_csv(completefile, index=False)

    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    page_data = res.iloc[start_index:end_index]

    # Convert the page_data to CSV
    page_data_csv = page_data.to_csv(index=False)

    return page_data_csv


def editdata(completefile, updated_data):
    df = pd.read_csv(completefile)
    for index, row in df.iterrows():
        if row['FLIGHT_ID'] == updated_data['FLIGHT_ID']:
            # Update the DataFrame with the new data
            df.at[index, 'Operator'] = updated_data['Operator']
            df.at[index, 'ICAOType'] = updated_data['ICAOType']
            df.at[index, 'ADEP'] = updated_data['ADEP']
            df.at[index, 'DEST'] = updated_data['DEST']
            df.at[index, 'TAS'] = updated_data['TAS']
            df.at[index, 'RFL'] = updated_data['RFL']
            df.at[index, 'WeightClass'] = updated_data['WeightClass']
            df.at[index, 'RunWay'] = updated_data['RunWay']
            df.at[index, 'GATE'] = updated_data['GATE']
            df.at[index, 'STACK'] = updated_data['STACK']
            df.to_csv(completefile, index=False)

    return jsonify({'message': 'Row not found'}), 404

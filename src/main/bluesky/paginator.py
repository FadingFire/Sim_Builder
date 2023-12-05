import pandas as pd
from flask import jsonify


def paginate_dataframe(page_size, page_number, sortby, deleteafter, completefile, deleterow, order):
    # Check if the specified column exists in the DataFrame
    df = pd.read_csv(completefile)
    row_count = df.shape[0]
    df.fillna(value=pd.NA, inplace=True)

    if sortby in df.columns:
        if order == "asc":
            df = df.sort_values(by=sortby)
        else:
            df = df.sort_values(by=sortby, ascending=False)
    else:
        df = df.sort_values(by="FLIGHT_ID")

    row_count = row_count / 10
    res = df[~(df['Date_Added'] < deleteafter)]
    res = res[~(res['FLIGHT_ID'] == deleterow)]  # Exclude rows with FLIGHT_ID equal to deleterow

    # Save the modified DataFrame to CSV
    res.to_csv(completefile, index=False)

    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    page_data = res.iloc[start_index:end_index]

    # Convert the page_data to CSV
    page_data_csv = page_data.to_csv(index=False)

    return page_data_csv, row_count


def editdata(completefile, updated_data):
    df = pd.read_csv(completefile)
    for index, row in df.iterrows():
        if str(row['FLIGHT_ID']) == updated_data['FLIGHT_ID']:
            # Update the DataFrame with the new data
            df.at[index, 'CALLSIGN'] = updated_data.get('Callsign', row['CALLSIGN'])
            df.at[index, 'OPERATOR'] = updated_data.get('Operator', row['OPERATOR'])
            df.at[index, 'ICAO_ACTYPE'] = updated_data.get('ICAOType', row['ICAO_ACTYPE'])
            df.at[index, 'ADEP'] = updated_data.get('ADEP', row['ADEP'])
            df.at[index, 'DEST'] = updated_data.get('DEST', row['DEST'])
            df.at[index, 'TAS'] = float(updated_data.get('TAS', row['TAS']))
            df.at[index, 'RFL'] = float(updated_data.get('RFL', row['RFL']))
            df.at[index, 'RUNWAY'] = updated_data.get('RUNWAY', row['RUNWAY'])
            df.at[index, 'GATE'] = updated_data.get('GATE', row['GATE'])
            df.at[index, 'STACK'] = updated_data.get('STACK', row['STACK'])
            df.to_csv(completefile, index=False)

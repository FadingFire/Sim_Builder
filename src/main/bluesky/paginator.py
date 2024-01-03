import pandas as pd
from datetime import date, datetime


def search(regex: str, df, case=False):
    """Search all the text columns of `df`, return rows with any matches."""
    textlikes = df.select_dtypes(include=[object, "string"])
    return df[
        textlikes.apply(
            lambda column: column.str.contains(regex, regex=True, case=case)
        ).any(axis=1)
    ]


def sort(df, sortby: str, order: str):
    df.fillna(value=pd.NA, inplace=True)
    if sortby in df.columns:
        if order == "asc":
            df = df.sort_values(by=sortby)
        else:
            df = df.sort_values(by=sortby, ascending=False)
    else:
        df = df.sort_values(by="FLIGHT_ID")
    return df


def delete(deleteafter, deleterow, completefile):
    df = pd.read_csv(completefile)

    res = df[~(df['Date_Added'] < deleteafter)]
    res = res[~(res['FLIGHT_ID'] == deleterow)]  # Exclude rows with FLIGHT_ID equal to deleterow
    # Save the modified DataFrame to CSV
    res.to_csv(completefile, index=False)


def paginate_dataframe(page_size, page_number, completefile, stored_search_filter, sortby, order, new_search_filter=None):
    # Check if the specified column exists in the DataFrame
    if page_number == 1 or stored_search_filter is not None:
        df = pd.read_csv(completefile)

        # Apply stored search filter if available
        if stored_search_filter:
            df = search(stored_search_filter, df)

        # Apply new search filter if provided
        if new_search_filter:
            df = search(new_search_filter, df)

        # Sort the DataFrame
        df = sort(df, sortby, order)

        row_count = df.shape[0] // 10
    else:
        df = stored_search_filter  # Use the DataFrame from the previous pages

    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    page_data = df.iloc[start_index:end_index]

    # Convert the page_data to CSV
    page_data_csv = page_data.to_csv(index=False)

    return page_data_csv, row_count, new_search_filter


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
            df.at[index, 'FLIGHT_RULES'] = updated_data.get('FLIGHT_RULES', row['FLIGHT_RULES'])
            df.at[index, 'TAS'] = float(updated_data.get('TAS', row['TAS']))
            df.at[index, 'RFL'] = float(updated_data.get('RFL', row['RFL']))
            df.at[index, 'WTC'] = updated_data.get('WeightClass', row['WTC'])
            df.at[index, 'RUNWAY'] = updated_data.get('RUNWAY', row['RUNWAY'])
            df.at[index, 'GATE'] = updated_data.get('GATE', row['GATE'])
            df.at[index, 'STACK'] = updated_data.get('STACK', row['STACK'])
            df.to_csv(completefile, index=False)


def addData(completefile, updated_data):
    idlength = 0
    firsttime = False
    try:
        idlength = pd.read_csv("src/main/bluesky/Data/SAVE/selfmade.csv").shape[0]
    except ValueError:
        pass
    df = pd.read_csv(completefile)

    df2 = pd.DataFrame({
        'FLIGHT_ID': [idlength],
        'CALLSIGN': [updated_data.get('Callsign')],
        'OPERATOR': [updated_data.get('Operator')],
        'ICAO_ACTYPE': [updated_data.get('ICAOType')],
        'ADEP': [updated_data.get('ADEP')],
        'DEST': [updated_data.get('DEST')],
        'FLIGHT_RULES': [updated_data.get('FLIGHT_RULES')],
        'TAS': [updated_data.get('TAS')],
        'RFL': [updated_data.get('RFL')],
        'WTC': [updated_data.get('WeightClass')],
        'T0': [datetime.now().strftime("%#d-%#m-%Y %H:%M:%S")],
        'Date_Added': [date.today()],
        'RUNWAY': [updated_data.get('RunWay')],
        'GATE': [updated_data.get('GATE')],
        'STACK': [updated_data.get('STACK')]
    })
    with open("src/main/bluesky/Data/SAVE/selfmade.csv", 'a') as df1:
        try:
            pd.read_csv("src/main/bluesky/Data/SAVE/selfmade.csv")
        except ValueError:
            df1.write(df2.to_csv(index=False))
            firsttime = True
        if not firsttime:
            df1.write(df2.to_csv(index=False, header=False))
    df = pd.concat([df, df2], ignore_index=True)
    df.to_csv(completefile, index=False)

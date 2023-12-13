import pandas as pd

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
            # ... (update other columns)
            df.to_csv(completefile, index=False)

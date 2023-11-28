import pandas as pd


def paginate_dataframe(page_size, page_number, sortby, deleteafter, completefile):
    # Check if the specified column exists in the DataFrame
    df = pd.read_csv(completefile)
    df.fillna(value=pd.NA, inplace=True)
    if sortby in df.columns:
        full = df.sort_values(by=sortby)
    else:
        full = df.sort_values(by="FLIGHT_ID")
    res = deletefunction(deleteafter, full, completefile)
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    page_data = res.iloc[start_index:end_index]
    # Convert the page_data to CSV
    page_data_csv = page_data.to_csv(index=False)

    return page_data_csv


def deletefunction(deleteafter, full, completefile):
    res = full[~(full['Date_Added'] < deleteafter)]
    res.to_csv(completefile, index=False)
    return res



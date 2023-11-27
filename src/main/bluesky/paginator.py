import pandas as pd

df = pd.read_csv('src/main/bluesky/Data/complete.csv')
df.fillna(value=pd.NA, inplace=True)


def paginate_dataframe(page_size, page_number, sortby):
    # Check if the specified column exists in the DataFrame
    var = "CALLSIGN"
    if sortby in df.columns:
        var = sortby
    full = df.sort_values(by=var)
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    page_data = full.iloc[start_index:end_index]

    # Convert the page_data to CSV (assuming you want CSV format)
    page_data_csv = page_data.to_csv(index=False)

    return page_data_csv


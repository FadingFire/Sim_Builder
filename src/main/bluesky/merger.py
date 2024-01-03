import pandas as pd
from datetime import datetime


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


def insert_avl(root, key):
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert_avl(root.left, key)
    elif key > root.key:
        root.right = insert_avl(root.right, key)
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)
    if balance > 1:
        if key < root.left.key:
            return rotate_right(root)
        else:
            root.left = rotate_left(root.left)
            return rotate_right(root)
    if balance < -1:
        if key > root.right.key:
            return rotate_left(root)
        else:
            root.right = rotate_right(root.right)
            return rotate_left(root)
    return root


def get_height(node):
    if not node:
        return 0
    return node.height


def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)


def rotate_left(z):
    y = z.right
    T2 = y.left
    y.left = z
    z.right = T2
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def process_and_save_data(input_file, landings_file, output_file):
    # Load data from the input CSV file
    df = pd.read_csv(input_file)

    # Create an AVL tree to store unique data
    avl_tree = None

    # Helper function to check if a string is "nan" (case-insensitive)
    def is_nan_string(value):
        return isinstance(value, str) and (value.strip().lower() == "nan" or value.strip().lower() == "zzzz" or value.strip().lower() == "cancelled")

    # Iterate through the input CSV file and insert unique data into the AVL tree
    for index, row in df.iterrows():
        key = (
            int(row["FLIGHT_ID"]), str(row["CALLSIGN"]), str(row["OPERATOR"]), str(row["ICAO_ACTYPE"]), str(row["ADEP"]), str(row["DEST"]), str(row["FLIGHT_RULES"]), str(row["TAS"]), str(row["RFL"]), str(row["WTC"]),  str(row["T0"])
        )
        # Check if any value in the key tuple is "nan" (case-insensitive)
        if not any(is_nan_string(value) for value in key):
            avl_tree = insert_avl(avl_tree, key)

    def inorder_traversal(root, unique_data, callsigns):
        if root:
            inorder_traversal(root.left, unique_data, callsigns)
            key = root.key

            # Check if any value in the key tuple is NaN
            if all(not pd.isna(value) for value in key):
                callsign = key[0]
                if callsign not in callsigns:
                    callsigns.add(callsign)
                    unique_data.append(key)

            inorder_traversal(root.right, unique_data, callsigns)

    # Combine unique data from the AVL tree into a new data frame
    unique_data = []
    callsigns = set()
    inorder_traversal(avl_tree, unique_data, callsigns)

    # Convert the combined unique data into a DataFrame
    combined_df = pd.DataFrame(unique_data, columns=["FLIGHT_ID", "CALLSIGN", "OPERATOR", "ICAO_ACTYPE", "ADEP", "DEST", "FLIGHT_RULES", "TAS", "RFL", "WTC", "T0"])

    # Add the Date_Added column with the current date
    combined_df["Date_Added"] = datetime.now().strftime("%Y-%m-%d")

    # Load additional data from the "AdditionalData.csv" file
    additional_data_df = pd.read_csv(landings_file)

    # Ensure both data frames have the "FLIGHT_ID" column as objects (strings)
    combined_df["FLIGHT_ID"] = combined_df["FLIGHT_ID"].astype(int)
    additional_data_df["FLIGHT_ID"] = additional_data_df["FLIGHT_ID"].astype(int)

    # Merge the additional data based on the FLIGHT_ID column
    combined_df = pd.merge(combined_df, additional_data_df, on="FLIGHT_ID", how="left")

    # Append the new data to the existing "complete.csv" file or create a new one if it doesn't exist
    try:
        existing_df = pd.read_csv(output_file)
        combined_df = pd.concat([existing_df, combined_df])
    except FileNotFoundError:
        pass

    # Save the combined data to "complete.csv"
    combined_df = combined_df.drop_duplicates(subset=["CALLSIGN", "ICAO_ACTYPE", "STACK"], keep='last')
    combined_df = combined_df.sort_values(by="FLIGHT_ID")
    combined_df.to_csv(output_file, index=False)
    return output_file

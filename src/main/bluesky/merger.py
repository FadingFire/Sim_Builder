import pandas as pd


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


# Load data from the first Excel file
file1 = "Flights.csv"
df1 = pd.read_csv(file1)

# Load data from the second Excel file
file2 = "Flights2.csv"
df2 = pd.read_csv(file2)

# Create AVL trees to store unique data from both files
avl_tree1 = None
avl_tree2 = None


# Iterate through the first Excel file and insert unique data into AVL tree 1
for index, row in df1.iterrows():
    key = (
        str(row["CALLSIGN"]), str(row["OPERATOR"]), str(row["ICAO_ACTYPE"]),
        str(row["ADEP"]), str(row["DEST"]), str(row["TAS"]), str(row["RFL"]), str(row["TYPE_OF_TRANSPONDER"]), str(row["T0"]), str(row["T_UPDATE"])
    )
    avl_tree1 = insert_avl(avl_tree1, key)


# Iterate through the second Excel file and insert unique data into AVL tree 2
for index, row in df2.iterrows():
    key = (
        str(row["CALLSIGN"]), str(row["OPERATOR"]), str(row["ICAO_ACTYPE"]),
        str(row["ADEP"]), str(row["DEST"]), str(row["TAS"]), str(row["RFL"]), str(row["TYPE_OF_TRANSPONDER"]), str(row["T0"]), str(row["T_UPDATE"])
    )
    avl_tree2 = insert_avl(avl_tree2, key)

# Combine unique data from both AVL trees into a new data frame
unique_data = []


def inorder_traversal(root, unique_data):
    if root:
        inorder_traversal(root.left, unique_data)
        unique_data.append(root.key)
        inorder_traversal(root.right, unique_data)


inorder_traversal(avl_tree1, unique_data)
inorder_traversal(avl_tree2, unique_data)

# Convert the combined unique data into a DataFrame
combined_df = pd.DataFrame(unique_data, columns=["CALLSIGN", "OPERATOR", "ICAO_ACTYPE", "ADEP", "DEST", "TAS", "RFL", "TYPE_OF_TRANSPONDER", "T0", "T_UPDATE"])
combined_df.to_excel('complete.xlsx')

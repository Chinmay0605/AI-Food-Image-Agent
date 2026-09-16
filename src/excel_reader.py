import pandas as pd


def read_food_items(file_path):
    df = pd.read_excel(file_path)

    if "Food Item" in df.columns:
        column = "Food Item"

    elif "item_name" in df.columns:
        column = "item_name"

    else:
        raise ValueError(
            "Excel file must contain either "
            "'Food Item' or 'item_name' column."
        )

    items = (
        df[column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    items = items[items != ""]
    items = items.drop_duplicates()

    return items.tolist()
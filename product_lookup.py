import pandas as pd

data = pd.read_csv("product.csv")

def get_product_details(class_name):
    rows = data[data["class_name"] == class_name]
    if rows.empty:
        return None
    return rows.sample(1).to_dict(orient="records")[0]

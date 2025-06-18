import pandas as pd

# Load CSVs
fats = pd.read_csv("data/fats.csv")
carbs = pd.read_csv("data/carbs.csv")
proteins = pd.read_csv("data/proteins.csv")

def get_macro_info(ingredient: str):
    ingredient = ingredient.lower()
    source = "context"

    for df, macro in [(fats, "fat"), (carbs, "carbs"), (proteins, "protein")]:
        match = df[df['Ingredient'].str.lower() == ingredient]
        if not match.empty:
            row = match.iloc[0].to_dict()
            return row, macro, source

    return None, None, "online"

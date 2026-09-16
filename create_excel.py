import pandas as pd

data = {
    "Food Item": [
        "Paneer Butter Masala",
        "Dal Tadka",
        "Veg Biryani",
        "Butter Naan",
        "Chicken Tikka"
    ]
}

df = pd.DataFrame(data)

df.to_excel(
    "data/food_items.xlsx",
    index=False
)

print("food_items.xlsx created successfully!")

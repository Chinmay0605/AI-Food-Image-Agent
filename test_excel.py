from src.excel_reader import read_food_items


file_path = "data/food_items.xlsx"

items = read_food_items(file_path)

print("\nFood Items Found:")
print("-" * 30)

for i, item in enumerate(items, start=1):
    print(f"{i}. {item}")

print("-" * 30)
print(f"Total items: {len(items)}")
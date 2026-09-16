from src.image_search import search_images


food = "Paneer Butter Masala"

results = search_images(food)

print("\nImage Search Results")
print("=" * 60)

print(f"Food Item: {food}")
print(f"Images Found: {len(results)}")

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("Title:", result["title"])
    print("Image URL:", result["image_url"])
    print("Source:", result["source"])
    print("Source URL:", result["source_url"])
    print(
        "Dimensions:",
        result["width"],
        "x",
        result["height"]
    )
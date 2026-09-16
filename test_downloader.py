from src.image_search import search_images
from src.image_downloader import download_candidates


food = "Paneer Butter Masala"

print("\nSearching images...")
print("=" * 50)

results = search_images(
    food,
    limit=5
)

print(
    f"Images found: {len(results)}"
)

print("\nDownloading images...")
print("=" * 50)

downloaded = download_candidates(
    food,
    results
)

print("\nDownload Complete")
print("=" * 50)

print(
    f"Images downloaded: {len(downloaded)}"
)

for image in downloaded:
    print(
        image["path"]
    )
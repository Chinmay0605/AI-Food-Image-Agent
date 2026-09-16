import os

import serpapi
from dotenv import load_dotenv


load_dotenv()


def search_images(food_item, limit=5):

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        raise ValueError(
            "SERPAPI_KEY is missing from the .env file."
        )

    client = serpapi.Client(
        api_key=api_key
    )

    query = f"{food_item} Indian restaurant food"

    results = client.search(
        {
            "engine": "google_images",
            "q": query,
            "hl": "en",
            "gl": "in",
        }
    )

    images = results.get(
        "images_results",
        results.get("image_results", [])
    )

    candidates = []

    for image in images[:limit]:

        image_url = image.get("original")

        if not image_url:
            continue

        candidates.append(
            {
                "title": image.get("title", ""),
                "image_url": image_url,
                "source_url": image.get("link", ""),
                "source": image.get("source", ""),
                "width": image.get("original_width"),
                "height": image.get("original_height"),
            }
        )

    return candidates
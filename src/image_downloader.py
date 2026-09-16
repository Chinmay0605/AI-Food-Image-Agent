import os
import requests


def download_image(image_url, save_path):
    try:
        response = requests.get(
            image_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        if "image" not in content_type:
            return False

        with open(save_path, "wb") as file:
            file.write(response.content)

        return True

    except Exception as e:
        print("Download failed:", e)
        return False


def download_candidates(food_item, candidates):

    folder = os.path.join(
        "downloads",
        food_item
    )

    os.makedirs(
        folder,
        exist_ok=True
    )

    downloaded = []

    for i, candidate in enumerate(
        candidates,
        start=1
    ):

        image_url = candidate.get(
            "image_url"
        )

        if not image_url:
            continue

        file_path = os.path.join(
            folder,
            f"candidate_{i}.jpg"
        )

        success = download_image(
            image_url,
            file_path
        )

        if success:

            downloaded.append(
                {
                    "path": file_path,
                    "title": candidate.get(
                        "title",
                        ""
                    ),
                    "source_url": candidate.get(
                        "source_url",
                        ""
                    ),
                    "width": candidate.get(
                        "width"
                    ),
                    "height": candidate.get(
                        "height"
                    )
                }
            )

            print(
                f"Downloaded candidate {i}"
            )

    return downloaded
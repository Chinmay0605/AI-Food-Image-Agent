import os

from excel_reader import read_food_items
from image_search import search_images
from image_downloader import download_candidates
from image_validator import validate_image
from ai_selector import select_best_image
from image_processor import process_image
from drive_uploader import upload_file
from report import generate_report


EXCEL_FILE = "data/food_items.xlsx"


def process_food_item(food_item):

    print("\n" + "=" * 60)
    print(f"PROCESSING: {food_item}")
    print("=" * 60)

    try:

        # --------------------------------------------------
        # 1. Search images
        # --------------------------------------------------

        print("\nSearching images...")

        candidates = search_images(
            food_item,
            limit=5
        )

        if not candidates:
            raise Exception(
                "No image candidates found."
            )

        print(
            f"Found {len(candidates)} candidates."
        )

        # --------------------------------------------------
        # 2. Download image candidates
        # --------------------------------------------------

        print("\nDownloading images...")

        downloaded = download_candidates(
            food_item,
            candidates
        )

        if not downloaded:
            raise Exception(
                "No images could be downloaded."
            )

        print(
            f"Downloaded {len(downloaded)} images."
        )

        # --------------------------------------------------
        # 3. Validate downloaded images
        # --------------------------------------------------

        print("\nValidating images...")

        valid_images = []

        for image in downloaded:

            validation = validate_image(
                image["path"]
            )

            if validation["valid"]:

                valid_images.append(
                    image["path"]
                )

                print(
                    f"✓ Valid: {image['path']}"
                )

            else:

                print(
                    f"✗ Rejected: {image['path']}"
                )

                if validation["issues"]:

                    print(
                        "  Issues:",
                        ", ".join(
                            validation["issues"]
                        )
                    )

        if not valid_images:

            raise Exception(
                "No valid images available."
            )

        # --------------------------------------------------
        # 4. Gemini AI image selection
        # --------------------------------------------------

        print(
            "\nGemini AI selecting best image..."
        )

        selection = select_best_image(
            food_item,
            valid_images
        )

        if not selection:

            raise Exception(
                "AI image selection failed."
            )

        selected_path = selection["best_path"]

        print(
            "✓ Selected:",
            selected_path
        )

        print(
            "Confidence:",
            selection["confidence"]
        )

        print(
            "Reason:",
            selection["reason"]
        )

        # --------------------------------------------------
        # 5. Process selected image
        # --------------------------------------------------

        print("\nProcessing final image...")

        processed = process_image(
            selected_path,
            food_item
        )

        if not processed["success"]:

            raise Exception(
                processed.get(
                    "error",
                    "Image processing failed."
                )
            )

        print(
            f"✓ Dimensions: "
            f"{processed['width']} x "
            f"{processed['height']}"
        )

        print(
            f"✓ Size: "
            f"{processed['size_mb']} MB"
        )

        # --------------------------------------------------
        # 6. Upload processed image to Google Drive
        # --------------------------------------------------

        print(
            "\nUploading to Google Drive..."
        )

        uploaded = upload_file(
            processed["path"],
            f"{food_item}.jpg"
        )

        print(
            "✓ Uploaded successfully!"
        )

        print(
            "Drive URL:",
            uploaded["url"]
        )

        # --------------------------------------------------
        # 7. Return successful result
        # --------------------------------------------------

        return {
            "success": True,
            "food_item": food_item,
            "selected_image": selected_path,
            "processed_path": processed["path"],
            "width": processed["width"],
            "height": processed["height"],
            "size_mb": processed["size_mb"],
            "confidence": selection["confidence"],
            "reason": selection["reason"],
            "drive_url": uploaded["url"]
        }

    except Exception as e:

        print(
            f"\n✗ FAILED: {food_item}"
        )

        print(
            "Error:",
            str(e)
        )

        # Return failure information
        # instead of stopping the complete agent

        return {
            "success": False,
            "food_item": food_item,
            "selected_image": "",
            "processed_path": "",
            "width": 0,
            "height": 0,
            "size_mb": 0,
            "confidence": 0,
            "reason": "",
            "drive_url": "",
            "error": str(e)
        }


def main():

    print("=" * 60)
    print("AI FOOD IMAGE AGENT")
    print("=" * 60)

    # ------------------------------------------------------
    # 1. Read food items from Excel
    # ------------------------------------------------------

    try:

        food_items = read_food_items(
            EXCEL_FILE
        )

    except Exception as e:

        print(
            "\nCould not read Excel file:"
        )

        print(
            str(e)
        )

        return

    print(
        f"\nFound {len(food_items)} food items."
    )

    # ------------------------------------------------------
    # 2. Process every food item
    # ------------------------------------------------------

    results = []

    for food_item in food_items:

        result = process_food_item(
            food_item
        )

        results.append(
            result
        )

    # ------------------------------------------------------
    # 3. Calculate final summary
    # ------------------------------------------------------

    successful = [
        result
        for result in results
        if result["success"]
    ]

    failed = [
        result
        for result in results
        if not result["success"]
    ]

    # ------------------------------------------------------
    # 4. Print processing summary
    # ------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)

    for result in successful:

        print(
            f"✓ {result['food_item']}"
        )

    for result in failed:

        print(
            f"✗ {result['food_item']} "
            f"-> {result.get('error', 'Unknown error')}"
        )

    print("\n")

    print(
        "Successful:",
        len(successful)
    )

    print(
        "Failed:",
        len(failed)
    )

    print(
        "Total:",
        len(results)
    )

    # ------------------------------------------------------
    # 5. Generate processing report
    # ------------------------------------------------------

    try:

        report_file = generate_report(
            results
        )

        print(
            "\n✓ Processing report created:"
        )

        print(
            report_file
        )

    except Exception as e:

        print(
            "\n✗ Could not create processing report:"
        )

        print(
            str(e)
        )

    # ------------------------------------------------------
    # 6. Finish
    # ------------------------------------------------------

    print(
        "\nAgent finished."
    )


if __name__ == "__main__":

    main()
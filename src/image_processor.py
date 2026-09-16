import os

from PIL import Image, ImageOps


TARGET_WIDTH = 1800
TARGET_HEIGHT = 1200
MAX_SIZE_MB = 10


def process_image(
    input_path,
    food_item
):

    os.makedirs(
        "processed",
        exist_ok=True
    )

    output_path = os.path.join(
        "processed",
        f"{food_item}.jpg"
    )

    try:

        image = Image.open(
            input_path
        )

        # Convert to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Crop to 3:2 while keeping the
        # important center area
        image = ImageOps.fit(
            image,
            (
                TARGET_WIDTH,
                TARGET_HEIGHT
            ),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )

        # Save high-quality JPEG
        quality = 95

        image.save(
            output_path,
            "JPEG",
            quality=quality,
            optimize=True
        )

        # Reduce quality if file is > 10 MB
        while (
            os.path.getsize(output_path)
            > MAX_SIZE_MB * 1024 * 1024
            and quality > 50
        ):

            quality -= 5

            image.save(
                output_path,
                "JPEG",
                quality=quality,
                optimize=True
            )

        # Final verification
        final_image = Image.open(
            output_path
        )

        width, height = final_image.size

        size_mb = (
            os.path.getsize(output_path)
            / (1024 * 1024)
        )

        if (
            width != TARGET_WIDTH
            or height != TARGET_HEIGHT
        ):
            raise ValueError(
                "Final image dimensions are incorrect."
            )

        if size_mb > MAX_SIZE_MB:
            raise ValueError(
                "Final image is larger than 10 MB."
            )

        return {
            "success": True,
            "path": output_path,
            "width": width,
            "height": height,
            "size_mb": round(
                size_mb,
                2
            ),
            "quality": quality
        }

    except Exception as e:

        return {
            "success": False,
            "path": None,
            "width": 0,
            "height": 0,
            "size_mb": 0,
            "quality": 0,
            "error": str(e)
        }
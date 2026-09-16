import os

import cv2
from PIL import Image


def validate_image(image_path):
    result = {
        "path": image_path,
        "valid": False,
        "width": 0,
        "height": 0,
        "file_size_mb": 0,
        "blur_score": 0,
        "issues": []
    }

    try:
        # Check file exists
        if not os.path.exists(image_path):
            result["issues"].append(
                "File does not exist"
            )
            return result

        # File size
        file_size = os.path.getsize(
            image_path
        )

        result["file_size_mb"] = round(
            file_size / (1024 * 1024),
            2
        )

        # Open image
        image = Image.open(
            image_path
        )

        width, height = image.size

        result["width"] = width
        result["height"] = height

        # Minimum resolution
        if width < 800 or height < 600:
            result["issues"].append(
                "Low resolution"
            )

        # File size check
        if result["file_size_mb"] > 10:
            result["issues"].append(
                "File larger than 10 MB"
            )

        # Open with OpenCV
        img = cv2.imread(
            image_path
        )

        if img is None:
            result["issues"].append(
                "Unable to read image"
            )
            return result

        # Convert to grayscale
        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        # Blur detection
        blur_score = cv2.Laplacian(
            gray,
            cv2.CV_64F
        ).var()

        result["blur_score"] = round(
            blur_score,
            2
        )

        if blur_score < 100:
            result["issues"].append(
                "Image may be blurry"
            )

        # Aspect ratio
        ratio = width / height

        if ratio < 0.5 or ratio > 2.0:
            result["issues"].append(
                "Unusual aspect ratio"
            )

        # Final decision
        if not result["issues"]:
            result["valid"] = True

        return result

    except Exception as e:

        result["issues"].append(
            str(e)
        )

        return result
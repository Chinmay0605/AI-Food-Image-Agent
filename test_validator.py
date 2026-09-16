import os

from src.image_validator import validate_image


folder = "downloads/Paneer Butter Masala"


files = [
    os.path.join(folder, file)
    for file in os.listdir(folder)
    if file.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
]


print("\nImage Quality Validation")
print("=" * 60)


for file in files:

    result = validate_image(file)

    print("\nFile:", file)

    print(
        "Resolution:",
        result["width"],
        "x",
        result["height"]
    )

    print(
        "Size:",
        result["file_size_mb"],
        "MB"
    )

    print(
        "Blur Score:",
        result["blur_score"]
    )

    print(
        "Valid:",
        result["valid"]
    )

    print(
        "Issues:",
        result["issues"]
    )
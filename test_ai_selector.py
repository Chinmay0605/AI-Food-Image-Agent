import os

from src.ai_selector import select_best_image


folder = "downloads/Paneer Butter Masala"


image_paths = [
    os.path.join(
        folder,
        file
    )
    for file in os.listdir(folder)
    if file.lower().endswith(
        (".jpg", ".jpeg", ".png")
    )
]


print("\nAI Image Selection")
print("=" * 60)

print(
    f"Food Item: Paneer Butter Masala"
)

print(
    f"Candidates: {len(image_paths)}"
)

print("\nSending images to Gemini...")


result = select_best_image(
    "Paneer Butter Masala",
    image_paths
)


print("\nAI Selection Result")
print("=" * 60)


if result:

    print(
        "Best Image:",
        result["best_image"]
    )

    print(
        "Best Path:",
        result["best_path"]
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "Reason:",
        result["reason"]
    )

else:

    print(
        "No image was selected."
    )
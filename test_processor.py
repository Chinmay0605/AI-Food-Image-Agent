from src.image_processor import process_image


input_image = (
    "downloads/"
    "Paneer Butter Masala/"
    "candidate_2.jpg"
)


result = process_image(
    input_image,
    "Paneer Butter Masala"
)


print("\nImage Processing Result")
print("=" * 60)


print(
    "Success:",
    result["success"]
)

print(
    "Output:",
    result["path"]
)

print(
    "Resolution:",
    result["width"],
    "x",
    result["height"]
)

print(
    "Size:",
    result["size_mb"],
    "MB"
)

print(
    "JPEG Quality:",
    result["quality"]
)


if not result["success"]:

    print(
        "Error:",
        result["error"]
    )
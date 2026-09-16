from src.drive_uploader import upload_file


file_path = "processed/Butter Naan.jpg"


result = upload_file(
    file_path,
    "Butter Naan.jpg"
)


print("\nUPLOAD SUCCESSFUL!")
print("File name:", result["name"])
print("File ID:", result["id"])
print("Drive URL:", result["url"])
import os
import shutil

downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")

file_types = {
    "Images": [".jpg", ".jpeg", ".gif", ".gif"],
    "PDFs": [".pdf"],
    "Installers": [".exe", ".msi"],
    "Code Files": [".py", ".html", ".css", ".js"],
    "Music": [".mp3"],
    "Videos": [".mp4"]
}

for filename in os.listdir(downloads_path):
    file_path = os.path.join(downloads_path, filename)
    if os.path.isfile(file_path):
        ext = os.path.splitext(filename)[1].lower()

        for folder_name, extensions in file_types.items():
            if ext in extensions:
                target_folder = os.path.join(downloads_path, folder_name)
                os.makedirs(target_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(target_folder, filename))
                break

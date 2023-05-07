import os
import re
import shutil
import unicodedata
from pathlib import Path
import sys
import zipfile


def normalize(text):
    """Normalize a string, converting Cyrillic characters to Latin and removing all non-alphanumeric characters."""
    # Convert Cyrillic characters to Latin using NFKD Unicode normalisation
    text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8')
    # Replace all non-alphanumeric characters with '_'
    text = re.sub(r'[\W_]+', '_', text)
    return text


folder = r'C:\Users\67400\OneDrive\Рабочий стол\Anything'

for dirpath, dirnames, filenames in os.walk(folder, topdown=False):
    for dirname in dirnames:
        full_path = os.path.join(dirpath, dirname)
        if not os.listdir(full_path):
            os.rmdir(full_path)


def sort_files(path):
    """Sort files in a directory tree by their extension."""
    # Define file extensions for each category
    image_extensions = ('JPEG', 'JPG', 'PNG', 'SVG')
    video_extensions = ('AVI', 'MP4', 'MOV', 'MKV')
    document_extensions = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    music_extensions = ('MP3', 'OGG', 'WAV', 'AMR')
    archive_extensions = ('ZIP', 'GZ', 'TAR')

    # Define categories and their extensions
    categories = {
        'Images': image_extensions,
        'Videos': video_extensions,
        'Documents': document_extensions,
        'Music': music_extensions,
        'Archives': archive_extensions
    }

    # Create dictionaries to store the files for each category
    images = {}
    videos = {}
    documents = {}
    music = {}
    archives = {}
    unknown = {}

    # Create directories for each category
    for category in categories:
        category_path = os.path.join(path, category)
        os.makedirs(category_path, exist_ok=True)

    # Walk through the directory tree
    for root, dirs, files in os.walk(path):
        for file in files:
            # Get the file extension and normalize the file name
            ext = os.path.splitext(file)[-1][1:].upper()
            name = normalize(file)

            # Find the appropriate category for the file
            file_category = 'Unknown'
            for category, extensions in categories.items():
                if ext in extensions:
                    file_category = category
                    break

            # Move the file to the category directory
            src_file = os.path.join(root, file)
            dest_file = os.path.join(path, file_category, file)
            shutil.move(src_file, dest_file)

            try:
                file_path = src_file
                shutil.unpack_archive(file_path, os.path.join(
                    path, 'Archives', name))  # Розпакування
                os.remove(file_path)  # Видалення архіву
            except Exception as e:
                print(f"Failed to unpack or remove archive: {file_path}")
                print(f"Error: {e}")
                archives[name] = src_file

            # Categorize the file by its extension
            if ext in image_extensions:
                if 'Images' not in images:
                    images['Images'] = []
                images['Images'].append(os.path.join(root, file))
            elif ext in video_extensions:
                if 'Videos' not in videos:
                    videos['Videos'] = []
                videos['Videos'].append(os.path.join(root, file))
            elif ext in document_extensions:
                if 'Documents' not in documents:
                    documents['Documents'] = []
                documents['Documents'].append(os.path.join(root, file))
            elif ext in music_extensions:
                if 'Music' not in music:
                    music['Music'] = []
                music['Music'].append(os.path.join(root, file))
            elif ext in archive_extensions:
                if 'Archives' not in archives:
                    archives['Archives'] = []
                archives['Archives'].append(os.path.join(root, file))
            else:
                if 'Unknown' not in unknown:
                    unknown['Unknown'] = []
                unknown['Unknown'].append(os.path.join(root, file))

            # Rename the file
            new_name = os.path.join(root, normalize(
                os.path.splitext(file)[0]) + '.' + ext.lower())
            if new_name != os.path.join(root, file):
                print("new_name is not equal to os.path.join(root, file)")


def main():
    """
    тут шлях до папки яку треба сортувати. працюй з цією змінною аж доки не відлагодиш весь скрипт. запускай просто кнопкою run чи ctrl+f5

    """
    path = r'C:\Users\67400\OneDrive\Рабочий стол\Anything'

    """
    коли відпрацюшь усе, закоментуєш змінну в рядку 83 і розкоментуєш рядок 88
    """
    # path = Path(sys.argv[1])

    sort_files(path)  # запускає сам скрипт сортування

    pass


if __name__ == "__main__":
    main()

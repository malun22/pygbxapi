import re
import string
import os
import random
import pathlib
import shutil
import io

from werkzeug.datastructures import FileStorage
from flask import current_app
from zipfile import ZipFile, ZIP_DEFLATED
from typing import List


class FileHelper:
    @staticmethod
    def get_folder_size(folder_path: str) -> int:
        size = 0

        for path, _, files in os.walk(folder_path):
            for f in files:
                fp = os.path.join(path, f)
                size += os.path.getsize(fp)

        return size

    @staticmethod
    def get_file_size(filepath: str) -> int:
        return os.path.getsize(filepath)

    @staticmethod
    def move_file(filepath: str, destination: str) -> str:
        filename = FileHelper.get_filename_from_path(filepath)
        destination = os.path.join(destination, filename)
        shutil.move(filepath, destination)

        return destination

    @staticmethod
    def file_exists(filepath: str) -> bool:
        return os.path.exists(filepath)

    @staticmethod
    def has_type(filename: str, ending: str) -> bool:
        return filename.lower().endswith(ending)

    @staticmethod
    def get_filename_from_path(filepath: str, extension: bool = True) -> str:
        """Returns the filename and extension from a given path"""
        path_object = pathlib.Path(filepath)

        if extension:
            return f"{path_object.stem}{path_object.suffix}"
        else:
            return f"{path_object.stem}"

    @staticmethod
    def get_path_from_filepath(filepath: str) -> str:
        """Returns the path of the folder of the filepath"""
        path_object = pathlib.Path(filepath)

        return path_object.parent

    @staticmethod
    def zip_file(filepath: str, delete_original: bool = False) -> str:
        """Zips the file and returns the filepath to the zip file"""
        path = FileHelper.get_path_from_filepath(filepath)
        filename_wo_suffix = FileHelper.get_filename_from_path(
            filepath=filepath, extension=False
        )
        filename_w_suffix = FileHelper.get_filename_from_path(
            filepath=filepath)
        zip_path = os.path.join(path, filename_wo_suffix)

        zip_path += ".zip"
        with ZipFile(zip_path, "w", ZIP_DEFLATED) as zip:
            zip.write(filepath, arcname=filename_w_suffix)

        if delete_original:
            FileHelper.delete_file(filepath)

        return zip_path

    @staticmethod
    def rename_file(filepath: str, name: str) -> str:
        path = FileHelper.get_path_from_filepath(filepath)

        new_filepath = os.path.join(path, name)

        os.rename(filepath, new_filepath)

        return new_filepath

    @staticmethod
    def create_return_data(filepath: str, delete_original: bool = False) -> io.BytesIO:
        return_data = io.BytesIO()
        with open(filepath, "rb") as fo:
            return_data.write(fo.read())

        return_data.seek(0)

        if delete_original:
            FileHelper.delete_file(filepath)

        return return_data

    @staticmethod
    def unzip_file(zip_file: str, delete_after: bool) -> str:
        unzipped_files = FileHelper.unzip_files(zip_file, delete_after)

        if len(unzipped_files) > 0:
            return unzipped_files[0]

        return False

    @staticmethod
    def unzip_files(zip_file: str, delete_after: bool) -> List[str]:
        """Unzips a zip file and stores it in the same directory"""
        path = FileHelper.get_path_from_filepath(zip_file)

        filenames: List[str] = []

        with ZipFile(zip_file, "r") as zip:
            for name in zip.namelist():
                zip.extract(name, path)
                filenames.append(os.path.join(path, name))

        if delete_after:
            FileHelper.delete_file(zip_file)

        return filenames

    @staticmethod
    def save_temp_file(file: FileStorage) -> str:
        file_extension = pathlib.Path(file.filename).suffix

        filepath = FileHelper.__generate_temp_path(
            location=current_app.config["TEMP_UPLOAD_FOLDER"],
            len=20,
            file_extension=file_extension,
        )
        while os.path.exists(filepath):
            filepath = FileHelper.__generate_temp_path(
                location=current_app.config["TEMP_UPLOAD_FOLDER"],
                len=20,
                file_extension=file_extension,
            )

        file.save(filepath)

        return filepath

    @staticmethod
    def _get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall("filename=(.+)", cd)
        if len(fname) == 0:
            return None
        return fname[0]

    @staticmethod
    def delete_file(filepath: str):
        os.remove(filepath)

    @staticmethod
    def __generate_random_string(len: int) -> str:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=len))

    @staticmethod
    def __generate_random_file_name(len: int, file_extension: str) -> str:
        return f"{FileHelper.__generate_random_string(len=len)}{file_extension}"

    @staticmethod
    def __generate_temp_path(location: str, len: int, file_extension: str) -> str:
        filename = FileHelper.__generate_random_file_name(
            len=len, file_extension=file_extension
        )
        return os.path.join(location, filename)

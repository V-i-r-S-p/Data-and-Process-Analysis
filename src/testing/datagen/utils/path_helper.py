import os
import sys
from os.path import join
from pathlib import Path
from typing import Union, List, Optional, Callable
import shutil

class PathHelper:
    @staticmethod
    def path(*path_parts: str) -> str:
        joined_path = Path(*path_parts)
        return str(joined_path.resolve().absolute())

    @staticmethod
    def create_dir(path_to_dir: str) -> None:
        normalized_path = PathHelper.path(path_to_dir)
        Path(normalized_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def parse_file_paths(path_to_root: str) -> Union[List[str], None]:
        paths = []
        normalized_root = PathHelper.path(path_to_root)

        try:
            for root, dirs, files in os.walk(normalized_root):
                for file in files:
                    file_path = join(root, file)
                    if Path(file_path).exists():
                        paths.append(PathHelper.path(file_path))
            return paths
        except OSError as e:
            print(f"Error scanning directory {normalized_root}: {e}", file=sys.stderr)
            return None

    @staticmethod
    def filename(file_path: str, suffix: bool = True) -> str:
        normalized_path = PathHelper.path(file_path)
        path_obj = Path(normalized_path)
        return path_obj.name if suffix else path_obj.stem

    @staticmethod
    def parent_dir(file_path: str) -> str:
        normalized_path = PathHelper.path(file_path)
        path_obj = Path(normalized_path)
        return path_obj.parent.name

    @staticmethod
    def flatten_directory(
        source_dir: str,
        target_dir: str,
        name_generator: Optional[Callable[[str], str]] = None
    ) -> None:
        PathHelper.create_dir(target_dir)

        def default_name_generator(file_path: str) -> str:
            rel_path = os.path.relpath(file_path, source_dir)
            return rel_path.replace(os.sep, '_')

        name_func = name_generator or default_name_generator

        for root, dirs, files in os.walk(PathHelper.path(source_dir)):
            for file in files:
                src_path = PathHelper.path(root, file)
                new_name = name_func(src_path)
                dst_path = PathHelper.path(target_dir, new_name)
                shutil.copy2(src_path, dst_path)
                # print(f"Скопировано: {src_path} -> {dst_path}")

    @staticmethod
    def find_nearest_folder(path: Union[str, os.PathLike]) -> str:
        abs_path = os.path.abspath(path)

        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Path does not exist: {abs_path}")

        if os.path.isdir(abs_path):
            return abs_path

        parent_dir = os.path.dirname(abs_path)

        if not os.path.isdir(parent_dir):
            raise NotADirectoryError(f"Parent directory does not exist: {parent_dir}")

        return parent_dir
    
    @staticmethod
    def exists(path: Union[str, os.PathLike]) -> bool:
        return os.path.exists(path)

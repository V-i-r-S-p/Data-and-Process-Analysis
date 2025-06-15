import os
from os.path import isdir, join
from pathlib import Path, PureWindowsPath

class file_path_finder:
  
  def parse_file_paths(path_to_root: str) -> list[str] | None:
    paths = []

    try:
      for root, dirs, files in os.walk(path_to_root):
        for file in files:
          file_path = join(root, file)
          if Path(file_path).exists():
            paths.append(file_path_finder.path(file_path))
    except (FileNotFoundError or FileExistsError) as e:
      print(e)
      paths = None

    return paths

  def path(file_path: str) -> str:
    return PureWindowsPath(file_path).as_posix()

  def filename(file_path: str, suffix=True) -> str:
    if suffix:
      return PureWindowsPath(file_path).name
    else:
      return PureWindowsPath(file_path).stem

import os
from pathlib import Path, PureWindowsPath


from composition import *


def mk_dir(path: str, *paths: list[str]) -> str:
  path_ = os.path.join(path, *paths)
  if not os.path.exists(path_):
    os.mkdir(path_)

  return path_

def main(data_root: str):
  build_path = mk_dir(data_root, '..', 'build')
  composition = compose_data(data_root)
  check_uniq(composition)
  render_png(build_path, composition)

  doc_path = os.path.join(data_root, '..', 'checklist.tex')
  create_doc_from_composition(doc_path, composition)


main('./src/testing/datagen/data')

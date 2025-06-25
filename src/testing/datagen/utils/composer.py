from .path_helper import *
from .data_parser import *
from .data2tex import *
from .tex2img import *
from .img_effects import *


def compose_data(data_root: str) -> dict[str: dict[str: str]]:
  files = PathHelper.parse_file_paths(data_root)

  composition = dict()
  for file in files:
    filename = PathHelper.filename(file, False)
    data = data_parser(file)

    counter = 0
    buf = dict()
    for data_ in data:
      name_data = f'{filename}_{counter}'
      counter += 1
      buf[name_data] = data_

    composition[filename] = buf

  return composition


def create_tex(build_path: str, composition: dict[str: dict[str: str]]):
  for k, v in composition.items():
    dir_path = PathHelper.path(build_path, k)
    PathHelper.create_dir(dir_path)
    for name_data, data in v.items():
      out_file_path = PathHelper.path(dir_path, f'{name_data}.tex')
      tex = data

      with open(out_file_path, 'w', encoding='utf8') as file:
        file.write(tex)

def create_img(build_path: str, composition: dict[str: dict[str: str]]):
  for k, v in composition.items():
    dir_path = PathHelper.path(build_path, k)
    PathHelper.create_dir(dir_path)
    for name_data, data in v.items():
      out_file_path = PathHelper.path(dir_path, name_data)
      tex = data2tex(data)

      if tex2img(tex, out_file_path):
        return


def create_doc(doc_path: str, composition: dict[str: dict[str: str]]):
  with open(doc_path, 'w', encoding='utf8') as file:
    text = ''
    for k, v in composition.items():
      cases = ''
      for data_name, data in v.items():
        data_math = tex_math(data)

        data_name = str(data_name).replace('_', r'\_')
        cases += r'''
        %s & %s & %s \\
        \hline
        ''' % (data_name, data_math, tex_verbatim(data))

      text += tex_longtable(cases, '|l|c|p{5cm}|', k, 'Name', r'Case(math)', r'LaTeX')

    text = tex_center(text)
    text = tex_title(text, 'checklist')
    text = tex_document(text)
    text = tex_package(text)

    file.write(text)


class Composer:
  root_dir: str
  middleware: dict
  def __init__(self, root_dir):
    self.root_dir = root_dir
    self.middleware = dict()


  def create_base_data(self, data_path, latex_path, img_path, checklist_path):
    composition = compose_data(PathHelper.path(self.root_dir, data_path))
    create_tex(PathHelper.path(self.root_dir, latex_path), composition)
    create_img(PathHelper.path(self.root_dir, img_path), composition)
    create_doc(PathHelper.path(self.root_dir, checklist_path), composition)

  def add_to_middleware(self, postfix: str, fn):
    self.middleware[postfix] = fn

  def create_data_from_middleware(self, img_path, effect_path):
    effect_dir = PathHelper.path(self.root_dir, effect_path)
    PathHelper.create_dir(effect_dir)
    files = PathHelper.parse_file_paths(PathHelper.path(self.root_dir, img_path))
    for file in files:
      filename = PathHelper.filename(file)
      dirname = PathHelper.parent_dir(file)
      for postfix, fn in self.middleware.items():
        # i = filename.rindex('.')
        # filename = filename[:i] + f'_{postfix}' + filename[i:]
        dir_ = PathHelper.path(effect_dir, postfix, dirname)
        PathHelper.create_dir(dir_)
        file_path = PathHelper.path(dir_, filename)
        fn(file).save(file_path)

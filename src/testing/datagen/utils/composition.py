from file_path_finder import *
from data_parser import *
from data2tex import *
from tex2img import *


def compose_data(data_root: str) -> dict[str: dict[str: str]]:
  files = file_path_finder.parse_file_paths(data_root)

  composition = dict()
  for file in files:
    filename = file_path_finder.filename(file, False)
    data = data_parser(file)

    counter = 0
    buf = dict()
    for data_ in data:
      name_data = f'{filename}_{counter}'
      counter += 1
      buf[name_data] = data_

    composition[filename] = buf
  
  return composition


def render_png(build_path: str, composition: dict[str: dict[str: str]]):
  for k, v in composition.items():
    for name_data, data in v.items():
      out_file_path = os.path.join(build_path, name_data)
      tex = data2tex(data)

      if tex2img(tex, out_file_path):
        return


def check_uniq(composition: dict[str: dict[str: str]]):
  pass


def create_doc_from_composition(doc_path: str, composition: dict[str: dict[str: str]]):
  with open(doc_path, 'w', encoding='utf8') as file:
    text = ''
    for k, v in composition.items():
      cases = ''
      for data_name, data in v.items():
        data_math = tex_math(data)

        data_name = str(data_name).replace('_', r'\_')
        cases += r'''
        %s & %s & %s & %s \\
        \hline
        ''' % (data_name, data_math, tex_math(f'\\displaystyle {data}'), tex_verbatim(data))
      
      text += tex_longtable(cases, '|l|c|c|p{5cm}|', k, 'Name', r'Case(math)', r'Case(displaymath)', r'LaTeX')
    
    text = tex_center(text)
    text = tex_title(text, 'checklist')
    text = tex_document(text)
    text = tex_package(text)

    file.write(text)

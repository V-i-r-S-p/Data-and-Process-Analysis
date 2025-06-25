from .composer import *

def main(root: str):
  print('Data creating: ', end='')

  composer = Composer(root)
  composer.create_base_data('data', 'build/latex', 'build/raw_img', 'build/checklist.tex')

  composer.add_to_middleware('rotate30', rotate30)
  # composer.add_to_middleware('rotate90', rotate90)
  # composer.add_to_middleware('rotate180', rotate180)
  # composer.add_to_middleware('rotate270', rotate270)
  composer.add_to_middleware('resize4x', resize4x)
  composer.add_to_middleware('resize8x', resize8x)
  composer.add_to_middleware('blur', blur)
  composer.add_to_middleware('whiteText', whiteText)

  composer.create_data_from_middleware('build/raw_img', 'build/effect')
  print('Done')

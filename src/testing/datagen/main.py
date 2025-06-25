from .utils.main import main
from .utils.path_helper import PathHelper

main(PathHelper.find_nearest_folder(__file__))

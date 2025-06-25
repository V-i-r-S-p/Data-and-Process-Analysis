import pytest
from datagen.utils.path_helper import PathHelper
from data_handler import *

from alphabet import VOCAB

@pytest.fixture(scope="session", autouse=True)
def resource_setup(request):
    setup_data()


def get_data_keys():
    filtered = filter_latex_files('./test_images', 'latex_', VOCAB)
    return list(filtered.keys())


@pytest.fixture(scope="function", )
def latex_resource_setup(request):
    filtered = filter_latex_files('./test_images', 'latex_', VOCAB)
    return filtered

@pytest.fixture(scope="function", )
def raw_resource_setup(request):
    filtered = filter_png_files('out.txt', 'raw_img_')
    return filtered

@pytest.fixture(scope="function", )
def effect_blur_resource_setup(request):
    filtered = filter_png_files('out.txt', 'effect_blur_')
    return filtered

@pytest.fixture(scope="function", )
def effect_rotate_resource_setup(request):
    filtered = filter_png_files('out.txt', 'effect_rotate30_')
    return filtered

@pytest.fixture(scope="function", )
def effect_whiteText_resource_setup(request):
    filtered = filter_png_files('out.txt', 'effect_whiteText_')
    return filtered

@pytest.fixture(scope="function", )
def effect_resize4x_resource_setup(request):
    filtered = filter_png_files('out.txt', 'effect_resize4x_')
    return filtered

@pytest.fixture(scope="function", )
def effect_resize8x_resource_setup(request):
    filtered = filter_png_files('out.txt', 'effect_resize8x_')
    return filtered


def get_external_data_keys():
    filtered = filter_latex_files('./test_images', 'external_', VOCAB, '.txt')
    return list(filtered.keys())

@pytest.fixture(scope="function", )
def external_latex_resource_setup(request):
    filtered = filter_latex_files('./test_images', 'external_', VOCAB, '.txt')
    return filtered

@pytest.fixture(scope="function", )
def external_raw_resource_setup(request):
    filtered = filter_png_files('out.txt', 'external_')
    return filtered


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    skipped = len(terminalreporter.stats.get("skipped", []))
    total = passed + failed + skipped

    real_total = total - skipped
    efficiency = 0.0
    if real_total > 0:
        efficiency = passed / real_total
    terminalreporter.write_sep('-', '[Stat]', bold=True)
    terminalreporter.write_line(f'Total:       {total}')
    terminalreporter.write_line(f'Passed:      {passed}')
    terminalreporter.write_line(f'Failed:      {failed}')
    terminalreporter.write_line(f'Skipped:     {skipped}')
    terminalreporter.write_line(f'Efficiency:  {efficiency}')

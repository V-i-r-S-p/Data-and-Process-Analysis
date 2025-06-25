import conftest
import pytest
from tex_comp import LatexComparator


class TestClass():
    def comp(self, latex1: str, latex2: str, fast=True, absolute=True):
        assert_msg = f'Expected: [\"{latex1}\"] | got: [\"{latex2}\"].'
        if not absolute:
            if fast == True:
                assert LatexComparator.equals(latex1, latex2), assert_msg
            else:
                assert LatexComparator.syntax_equals(latex1, latex2), assert_msg
        else:
            assert latex1 == latex2, assert_msg

    @pytest.mark.parametrize('key', conftest.get_data_keys())
    def test_smoke(self, key, latex_resource_setup, raw_resource_setup):
        self.comp(latex_resource_setup[key], raw_resource_setup[key])

    @pytest.mark.parametrize('key', conftest.get_data_keys())
    def test_blur(self, key, latex_resource_setup, effect_blur_resource_setup):
        self.comp(latex_resource_setup[key], effect_blur_resource_setup[key])

    @pytest.mark.parametrize('key', conftest.get_data_keys())
    def test_rotate(self, key, latex_resource_setup, effect_rotate_resource_setup):
        self.comp(latex_resource_setup[key], effect_rotate_resource_setup[key])

    @pytest.mark.parametrize('key', conftest.get_data_keys())
    def test_whiteText(self, key, latex_resource_setup, effect_whiteText_resource_setup):
        self.comp(latex_resource_setup[key], effect_whiteText_resource_setup[key])


    @pytest.mark.parametrize('key', conftest.get_external_data_keys())
    def test_external_data(self, key, external_latex_resource_setup, external_raw_resource_setup):
        self.comp(external_latex_resource_setup[key], external_raw_resource_setup[key])

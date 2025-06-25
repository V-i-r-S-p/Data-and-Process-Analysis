import re
import cv2
import numpy as np
from latex2sympy2_extended import latex2sympy, normalize_latex, NormalizationConfig
from sympy import sympify, simplify, latex, SympifyError
from typing import List, Optional, Tuple

import sympy
from datagen.utils.tex2img import *

class LatexComparator:
    def to_tokens(latex_str: str) -> List[str]:
        try:
            return normalize_latex(latex_str, NormalizationConfig(units=True, nits=True)).split()
        except Exception as e:
            return None

    @staticmethod
    def parse_latex(latex_str: str):
        try:
            return latex2sympy(f'${latex_str}$')
        except Exception as e:
            return None

    @staticmethod
    def normalize_latex(latex_str: str):
        try:
            return normalize_latex(latex_str, NormalizationConfig(units=True, nits=True))
        except Exception as e:
            return None

    @staticmethod
    def syntax_equals(latex1: str, latex2: str) -> bool:
        expr1 = LatexComparator.parse_latex(latex1)
        expr2 = LatexComparator.parse_latex(latex2)
        if expr1 is None or expr2 is None:
            return False

        return simplify(expr1 - expr2) == 0

    @staticmethod
    def semantic_equals(latex1: str, latex2: str) -> bool:
        expr1 = LatexComparator.normalize_latex(latex1)
        expr2 = LatexComparator.normalize_latex(latex2)
        if expr1 is None or expr2 is None:
            return False
        return expr1 == expr2

    @staticmethod
    def render_latex_to_image(latex_str: str, output_path: str = "temp.png") -> Optional[np.ndarray]:
        try:
            tex2img(f'${LatexComparator.normalize_latex(latex_str)}$', output_path)
            img = cv2.imread(output_path, cv2.IMREAD_GRAYSCALE)
            return img
        except:
            return None

    @staticmethod
    def visual_similarity(img1: np.ndarray, img2: np.ndarray, threshold: float = 0.99) -> bool:
        if img1 is None or img2 is None:
            return False

        height = max(img1.shape[0], img2.shape[0])
        width = max(img1.shape[1], img2.shape[1])
        img1_resized = cv2.resize(img1, (width, height))
        img2_resized = cv2.resize(img2, (width, height))

        diff = cv2.absdiff(img1_resized, img2_resized)
        similarity = 1 - np.mean(diff) / 255
        return similarity >= threshold

    @staticmethod
    def visual_equals(latex1: str, latex2: str) -> bool:
        img1 = LatexComparator.render_latex_to_image(latex1, "./temp1.png")
        img2 = LatexComparator.render_latex_to_image(latex2, "./temp2.png")
        return LatexComparator.visual_similarity(img1, img2)

    @staticmethod
    def equals(latex1: str, latex2: str) -> bool:
        expr1 = LatexComparator.normalize_latex(latex1)
        expr2 = LatexComparator.normalize_latex(latex2)
        if expr1 is None or expr2 is None:
            return False
        elif LatexComparator.syntax_equals(latex1, latex2):
            if LatexComparator.semantic_equals(latex1, latex2):
                return True
        else:
            return LatexComparator.visual_equals(latex1, latex2)
        return False

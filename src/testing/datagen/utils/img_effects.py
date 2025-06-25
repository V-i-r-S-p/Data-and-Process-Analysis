from PIL import Image, ImageFilter, ImageOps, ImageColor
import cv2
import numpy as np
from typing import Union, Tuple

class ImageEffectBuilder:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert('RGBA')
        self.image.height

    def apply_blur(self, radius) -> "ImageEffectBuilder":
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self

    def resize(self, width=None, height=None) -> "ImageEffectBuilder":
        if width is None and height is None:
            raise ValueError("Required width or height")

        original_width, original_height = self.image.size

        if width is None:
            ratio = height / original_height
            width = int(original_width * ratio)
        elif height is None:
            ratio = width / original_width
            height = int(original_height * ratio)

        self.image = self.image.resize((width, height), Image.LANCZOS)
        return self

    def perspective_transform(self, src_points) -> "ImageEffectBuilder":
        width, height = self.image.size

        img_array = np.array(self.image)

        dst_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
        src_points = np.float32(src_points)

        matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        transformed_img = cv2.warpPerspective(
            img_array, matrix, (width, height), flags=cv2.INTER_LINEAR
        )

        self.image = Image.fromarray(transformed_img)
        return self

    def rotate(self, angle, background=(0, 0, 0, 0)) -> "ImageEffectBuilder":
        rotated = self.image.rotate(
            angle,
            center=(self.image.width // 2, self.image.height // 2),
            expand=True,
            fillcolor=background
        )
        self.image = rotated
        return self

    def apply_mask(self, mask_path):
        mask = Image.open(mask_path).convert("L")
        self.image.putalpha(mask)
        return self

    def overlay_image(self, overlay_path, position=(0, 0), opacity=1.0) -> "ImageEffectBuilder":
        overlay = Image.open(overlay_path).convert("RGBA")
        overlay = overlay.resize(self.image.size) if overlay.size != self.image.size else overlay

        if opacity < 1.0:
            overlay = overlay.copy()
            alpha = overlay.split()[3]
            alpha = Image.eval(alpha, lambda a: int(a * opacity))
            overlay.putalpha(alpha)

        self.image = Image.alpha_composite(self.image, overlay)
        return self

    def replace_transparent(
        self,
        new_color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]],
    ) -> "ImageEffectBuilder":
        white_bg = Image.new("RGBA", self.image.size, self._parse_color(new_color))
        self.image = Image.alpha_composite(white_bg, self.image)
        return self

    def replace_color(
        self,
        target_color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]],
        new_color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]],
        tolerance: int = 30
    ) -> "ImageEffectBuilder":
        target = self._parse_color(target_color)
        new = self._parse_color(new_color)

        img_array = np.array(self.image)

        distances = np.sqrt(
            (img_array[..., 0] - target[0])**2 +
            (img_array[..., 1] - target[1])**2 +
            (img_array[..., 2] - target[2])**2
        )

        mask = distances <= tolerance

        if target[3] == new[3]:
            for c in range(3):
                img_array[..., c][mask] = new[c]
        else:
            img_array[mask] = new

        self.image = Image.fromarray(img_array)
        return self

    def remove_background(
        self,
        background_color: Union[str, Tuple[int, int, int]] = (255, 255, 255),
        tolerance: int = 30
    ) -> "ImageEffectBuilder":
        return self.replace_color(
            target_color=background_color,
            new_color=(0, 0, 0, 0),
            tolerance=tolerance
        )

    def _parse_color(
        self,
        color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]
    ) -> Tuple[int, int, int, int]:
        if isinstance(color, str):
            color = ImageColor.getrgb(color)
        if len(color) == 3:
            return (*color, 255)
        return color

    def save(self, output_path):
        self.image.save(output_path)
        return self


# <----- presets ----->
background = (255, 255, 255, 255)
colorless = (0, 0, 0, 0)
def rotate30(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.rotate(30, background)
    builder.replace_transparent(background)
    return builder

def rotate90(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.rotate(90, background)
    builder.replace_transparent(background)
    return builder

def rotate180(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.rotate(180, background)
    builder.replace_transparent(background)
    return builder

def rotate270(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.rotate(270, background)
    builder.replace_transparent(background)
    return builder

def resize4x(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.resize(height=builder.image.height//4, width=builder.image.width//4)
    builder.replace_transparent(background)
    return builder

def resize8x(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.resize(height=builder.image.height//8, width=builder.image.width//8)
    builder.replace_transparent(background)
    return builder

def blur(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.apply_blur(3)
    builder.replace_transparent(background)
    return builder

def whiteText(file_path):
    builder = ImageEffectBuilder(file_path)
    builder.replace_color('black', 'white')
    builder.replace_transparent('black')

    return builder

from pathlib import Path
import skimage as ski
from skimage.morphology import *
from skimage.transform import resize
from skimage.filters import threshold_otsu
from skimage.util import compare_images
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from PIL import Image
import re


class DigitExtractor:
    DATASET_PATH = Path("../dataset/gasmeter")
    IM_WIDTH = 1000

    def __init__(self):
        self.img_paths = list(DigitExtractor.DATASET_PATH.iterdir())

    def img_read(self, img_path: Path):
        img = ski.io.imread(img_path, as_gray=True)

        h, w = img.shape
        return resize(img, (h * DigitExtractor.IM_WIDTH / w, DigitExtractor.IM_WIDTH))

    @staticmethod
    def img_preprocess(img_orig):
        img = img_orig

        # Get rid of black letters
        img = area_opening(img, 500)
        img = reconstruction(img, img_orig)
        img = compare_images(img, img_orig, method='diff')

        # Threshold
        thresh = threshold_otsu(img)
        img = img > thresh

        # Remove small objects
        img = remove_small_objects(img, 50)
        img = np.invert(img)

        return Image.fromarray(img).convert('RGB')

    @staticmethod
    def visualize(img_orig, img, txt: str):
        fig, ax = plt.subplots(1, 2, figsize=(15, 5))
        ax[0].imshow(img_orig, cmap='gray')
        ax[0].axis('off')
        ax[1].imshow(img, cmap='gray')
        ax[1].axis('off')

        fig.text(0.5, 0.04, txt, ha='center')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def img_to_string(img):
        try:
            txt = pytesseract.image_to_string(
                img, config='-c tessedit_char_whitelist=0123456789-,m'
            )
            match = re.search(r"([0-9]{4,5}),?([0-9]{0,2})", txt)
            txt = ",".join(match.groups())
            return txt
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def extract_digits(img_orig, show=True) -> str:
        img = DigitExtractor.img_preprocess(img_orig)
        txt = DigitExtractor.img_to_string(img)

        if show:
            DigitExtractor.visualize(img_orig, img, txt)

        return txt

    def process_dataset(self):
        for i, img_path in enumerate(self.img_paths):
            print(i)
            img = self.img_read(img_path)
            digits = DigitExtractor.extract_digits(img, show=True)


de = DigitExtractor()
de.process_dataset()


# fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
# plt.show()

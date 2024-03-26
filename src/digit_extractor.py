from abc import abstractmethod
from pathlib import Path
from typing import Optional
import skimage as ski
from skimage.morphology import *
from skimage.transform import resize
from skimage.filters import threshold_otsu
from skimage.util import compare_images
from skimage.exposure import equalize_hist, equalize_adapthist
import numpy as np
from matplotlib import pyplot as plt
import pytesseract
from PIL import Image
import re
import pandas as pd


class DigitExtractor:
    DATASET_PATH = Path("dataset/gasmeter")
    IM_WIDTH = 1000
    RE_WHITESPACE_PATTERN = re.compile(r"\s")
    RE_DIGIT_PARSER_PATTERN = re.compile(r"([0-9]{4,5}),?([0-9]{0,2})")
    

    def __init__(self, csv_name: str):
        self.csv_name = csv_name
        self.img_paths = list(DigitExtractor.DATASET_PATH.iterdir())

    def img_read(self, img_path: Path):
        img = ski.io.imread(img_path, as_gray=True)

        h, w = img.shape
        return resize(img, (h * DigitExtractor.IM_WIDTH / w, DigitExtractor.IM_WIDTH))

    @abstractmethod
    def img_preprocess(self, img_orig, show: bool):
        ...

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
            txt = re.sub(DigitExtractor.RE_WHITESPACE_PATTERN, "", txt)
            match = re.search(DigitExtractor.RE_DIGIT_PARSER_PATTERN, txt)
            txt = ",".join(match.groups())
            return txt
        except Exception as e:
            print(e)
            return ""

    def extract_digits(self, img_orig, show=True) -> str:
        img = self.img_preprocess(img_orig, show)
        txt = DigitExtractor.img_to_string(img)

        if show:
            DigitExtractor.visualize(img_orig, img, txt)

        return txt

    def process_dataset(self, img_idx=-1):
        if img_idx > -1:
            print(img_idx)
            img = self.img_read(self.img_paths[img_idx])
            self.extract_digits(img, show=True)
            return
        
        d = {
            "idx": [],
            "img_name": [],
            "digits": []
        }
        for i, img_path in enumerate(self.img_paths):
            print(i)
            img = self.img_read(img_path)
            digits = self.extract_digits(img, show=False)
            print(digits)
            
            d["idx"].append(i)
            d["img_name"].append(img_path.name)
            d["digits"].append(digits)
            
        df = pd.DataFrame.from_dict(d)
        df.to_csv(self.csv_name)
        



# fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
# plt.show()

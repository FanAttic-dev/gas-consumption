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
    

    def __init__(self, csv_name):
        self.csv_name = csv_name
        self.img_paths = list(DigitExtractor.DATASET_PATH.iterdir())

    def img_read(self, img_path: Path):
        img = ski.io.imread(img_path, as_gray=True)

        h, w = img.shape
        return resize(img, (h * DigitExtractor.IM_WIDTH / w, DigitExtractor.IM_WIDTH))

    @staticmethod
    def img_preprocess(img_orig, show: bool):
        img = img_orig
        
        if show:
            fig = plt.figure()
            ncols = 2
            nrows = 3
            ax1 = fig.add_subplot(nrows, ncols, 1)
            ax1.title.set_text("Original")
            ax1.axis('off')
            ax1.imshow(img, cmap="gray")

        # Get rid of black letters
        img = area_opening(img, 500)
        if show:
            ax2 = fig.add_subplot(nrows, ncols, 2)
            ax2.title.set_text("Area opening")
            ax2.axis('off')
            ax2.imshow(img, cmap="gray")
        
        # img = reconstruction(img, img_orig)
        if show:
            ax3 = fig.add_subplot(nrows, ncols, 3)
            ax3.title.set_text("Reconstruction")
            ax3.axis('off')
            ax3.imshow(img, cmap="gray")
        
        
        img = compare_images(img, img_orig, method='diff')
        img = equalize_adapthist(img, nbins=8)
        if show:
            ax4 = fig.add_subplot(nrows, ncols, 4)
            ax4.title.set_text("Diff")
            ax4.axis('off')
            ax4.imshow(img, cmap="gray")

        # Threshold
        thresh = threshold_otsu(img)
        img = img > thresh
        if show:
            ax5 = fig.add_subplot(nrows, ncols, 5)
            ax5.title.set_text("Otsu Threshold")
            ax5.axis('off')
            ax5.imshow(img, cmap="gray")

        # Remove small objects
        img = remove_small_objects(img, 50)
        img = np.invert(img)
        if show:
            ax6 = fig.add_subplot(nrows, ncols, 6)
            ax6.title.set_text("Remove small objects")
            ax6.axis('off')
            ax6.imshow(img, cmap="gray")
        
        if show:
            fig.show()

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
            txt = re.sub(DigitExtractor.RE_WHITESPACE_PATTERN, "", txt)
            match = re.search(DigitExtractor.RE_DIGIT_PARSER_PATTERN, txt)
            txt = ",".join(match.groups())
            return txt
        except Exception as e:
            print(e)
            return ""

    @staticmethod
    def extract_digits(img_orig, show=True) -> str:
        img = DigitExtractor.img_preprocess(img_orig, show)
        txt = DigitExtractor.img_to_string(img)

        if show:
            DigitExtractor.visualize(img_orig, img, txt)

        return txt

    def process_dataset(self, img_idx=-1):
        if img_idx > -1:
            print(img_idx)
            img = self.img_read(self.img_paths[img_idx])
            DigitExtractor.extract_digits(img, show=True)
            return
        
        d = {
            "idx": [],
            "img_name": [],
            "digits": []
        }
        for i, img_path in enumerate(self.img_paths):
            print(i)
            img = self.img_read(img_path)
            digits = DigitExtractor.extract_digits(img, show=False)
            print(digits)
            
            d["idx"].append(i)
            d["img_name"].append(img_path.name)
            d["digits"].append(digits)
            
        df = pd.DataFrame.from_dict(d)
        df.to_csv(self.csv_name)
        



# fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
# plt.show()

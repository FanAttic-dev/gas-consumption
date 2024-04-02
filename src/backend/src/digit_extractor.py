from abc import abstractmethod
from pathlib import Path
import skimage as ski
from skimage.morphology import *
from skimage.transform import resize
from matplotlib import pyplot as plt
import pytesseract
import re
import pandas as pd

from src.constants import CSV_NAME, DIR_CSV


class DigitExtractor:
    IM_WIDTH = 1000
    RE_WHITESPACE_PATTERN = re.compile(r"\s")
    RE_DIGIT_PARSER_PATTERN = re.compile(r"([0-9]{4,5}),?([0-9]{0,2})")
    
    def __init__(self, dataset_path: Path):
        self.dataset_path = dataset_path
        DIR_CSV.mkdir(exist_ok=True, parents=True)
        self.csv_path = DIR_CSV / CSV_NAME
        self.img_paths: list[Path] = list(dataset_path.iterdir())

    @staticmethod
    def img_read(img_path: Path):
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
        txt = pytesseract.image_to_string(
            img, config='-c tessedit_char_whitelist=0123456789-,m'
        )
        txt = re.sub(DigitExtractor.RE_WHITESPACE_PATTERN, "", txt)
        match = re.search(DigitExtractor.RE_DIGIT_PARSER_PATTERN, txt)
        txt = ",".join(match.groups())
        return txt

    def extract_digits(self, img_orig, show=True) -> str:
        img = self.img_preprocess(img_orig, show)
        txt = DigitExtractor.img_to_string(img)

        if show:
            DigitExtractor.visualize(img_orig, img, txt)

        return txt

    def process_dataset(self, img_idx=-1):
        if img_idx > -1:
            print(img_idx)
            img = DigitExtractor.img_read(self.img_paths[img_idx])
            digits = self.extract_digits(img, show=False)
            print(digits)
            return
        
        if self.csv_path.exists():
            print(str(self.csv_path), "already exists, skipping processing.")
            return
        
        d = {
            "idx": [],
            "img_name": [],
            "digits": []
        }
        for i, img_path in enumerate(self.img_paths):
            try:
                img = DigitExtractor.img_read(img_path)
                digits = self.extract_digits(img, show=False)
                
                print(f"[{i}: {img_path.name}] {digits}")
                
                d["idx"].append(i)
                d["img_name"].append(img_path.name)
                d["digits"].append(digits)
            except Exception as e:
                print(e)
            
        df = pd.DataFrame.from_dict(d)
        df.to_csv(self.csv_path)
        
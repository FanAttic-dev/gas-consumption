from pathlib import Path
from skimage.morphology import *
from skimage.filters import threshold_otsu
from skimage.util import compare_images
from skimage.exposure import equalize_adapthist
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

from services.digit_extractor import DigitExtractor


class DigitExtractorMorphology(DigitExtractor):
    def __init__(self, dataset_path: Path, csv_dir: Path):
        super().__init__(dataset_path, csv_dir)

    def img_preprocess(self, img_orig, show: bool):
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

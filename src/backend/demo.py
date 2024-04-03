from pathlib import Path
from services.constants import CSV_DIRNAME, FIGURES_DIRNAME
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology
from services.digit_extractor_registration import DigitExtractorRegistration

DATASET_PATH = Path("dataset/gasmeter")
TMP_PATH = Path("tmp")
SHOW = True


def extract_digits():
    de = DigitExtractorMorphology(DATASET_PATH, TMP_PATH / CSV_DIRNAME)
    # de = DigitExtractorRegistration(DATASET_PATH)
    de.process_dataset(show=SHOW)


def analyze():
    da = DataAnalyzer(TMP_PATH / CSV_DIRNAME, TMP_PATH / FIGURES_DIRNAME)
    da.analyze(SHOW)


if __name__ == "__main__":
    extract_digits()
    analyze()

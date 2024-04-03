from pathlib import Path
from services.constants import CSV_DIRNAME, FIGURES_DIRNAME
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology
from services.digit_extractor_registration import DigitExtractorRegistration

DATASET_PATH = Path("dataset/gasmeter")
FILES_PATH = Path("files")
SHOW = True


def extract_digits():
    de = DigitExtractorMorphology(DATASET_PATH, FILES_PATH / CSV_DIRNAME)
    # de = DigitExtractorRegistration(DATASET_PATH)
    de.process_dataset(show=SHOW)


def analyze():
    da = DataAnalyzer(FILES_PATH / CSV_DIRNAME, FILES_PATH / FIGURES_DIRNAME)
    da.analyze(SHOW)


if __name__ == "__main__":
    extract_digits()
    analyze()

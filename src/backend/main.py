from pathlib import Path
from services.constants import CSV_DIRNAME
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology
from services.digit_extractor_registration import DigitExtractorRegistration

DATASET_PATH = Path("dataset/gasmeter")


def extract_digits():
    de = DigitExtractorMorphology(DATASET_PATH, CSV_DIRNAME)
    # de = DigitExtractorRegistration(DATASET_PATH)
    de.process_dataset()


def analyze():
    da = DataAnalyzer(CSV_DIRNAME)
    da.analyze()


if __name__ == "__main__":
    # extract_digits()
    analyze()

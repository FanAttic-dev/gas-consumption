from pathlib import Path
from services.constants import DIR_CSV
from services.data_analyzer import DataAnalyzer
from services.digit_extractor_morphology import DigitExtractorMorphology
from services.digit_extractor_registration import DigitExtractorRegistration

DATASET_PATH = Path("dataset/gasmeter")


def extract_digits():
    de = DigitExtractorMorphology(DATASET_PATH, DIR_CSV)
    # de = DigitExtractorRegistration(DATASET_PATH)
    de.process_dataset()


def analyze():
    da = DataAnalyzer(DIR_CSV)
    da.analyze()


if __name__ == "__main__":
    # extract_digits()
    analyze()

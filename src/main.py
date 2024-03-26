from data_analyzer import DataAnalyzer
from digit_extractor_morphology import DigitExtractorMorphology
from digit_extractor_registration import DigitExtractorRegistration

CSV_NAME = "digits.csv"


def extract_digits():
    de = DigitExtractorMorphology(CSV_NAME)
    # de = DigitExtractorRegistration(CSV_NAME)
    de.process_dataset()


def analyze():
    da = DataAnalyzer(CSV_NAME)
    da.analyze()


if __name__ == "__main__":
    # extract_digits()
    analyze()

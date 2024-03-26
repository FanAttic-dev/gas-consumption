from data_analyzer import DataAnalyzer
from digit_extractor import DigitExtractor
from digit_extractor_morphology import DigitExtractorMorphology

CSV_NAME = "digits.csv"

def extract_digits():
    de = DigitExtractorMorphology(CSV_NAME)
    de.process_dataset()
 
def analyze():
    da = DataAnalyzer(CSV_NAME)
    da.analyze()

if __name__ == "__main__":    
    # analyze()
    extract_digits()

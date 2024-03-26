from data_analyzer import DataAnalyzer
from digit_extractor import DigitExtractor

CSV_NAME = "digits.csv"

def extract_digits():
    de = DigitExtractor(CSV_NAME)
    de.process_dataset()
 
def analyze():
    da = DataAnalyzer(CSV_NAME)
    da.analyze()

if __name__ == "__main__":    
    analyze()

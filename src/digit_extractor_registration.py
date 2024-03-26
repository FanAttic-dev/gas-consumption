from digit_extractor import DigitExtractor

class DigitExtractorRegistration(DigitExtractor):
    def __init__(self, csv_name: str):
        super().__init__(csv_name)
        
    def img_preprocess(self, img_orig, show: bool):
        return img_orig
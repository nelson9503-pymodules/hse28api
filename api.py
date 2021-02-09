from .property_extractor import PropertyExtractor

def extract_property(id: int):
    extractor = PropertyExtractor()
    data = extractor.extract(id)
    return data
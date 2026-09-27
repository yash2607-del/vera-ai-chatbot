from app.categories.config import get_category_config

class PharmacyCategory:
    @staticmethod
    def get_config():
        return get_category_config("pharmacies")

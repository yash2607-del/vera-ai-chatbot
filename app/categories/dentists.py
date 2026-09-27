from app.categories.config import get_category_config

class DentistCategory:
    @staticmethod
    def get_config():
        return get_category_config("dentists")

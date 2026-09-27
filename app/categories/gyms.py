from app.categories.config import get_category_config

class GymCategory:
    @staticmethod
    def get_config():
        return get_category_config("gyms")

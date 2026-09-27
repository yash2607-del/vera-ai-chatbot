from app.categories.config import get_category_config

class RestaurantCategory:
    @staticmethod
    def get_config():
        return get_category_config("restaurants")

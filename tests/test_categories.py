from app.categories.config import CATEGORY_CONFIGS, get_category_config

def test_category_configurations():
    assert len(CATEGORY_CONFIGS) == 5
    for cat in ["dentists", "salons", "restaurants", "gyms", "pharmacies"]:
        cfg = get_category_config(cat)
        assert cfg.vertical == cat
        assert len(cfg.preferred_offers) > 0
        assert cfg.tone != ""

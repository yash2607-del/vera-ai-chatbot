from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class CategoryConfig(BaseModel):
    category_id: str
    vertical: str
    name: str
    tone: str
    preferred_offers: List[str]
    seasonal_moments: List[str]
    things_to_avoid: List[str]
    default_cta: str

CATEGORY_CONFIGS: Dict[str, CategoryConfig] = {
    "dentists": CategoryConfig(
        category_id="cat_dentists",
        vertical="dentists",
        name="Dentists & Dental Clinics",
        tone="clinical, reassuring, precise, utility-first",
        preferred_offers=["Dental Check Up", "Teeth Whitening", "Scaling & Polishing", "Root Canal Consultation"],
        seasonal_moments=["World Oral Health Day", "Back to School Clinic", "Festive Smile Makeover"],
        things_to_avoid=["overly informal slang", "guaranteeing painless results", "aggressive urgency"],
        default_cta="Should I activate this offer for local searchers?"
    ),
    "salons": CategoryConfig(
        category_id="cat_salons",
        vertical="salons",
        name="Salons & Spas",
        tone="visual, trend-focused, inviting, polished",
        preferred_offers=["Hair Spa & Haircut Combo", "Bridal Facial Package", "Gel Manicure Special", "Keratin Treatment Deal"],
        seasonal_moments=["Wedding Season", "Diwali Pamper Week", "Valentine Glow Package"],
        things_to_avoid=["clinical jargon", "dry statistical tone", "complex terms"],
        default_cta="Want me to blast this deal to nearby customers?"
    ),
    "restaurants": CategoryConfig(
        category_id="cat_restaurants",
        vertical="restaurants",
        name="Restaurants & Cafes",
        tone="appetizing, energetic, fast-paced, action-oriented",
        preferred_offers=["Lunch Buffet Special", "Buy 1 Get 1 Pizza", "Happy Hours Craft Beer", "Family Dinner Combo"],
        seasonal_moments=["IPL Match Days", "Weekend Brunch Wave", "Monsoon Snack Fest"],
        things_to_avoid=["medical tone", "stale pricing wording", "overly long intros"],
        default_cta="Shall I push this discount live for lunch hours?"
    ),
    "gyms": CategoryConfig(
        category_id="cat_gyms",
        vertical="gyms",
        name="Gyms & Fitness Centers",
        tone="motivational, high-energy, direct, goal-focused",
        preferred_offers=["3-Month Fitness Pass", "Personal Training Trial", "New Year Transformation Package", "Couples Gym Deal"],
        seasonal_moments=["New Year Resolutions", "Summer Shred Drive", "Post-Festive Detox"],
        things_to_avoid=["lazy wording", "over-promising weight loss", "passive phrasing"],
        default_cta="Ready to launch this membership push today?"
    ),
    "pharmacies": CategoryConfig(
        category_id="cat_pharmacies",
        vertical="pharmacies",
        name="Pharmacies & Wellness Stores",
        tone="reassuring, trustworthy, precise, utility-first",
        preferred_offers=["Chronic Care Refill Package", "Monsoon Immunity Booster Kit", "Diabetes Care Pack", "Senior Citizen Wellness Pass"],
        seasonal_moments=["Monsoon Health Care", "Diabetes Awareness Month", "Winter Immunity Push"],
        things_to_avoid=["playful humor", "prescription claims", "unverified cures"],
        default_cta="Should I notify regular customers about this refill discount?"
    )
}

def get_category_config(vertical: str) -> CategoryConfig:
    norm = vertical.lower().strip()
    if norm in CATEGORY_CONFIGS:
        return CATEGORY_CONFIGS[norm]
    # Fallback to general category config
    return CategoryConfig(
        category_id=f"cat_{norm}",
        vertical=norm,
        name=vertical.capitalize(),
        tone="professional, helpful, direct",
        preferred_offers=["Discount Voucher", "Special Deal"],
        seasonal_moments=["Festival Special"],
        things_to_avoid=["fake claims", "corporate jargon"],
        default_cta="Would you like to activate this campaign?"
    )

from typing import Dict, Any
from app.core.constants import SignalType
from app.models.signals import CandidateSignal

class FallbackComposer:
    @staticmethod
    def generate(signal: CandidateSignal) -> Dict[str, str]:
        ev = signal.evidence
        stype = signal.signal_type
        
        offer_title = ev.get("offer_title", "special offer")
        disc_price = ev.get("discounted_price", 299)
        locality = ev.get("locality", "your locality")
        
        if stype == SignalType.SEARCH_SPIKE:
            count = ev.get("metric_value") or ev.get("searches_in_locality") or 190
            msg = f"{count} people in {locality} are searching for '{offer_title}'. Should I send them a discounted offer at ₹{disc_price}?"
            cta = f"Should I send them a discounted {offer_title.lower()} at ₹{disc_price}?"
        elif stype == SignalType.PERFORMANCE_DIP:
            dip_val = ev.get("metric_value") or ev.get("lunch_dip") or "-22%"
            msg = f"Traffic dropped {dip_val} in {locality} recently. Should we launch an off-peak discount for '{offer_title}' at ₹{disc_price} to boost sales?"
            cta = f"Should we launch a discount for '{offer_title}'?"
        elif stype == SignalType.FESTIVAL_SEASONAL:
            event = ev.get("event_name", "Festive Season")
            msg = f"{event} demand is surging in {locality}! Want me to promote your {offer_title} package at ₹{disc_price} to nearby shoppers?"
            cta = f"Want me to promote {offer_title} for {event}?"
        elif stype == SignalType.CUSTOMER_LAPSE:
            cust_name = ev.get("customer_name", "A VIP customer")
            status = ev.get("customer_status", "inactive for 30+ days")
            msg = f"{cust_name} ({status}) hasn't visited recently. Should I send them an exclusive offer for {offer_title} at ₹{disc_price}?"
            cta = f"Should I send an exclusive offer to {cust_name}?"
        else:
            msg = f"Your listing in {locality} is getting steady interest. Should I activate a campaign for {offer_title} at ₹{disc_price}?"
            cta = f"Should I activate a campaign for {offer_title}?"

        return {
            "message": msg,
            "cta": cta,
            "send_as": "Vera"
        }

from typing import Dict, Any, Optional

class EvidenceExtractor:
    @staticmethod
    def extract_evidence(
        merchant_context: Dict[str, Any],
        trigger_context: Optional[Dict[str, Any]] = None,
        customer_context: Optional[Dict[str, Any]] = None,
        category_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Identity handling (supports official schema and flat fallback)
        identity = merchant_context.get("identity", {}) if isinstance(merchant_context.get("identity"), dict) else {}
        merchant_name = identity.get("name") or merchant_context.get("name", "Your Business")
        owner_name = identity.get("owner_first_name") or merchant_context.get("owner_name", "")
        locality = identity.get("locality") or merchant_context.get("locality", "your locality")
        city = identity.get("city") or merchant_context.get("city", "")
        vertical = merchant_context.get("category_slug") or merchant_context.get("vertical", "general")

        evidence = {
            "merchant_name": merchant_name,
            "owner_name": owner_name,
            "locality": locality,
            "city": city,
            "vertical": vertical
        }

        # Offers (check active merchant offers, then category catalog)
        offers = merchant_context.get("offers", [])
        active_offer = None
        for off in offers:
            st = off.get("status") or ("active" if off.get("active", True) else "inactive")
            if st == "active":
                active_offer = off
                break

        if not active_offer and category_config:
            catalog = category_config.get("offer_catalog", [])
            if catalog:
                active_offer = catalog[0]

        if active_offer:
            evidence["offer_title"] = active_offer.get("title", "")
            evidence["original_price"] = active_offer.get("original_price") or active_offer.get("value")
            evidence["discounted_price"] = active_offer.get("discounted_price") or active_offer.get("value") or 299
            evidence["offer_id"] = active_offer.get("id") or active_offer.get("offer_id", "")

        # Trigger details (supports official kind & payload)
        if trigger_context:
            kind = trigger_context.get("kind") or trigger_context.get("type", "")
            t_payload = trigger_context.get("payload", {}) if isinstance(trigger_context.get("payload"), dict) else {}
            
            evidence["trigger_kind"] = kind
            evidence["trigger_payload"] = t_payload
            evidence["metric"] = t_payload.get("metric") or trigger_context.get("metric", "")
            evidence["metric_value"] = t_payload.get("delta_pct") or t_payload.get("value") or trigger_context.get("value")
            evidence["topic"] = t_payload.get("top_item_id") or trigger_context.get("topic")
            evidence["event_name"] = t_payload.get("festival") or trigger_context.get("event")

        # Customer details
        if customer_context:
            c_ident = customer_context.get("identity", {}) if isinstance(customer_context.get("identity"), dict) else {}
            evidence["customer_id"] = customer_context.get("customer_id") or customer_context.get("id")
            evidence["customer_name"] = c_ident.get("name") or customer_context.get("name")
            evidence["customer_status"] = customer_context.get("status")

        # Performance metrics
        perf = merchant_context.get("performance", {}) if isinstance(merchant_context.get("performance"), dict) else {}
        evidence["views"] = perf.get("views") or merchant_context.get("metrics", {}).get("weekly_views")
        evidence["calls"] = perf.get("calls") or merchant_context.get("metrics", {}).get("calls")
        evidence["ctr"] = perf.get("ctr") or merchant_context.get("metrics", {}).get("ctr")

        return evidence

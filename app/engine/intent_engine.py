import re
from typing import Dict, Any, Tuple, Optional
from app.core.constants import ConversationState

class IntentEngine:
    AUTO_REPLY_PATTERNS = [
        r"thank you for contacting", r"our team will respond", r"out of office",
        r"automated response", r"auto-reply", r"automatic response", r"we will get back to you"
    ]

    HOSTILE_PATTERNS = [
        r"stop messaging me", r"useless spam", r"shut up", r"fuck", r"idiot",
        r"stop bothering", r"spam", r"leave me alone", r"block"
    ]

    ACCEPT_WORDS = {
        "yes", "sure", "okay", "ok", "agree", "yep", "activate",
        "proceed", "cool", "absolutely"
    }
    
    ACCEPT_PHRASES = [
        r"\bdo it\b", r"\bgo ahead\b", r"\bsend it\b", r"\bsounds good\b",
        r"\bmake it live\b", r"\blet'?s do it\b", r"\bplease do\b", r"\bwhats next\b"
    ]

    REJECT_WORDS = {
        "no", "stop", "cancel", "pass", "nope", "disable"
    }

    REJECT_PHRASES = [
        r"\bnot now\b", r"\bdon'?t want\b", r"\bmaybe later\b",
        r"\bnot interested\b", r"\bnevermind\b", r"\bno thanks\b"
    ]

    CLARIFICATION_PATTERNS = [
        r"\bhow much\b", r"\bcost\b", r"\btarget\b", r"\bradius\b", r"\bbudget\b",
        r"\bwhere\b", r"\bwho will\b", r"\bwhat is\b", r"\bcan i\b", r"\bdistance\b",
        r"\blocality\b", r"\bterms\b", r"\bdiscount\b"
    ]

    OFF_TOPIC_PATTERNS = [
        r"\bwho is\b", r"\bjoke\b", r"\bweather\b", r"\bprime minister\b",
        r"\bpresident\b", r"\bcapital of\b", r"2\s*\+\s*2", r"\bmath\b",
        r"\brecipe\b", r"\bmovie\b"
    ]

    @classmethod
    def classify_intent(cls, message: str) -> str:
        text = message.lower().strip()
        
        # Check auto-reply first
        for pat in cls.AUTO_REPLY_PATTERNS:
            if re.search(pat, text):
                return "AUTO_REPLY"

        # Check hostile next
        for pat in cls.HOSTILE_PATTERNS:
            if re.search(pat, text):
                return "HOSTILE"

        words = set(re.findall(r'\b\w+\b', text))

        # Check explicit acceptance
        if words.intersection(cls.ACCEPT_WORDS):
            return "ACCEPT"
        for pat in cls.ACCEPT_PHRASES:
            if re.search(pat, text):
                return "ACCEPT"

        # Check explicit rejection
        if words.intersection(cls.REJECT_WORDS):
            return "REJECT"
        for pat in cls.REJECT_PHRASES:
            if re.search(pat, text):
                return "REJECT"

        # Check off-topic pattern
        for pat in cls.OFF_TOPIC_PATTERNS:
            if re.search(pat, text):
                return "OFF_TOPIC"

        # Check clarification pattern
        for pat in cls.CLARIFICATION_PATTERNS:
            if re.search(pat, text):
                return "CLARIFICATION"

        return "UNKNOWN"

    @classmethod
    def process_reply(
        cls,
        previous_state: ConversationState,
        merchant_message: str,
        last_evidence: Dict[str, Any],
        last_cta: str
    ) -> Tuple[ConversationState, str, str, Optional[str], str]:
        """
        Returns: (current_state, reply_message, action_taken, new_cta, bot_action)
        where bot_action is "send", "end", or "wait".
        """
        intent = cls.classify_intent(merchant_message)
        
        offer_title = last_evidence.get("offer_title", "deal")
        discounted_price = last_evidence.get("discounted_price", 299)
        locality = last_evidence.get("locality", "your locality")
        
        if intent == "AUTO_REPLY":
            return ConversationState.NONE, "Auto-reply detected. Ending session.", "SESSION_ENDED", None, "end"

        elif intent == "HOSTILE":
            return ConversationState.REJECTED, "I apologize for any inconvenience. I won't message you again.", "OPT_OUT", None, "end"

        elif intent == "ACCEPT":
            new_state = ConversationState.ACTION_CONFIRMED
            msg = f"Done! Confirming your campaign setup for '{offer_title}' at ₹{discounted_price} in {locality}. We'll proceed with next steps now."
            return new_state, msg, "CAMPAIGN_LAUNCHED", None, "send"

        elif intent == "REJECT":
            new_state = ConversationState.REJECTED
            msg = f"Got it. I'll hold off on promoting {offer_title} for now. Let me know whenever you're ready!"
            return new_state, msg, "CAMPAIGN_CANCELLED", None, "send"

        elif intent == "CLARIFICATION":
            new_state = ConversationState.CLARIFICATION_NEEDED
            msg = f"This promotion targets active local searchers within {locality}. The price is set to ₹{discounted_price} for '{offer_title}' with no upfront ad spend required."
            cta = f"Should I make this live in {locality} now?"
            return new_state, msg, "CLARIFICATION_PROVIDED", cta, "send"

        elif intent == "OFF_TOPIC":
            new_state = ConversationState.OFF_TOPIC
            msg = f"I'm here to help grow your business! Regarding our live opportunity for '{offer_title}' in {locality}:"
            cta = last_cta or f"Should I activate this offer at ₹{discounted_price}?"
            return new_state, f"{msg} {cta}", "OFF_TOPIC_HANDLED", cta, "send"

        else:
            new_state = ConversationState.RECOMMENDATION_SENT
            msg = f"I want to make sure I get this right for {offer_title}."
            cta = last_cta or f"Should we launch this deal at ₹{discounted_price}?"
            return new_state, f"{msg} {cta}", "NONE", cta, "send"

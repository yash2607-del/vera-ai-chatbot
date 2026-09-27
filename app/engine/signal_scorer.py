from typing import List
from app.models.signals import CandidateSignal

class SignalScorer:
    @staticmethod
    def score_and_select(candidates: List[CandidateSignal]) -> CandidateSignal:
        if not candidates:
            raise ValueError("No candidate signals available to score.")

        for cand in candidates:
            score = 0.0
            ev = cand.evidence
            
            # 1. Trigger presence (30 pts)
            if ev.get("trigger_type"):
                score += 30.0

            # 2. Specific metrics / facts (25 pts)
            if ev.get("searches_in_locality") or ev.get("metric_value"):
                score += 15.0
            if ev.get("discounted_price"):
                score += 10.0

            # 3. Active offer availability (20 pts)
            if ev.get("offer_title"):
                score += 20.0

            # 4. Category fit (15 pts)
            if cand.category:
                score += 15.0

            # 5. Customer context fit (10 pts)
            if ev.get("customer_name"):
                score += 10.0

            cand.score = score

        # Deterministic sorting: higher score first, then signal_type alphabetically, then suppression_key
        candidates.sort(key=lambda c: (-c.score, c.signal_type.value, c.suppression_key))
        return candidates[0]

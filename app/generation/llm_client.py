import json
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.logging import logger
from app.generation.prompts import SYSTEM_PROMPT, build_user_prompt

class LLMClient:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.enabled = settings.USE_LLM and bool(self.api_key)
        self._client = None

        if self.enabled:
            try:
                import openai
                self._client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}. Falling back to deterministic generation.")
                self.enabled = False

    def generate_copy(self, brief: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.enabled or not self._client:
            return None

        brief_str = json.dumps(brief, indent=2)
        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": build_user_prompt(brief_str)}
                ],
                temperature=0.0,
                max_tokens=150,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            parsed = json.loads(content)
            if "message" in parsed and "cta" in parsed:
                return {
                    "message": parsed["message"],
                    "cta": parsed["cta"],
                    "send_as": parsed.get("send_as", "Vera")
                }
        except Exception as e:
            logger.error(f"LLM generation failed: {e}. Falling back to deterministic copy.")
            return None
        return None

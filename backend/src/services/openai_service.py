import openai
from typing import List, Dict, Any
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)


class OpenAIService:
    """
    Service for interacting with OpenAI API
    """

    def __init__(self):
        openai.api_key = settings.openai_api_key

    def generate_response(self, query: str, context: List[Dict[str, Any]], model: str = "gpt-3.5-turbo") -> str:
        """
        Generate a response based on the query and provided context
        """
        try:
            # Format the context for the prompt
            context_text = "\n\n".join([f"Source: {item['source_file']}\nContent: {item['text']}" for item in context])

            system_message = f"""You are an AI assistant for the Physical AI & Humanoid Robotics Textbook.
            Use the following context to answer the user's question. If the context doesn't contain
            the information needed to answer the question, say so. Always cite sources when possible."""

            user_message = f"""Context: {context_text}\n\nQuestion: {query}\n\nPlease provide a comprehensive answer based on the context provided."""

            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            raise

    def validate_api_key(self) -> bool:
        """
        Validate if the OpenAI API key is valid by making a simple test call
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"OpenAI API key validation failed: {e}")
            return False
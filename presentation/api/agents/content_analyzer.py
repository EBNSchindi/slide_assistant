"""
Content Analyzer Agent - Analyzes user input and structures it
"""
from openai import AsyncOpenAI


class ContentAnalyzerAgent:
    """Analyzes and structures user input"""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = """You are a Content Analyzer Agent. Your task is to:
1. Understand the user's input (can be bullet points, markdown, or structured text)
2. Identify the content type (statistics, narrative, list, quote, mixed)
3. Extract key information and structure it logically
4. Identify any specific formatting preferences mentioned

Respond with a JSON object containing:
{
    "content_type": "statistics|narrative|list|quote|mixed",
    "key_messages": ["message1", "message2", ...],
    "raw_content": "the structured content",
    "has_statistics": true/false,
    "has_lists": true/false,
    "has_quotes": true/false,
    "formatting_preferences": ["preference1", ...]
}"""

    async def analyze(self, user_input: str, slide_title: str = None) -> dict:
        """Analyze user input and return structured analysis"""

        user_message = f"""Please analyze this content for a slide{f' titled "{slide_title}"' if slide_title else ''}:

{user_input}"""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                response_format={"type": "json_object"},
            )

            import json
            analysis = json.loads(response.choices[0].message.content)
            return analysis

        except Exception as e:
            raise Exception(f"Content Analyzer error: {str(e)}")

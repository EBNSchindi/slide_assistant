import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# Model Provider Configuration
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  # openai | anthropic | google
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")  # gpt-4o, gpt-5, claude-sonnet-4.5, gemini-3.0-pro
ANTHROPIC_DEFAULT_MODEL = "claude-sonnet-4.5-20250514"  # Latest Claude model
GOOGLE_DEFAULT_MODEL = "gemini-3.0-pro"  # Latest Gemini model
TIMEOUT = 60

# Model mapping for per-request model selection
MODEL_TO_PROVIDER = {
    # OpenAI models
    "gpt-4o": "openai",
    "gpt-5": "openai",
    "gpt-5-mini": "openai",
    # Anthropic models (latest first)
    "claude-sonnet-4.5-20250514": "anthropic",
    "claude-sonnet-4.5": "anthropic",  # Alias
    "claude-4.5-sonnet": "anthropic",  # Alias
    "claude-3-5-sonnet-20241022": "anthropic",
    "claude-3-5-sonnet": "anthropic",  # Alias
    "claude-3-sonnet": "anthropic",  # Older version
    # Google Gemini models (latest first)
    "gemini-3.0-pro": "google",  # Gemini 3.0 Pro (latest)
    "gemini-3.0": "google",  # Alias
    "gemini-2.5-pro": "google",  # Gemini 2.5 Pro
    "gemini-2.5": "google",  # Alias
    "gemini-2.0-flash-exp": "google",  # Gemini 2.0 Flash Experimental
    "gemini-2.0-flash": "google",  # Gemini 2.0 Flash
    "gemini-1.5-pro": "google",  # Gemini 1.5 Pro (older)
    "gemini-1.5-flash": "google",  # Gemini 1.5 Flash (older)
}

# Content Generation Limits
MAX_COMPONENTS_PER_SLIDE = 3
MAX_SLIDES_PER_REQUEST = 10

# Project Configuration
PROJECTS_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "projects")
STYLES_PATH = "{project_path}/styles"
MARKDOWN_INPUT_PATH = "{project_path}/markdown/input"
MARKDOWN_OPTIMIZED_PATH = "{project_path}/markdown/optimized"
HTML_OUTPUT_PATH = "{project_path}/html"

# Server Configuration
HOST = "localhost"
PORT = 8001

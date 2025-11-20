import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# Model Provider Configuration
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  # openai | anthropic
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4o")  # gpt-4o, gpt-5, claude-3-5-sonnet-20241022
ANTHROPIC_DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
TIMEOUT = 60

# Model mapping for per-request model selection
MODEL_TO_PROVIDER = {
    # OpenAI models
    "gpt-4o": "openai",
    "gpt-5": "openai",
    "gpt-5-mini": "openai",
    # Anthropic models
    "claude-3-5-sonnet-20241022": "anthropic",
    "claude-3-5-sonnet": "anthropic",  # Alias
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

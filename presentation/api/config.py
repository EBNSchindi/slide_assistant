import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

# Model Configuration
DEFAULT_MODEL = "gpt-4o"
TIMEOUT = 60

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

# CORS Configuration
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:8000,http://localhost:8001,http://127.0.0.1:8000,http://127.0.0.1:8001"
).split(",")

# Rate Limiting Configuration
RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
RATE_LIMIT_GENERATE = os.getenv("RATE_LIMIT_GENERATE", "10/minute")
RATE_LIMIT_UPLOAD = os.getenv("RATE_LIMIT_UPLOAD", "20/minute")

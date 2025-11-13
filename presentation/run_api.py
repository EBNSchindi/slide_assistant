#!/usr/bin/env python3
"""
Run the Slides Helper AI API server
"""
import sys
import os

# Get the API directory
api_dir = os.path.join(os.path.dirname(__file__), 'api')

# Add api directory to Python path as first entry
sys.path.insert(0, api_dir)

# Now we can import from main
os.chdir(api_dir)
import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False,
        log_level="info",
    )

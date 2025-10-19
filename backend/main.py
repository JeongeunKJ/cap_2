"""
Thin entrypoint that delegates to the real FastAPI app in mdConverter.main.
This avoids import errors when running `uvicorn main:app --reload` from the backend folder.
"""

from mdConverter.main import app  # re-export FastAPI app

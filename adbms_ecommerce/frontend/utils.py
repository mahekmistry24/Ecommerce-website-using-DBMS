"""
Utility functions for the Streamlit frontend.
Makes API calls to the FastAPI backend.
"""
import requests

API_BASE = "http://localhost:8000/api"


def api_get(endpoint: str, params: dict = None):
    """Make a GET request to the backend API."""
    try:
        response = requests.get(f"{API_BASE}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Backend server is not running. Start it with: uvicorn app.main:app --reload"}
    except Exception as e:
        return {"error": str(e)}


def api_post(endpoint: str, data: dict = None):
    """Make a POST request to the backend API."""
    try:
        response = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Backend server is not running."}
    except requests.exceptions.HTTPError as e:
        try:
            return e.response.json()
        except Exception:
            return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}


def api_put(endpoint: str, data: dict = None):
    """Make a PUT request to the backend API."""
    try:
        response = requests.put(f"{API_BASE}{endpoint}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Backend server is not running."}
    except Exception as e:
        return {"error": str(e)}


def api_delete(endpoint: str):
    """Make a DELETE request to the backend API."""
    try:
        response = requests.delete(f"{API_BASE}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def get_xml_content(endpoint: str):
    """Get XML content from the backend."""
    try:
        response = requests.get(f"http://localhost:8000{endpoint}", timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

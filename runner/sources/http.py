import httpx
from typing import Optional
from runner.template import render_template


def render_headers (headers:dict , secrets:dict)->dict:
    rendered = {}
    for key,value in headers.items():
        rendered[key] = render_template(str(value), {"secrets": secrets},).strip()
    return rendered


def fetch_http_source(source_config:dict, secrets:Optional[dict]=None) -> dict:
    
    method = source_config.get("method", 'GET').upper()
    url = source_config.get("url")
    headers = source_config.get("headers", {})
    timeout = source_config.get("timeout" , 10)
    
    secrets = secrets or {}

    if not url:
        raise ValueError("URL not found")
    
    if method != "GET":
        raise ValueError("Unknown method")
    
    headers = render_headers(headers, secrets)
    
    response = httpx.get(url, headers=headers, timeout= timeout)

    response.raise_for_status()

    try:
        return response.json()
    except Exception as e:
        raise ValueError(f"HTTP source did not return valid JSON: {e}")

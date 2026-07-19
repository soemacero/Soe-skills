# Zero-Dependency Python (urllib) Notion Integration

This reference guide provides a highly robust, zero-dependency Python pattern for creating, reading, and patching Notion pages using only the standard library's `urllib`. This is extremely useful in restricted sandboxes, containers, or environments where installing external libraries like `requests` is prohibited or fails.

## Page Creation: Parent-Child Structure

To create a child page under an existing parent page, serialize the structured blocks in JSON and POST to `/v1/pages`.

```python
import json
import urllib.request
import urllib.error
import sys

def create_notion_page(api_key: str, parent_page_id: str, title: str, blocks: list) -> dict:
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    payload = {
        "parent": {
            "page_id": parent_page_id
        },
        "properties": {
            "title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            }
        },
        "children": blocks
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
            print(f"✅ Success! Page created: {response_data.get('url')}")
            return response_data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}", file=sys.stderr)
        raise
```

## Creating Page with Markdown Content (Notion-Version 2026-03-11)

In newer versions, Notion supports direct markdown injection via the `markdown` parameter.

```python
def create_page_with_markdown(api_key: str, parent_id: str, title: str, markdown_content: str) -> dict:
    url = "https://api.notion.com/v1/pages"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2026-03-11"
    }
    
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": [{"text": {"content": title}}]
        },
        "markdown": markdown_content
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    return json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
```

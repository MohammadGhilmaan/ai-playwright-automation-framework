import requests


def get_ai_locator_sync(dom_snapshot: str, description: str) -> str:
    """
    Sends the HTML string to the local Qwen AI model to find a resilient locator.
    """
    print(f"🤖 Local AI (Qwen) is analyzing DOM to find: '{description}'...")

    # Truncate to save local processing time
    truncated_dom = dom_snapshot[:3000]

    prompt = f"""
    You are an expert QA Automation Engineer using Playwright for Python.
    Given this HTML snippet and the description: "{description}", 
    return ONLY the most resilient Playwright locator string. 
    Rules:
    1. Prioritize data-testid, role, or stable CSS selectors.
    2. NEVER use brittle absolute XPaths.
    3. Return ONLY the locator string. No markdown, no explanations.

    HTML Snippet:
    {truncated_dom}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": prompt,
                "stream": False,
                "temperature": 0.1
            }
        )

        ai_response = response.json().get("response", "").strip()
        clean_locator = ai_response.replace("```css", "").replace("```", "").replace("`", "").strip()

        print(f"✅ AI Suggested Locator: {clean_locator}")
        return clean_locator

    except Exception as e:
        print(f"⚠️ AI Locator failed. Falling back to manual. Error: {e}")
        return "body"
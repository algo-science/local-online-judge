import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_ai_review(code, problem_context):
    """
    Gets AI-powered code review using the configured LLM.
    """
    load_dotenv(override=True) # Force reload environment variables
    api_key = os.getenv("LLM_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return {
            "error": "API key not configured. Please set LLM_API_KEY in your .env file."
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-pro-latest')

        prompt = f"""
        As an expert in competitive programming, please provide a concise code review for the following submission.

        **Problem Context:**
        {problem_context}

        **Submitted Code:**
        ```
        {code}
        ```

        Focus on:
        1.  **Correctness:** Does the logic seem sound for the problem?
        2.  **Efficiency:** Can the time or space complexity be improved?
        3.  **Best Practices:** Are there ways to write more idiomatic or cleaner code?
        4.  **Bugs:** Are there potential edge cases or bugs?

        Keep the review brief and to the point. Use Markdown for formatting.
        """

        response = model.generate_content(prompt)
        return {"review": response.text}

    except Exception as e:
        print(f"Error getting AI review: {e}")
        return {"error": "Failed to get AI review. Check your API key and network connection."}
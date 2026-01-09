import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_ai_review(code, problem_context, chat_history=None, user_message=None):
    """
    Gets AI-powered code review or chat response using the configured LLM.
    Args:
        code: The user's code.
        problem_context: Description of the problem.
        chat_history: List of previous messages (optional). [{'role': 'user', 'parts': ['...']}, ...]
        user_message: The new message from the user (optional).
    """
    load_dotenv(override=True) # Force reload environment variables
    api_key = os.getenv("LLM_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return {
            "error": "API key not configured. Please set LLM_API_KEY in your .env file."
        }

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Context construction
        system_context = f"""
        As an expert in competitive programming, you are assisting a user.
        
        **Problem Context:**
        {problem_context}

        **User's Code:**
        ```
        {code}
        ```

        If this is a code review request, focus on correctness, efficiency, best practices, and bugs.
        If this is a follow-up question, answer specifically what the user is asking about the code.
        """

        if not chat_history:
            # Initial Review Case
            prompt = f"{system_context}\n\nPlease provide a code review."
            response = model.generate_content(prompt)
            return {"review": response.text}
        else:
            # Chat Case
            # We need to reconstruct history for Gemini
            # We must inject the system_context into the first message or as a system instruction (if supported, but simplistic approach here)
            # Simplest: Prepend context to the very first user message in history.
            
            gemini_history = []
            for i, msg in enumerate(chat_history):
                role = 'user' if msg['role'] == 'user' else 'model'
                text = msg['parts'][0] if isinstance(msg['parts'], list) else msg['parts']
                
                # Inject context into the first user message
                if i == 0 and role == 'user':
                    text = f"{system_context}\n\n[User]: {text}"
                
                gemini_history.append({'role': role, 'parts': [text]})

            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(user_message)
            return {"review": response.text}

    except Exception as e:
        print(f"Error getting AI review: {e}")
        return {"error": "Failed to get AI review. Check your API key and network connection."}
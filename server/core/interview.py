import google.generativeai as genai
import os
from dotenv import load_dotenv

def get_ai_interview_response(chat_history, user_message, context):
    """
    Generates a response from the AI interviewer.
    
    Args:
        chat_history: List of previous messages.
        user_message: The new message from the user.
        context: Dict containing 'functional_req', 'non_functional_req', 'diagram'.
        
    Returns:
        Dict with 'reply' or 'error'.
    """
    load_dotenv(override=True)
    api_key = os.getenv("LLM_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return {"error": "API key not configured."}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')

        # Construct System Context
        system_prompt = f"""
        You are an expert Senior System Architect and Interviewer at a top tech company (like Google or Meta).
        You are conducting a System Design Interview with a candidate (the user).
        
        Your Goal:
        - Assess the candidate's ability to design scalable, reliable, and maintainable systems.
        - Guide them through the standard interview flow: Requirements -> High Level Design -> Deep Dive -> Bottlenecks.
        - Critique their inputs (requirements and diagram) constructively.
        
        Current Candidate inputs:
        [Functional Requirements]:
        {context.get('functional_req', 'None provided yet')}
        
        [Non-Functional Requirements]:
        {context.get('non_functional_req', 'None provided yet')}
        
        [System Diagram (Mermaid.js Code)]:
        {context.get('diagram', 'None provided yet')}
        
        Instructions:
        1. If the user just started, ask them to clarify requirements first.
        2. If they provided requirements, critique them (missing scale? edge cases?).
        3. If they provided a diagram, analyze the flow. Check for single points of failure, bottlenecks, or missing components (e.g., LB, Cache, DB Sharding).
        4. Be conversational but professional. Ask one thought-provoking question at a time.
        5. DO NOT solve the problem for them. Guide them.
        """
        
        # Build history for Gemini
        gemini_history = []
        
        # Inject system prompt into the first message or setup
        # Gemini 1.0 Pro doesn't support 'system' role in history, so we prepend to first turn or use simple generation if stateless.
        # However, for chat, we simply prepend the context to the latest message or the first message.
        # Let's use a fresh chat session strategy where we prepend system context to the finding.
        
        # Better approach: Prepend context to the very first user message in history if it exists,
        # OR just prepend it to the current prompt if history is empty.
        
        # Reconstruct history
        for msg in chat_history:
            role = 'user' if msg['role'] == 'user' else 'model'
            gemini_history.append({'role': role, 'parts': msg['parts']})
            
        chat = model.start_chat(history=gemini_history)
        
        # Send new message with context reminder (as "hidden" system instruction)
        full_prompt = f"{system_prompt}\n\nCandidate: {user_message}"
        
        response = chat.send_message(full_prompt)
        return {"reply": response.text}

    except Exception as e:
        print(f"AI Interview Error: {e}")
        return {"error": str(e)}

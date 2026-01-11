import google.generativeai as genai
import os
from dotenv import load_dotenv

def get_ai_interview_response(chat_history, user_message, context, action=None, step=None):
    """
    Generates a response from the AI interviewer.
    
    Args:
        chat_history: List of previous messages.
        user_message: The new message from the user.
        context: Dict containing 'functional_req', 'non_functional_req', 'diagram' etc.
        action: Optional action type (e.g., 'model_answer').
        step: Current step number (1-6).

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

        # Context Extraction
        specific_problem = context.get('problem_context', '')
        level = context.get('level', 'mid')
        current_step = step or context.get('current_step', 1)
        
        # Step Names for Context
        steps_map = {
            1: "Requirements (Functional & Non-Functional)",
            2: "Core Entities & Data Model",
            3: "API Interface Definition",
            4: "Data Flow (Sequence Diagram)",
            5: "High-Level Design (Architecture)",
            6: "Deep Dives & Bottlenecks"
        }
        step_name = steps_map.get(int(current_step), "General")

        # --- VALIDATION LOGIC ---
        if action == 'validate_step':
            prompt = f"""
            You are a strict System Design Interviewer.
            Context: Step {current_step} ({step_name}) of designing {specific_problem}.
            
            Candidate Input:
            - Reqs: {context.get('functional_req')} / {context.get('non_functional_req')}
            - Entities: {context.get('entities')}
            - API: {context.get('api')}
            - Diagram: {context.get('flow') or context.get('hld') or context.get('diagram')}
            
            CRITERIA FOR APPROVAL:
            - Goal: Check for **Minimum Viable Input**. Do NOT demand perfection. If it's a "solid start", APPROVE it.
            - Step 1 (Reqs): Input MUST contain at least 3 distinct requirements. Text length > 15 words. If it's gibberish ("abc") or empty -> REJECT.
            - Step 2 (Entities): At least 1 entity. Text length > 15 chars.
            - Step 3 (API): At least 1 endpoint.
            - Step 4/5 (Diagrams): Valid, non-empty diagram code.
            
            Return JSON ONLY:
            {{
                "approved": true or false,
                "feedback": "If approved, say 'Looks good!'. If rejected, keep it constructive."
            }}
            """
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            
            # Clean up JSON (Gemini sometimes adds ```json ... ```)
            clean_text = response.text.strip()
            if clean_text.startswith("```"):
                clean_text = clean_text.split("\n", 1)[1]
                if clean_text.endswith("```"):
                    clean_text = clean_text.rsplit("\n", 1)[0]
            
            import json
            try:
                validation_result = json.loads(clean_text)
            except:
                # Fallback
                validation_result = {"approved": False, "feedback": "System could not parse validation. Please try again or add more detail."}
                
            return {"validation": validation_result}

        # --- INTRO STEP LOGIC ---
        if action == 'intro_step':
            prompt = f"""
            You are a helpful System Design Interviewer.
            The user has just moved to **Step {current_step}: {step_name}** for the problem "{specific_problem}".
            
            Goal: Briefly introduce this step and ask them to provide the inputs.
            - Keep it encouraging.
            - 1-2 sentences max.
            - Example: "Great! Now let's define the Core Entities. What are the main data models for this system?"
            """
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            return {"reply": response.text}

        # --- DSA LOGIC ---
        problem_type = context.get('type', 'system_design')
        if problem_type == 'dsa':
            # DSA Interviewer Persona
            dsa_prompt = f"""
            You are an expert Data Structures & Algorithms Interviewer.
            Problem: {specific_problem}
            
            Your Goal:
            1. Stage 1: Assessment. Ask clarification questions if the user hasn't defined constraints.
            2. Stage 2: Approach. Discuss Time/Space complexity *before* they code. Don't let them code brute force without acknowledging it.
            3. Stage 3: Coding. Watch the code (provided in context['code']). Spot bugs but don't give the answer immediately. Hint at edge cases.
            4. Stage 4: Review. Ask them to dry run or optimize.
            
            Current Code:
            {context.get('code', 'No code yet')}
            
            Candidate Message: {user_message}
            
            Instructions:
            - Be concise. One thought/question at a time.
            - If they click "Run Code" (action='run_code'), analyze their output: {context.get('execution_output', 'N/A')}.
            - If output is wrong, help debug.
            """
            
            # Reconstruct history
            gemini_history = []
            for msg in chat_history:
                role = 'user' if msg['role'] == 'user' else 'model'
                gemini_history.append({'role': role, 'parts': msg['parts']})
            
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(dsa_prompt)
            return {"reply": response.text}

        # --- MODEL ANSWER LOGIC (System Design) ---
        if action == 'model_answer':
            prompt = f"""
            You are an expert Principal Software Engineer.
            The candidate is designing: {specific_problem}
            
            They are currently on **Step {current_step}: {step_name}**.
            
            Please provide a **concise, high-quality Model Answer** for ONLY this specific step.
            - If Step 1: List key Functional & Non-Functional requirements.
            - If Step 2: List the core entities and their attributes (Markdown).
            - If Step 3: Define the key API endpoints (Request/Response JSON).
            - If Step 4: Describe the happy path data flow.
            - If Step 5: Describe the high-level architecture components.
            - If Step 6: Identify 1-2 critical bottlenecks and solutions.
            
            Do not provide a full system design. Just the answer for Step {current_step}.
            Format your response clearly using Markdown.
            """
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            return {"reply": response.text}

        # --- CHAT LOGIC ---
        
        persona_map = {
            'junior': "Role: Senior Engineer mentoring a Junior. Focus: Basic correctness, encourage them, give hints if stuck.",
            'mid': "Role: Engineering Manager. Focus: Scalability, standard patterns, trade-offs.",
            'senior': "Role: Staff Engineer / Bar-Raiser. Focus: Deep bottlenecks, failure modes, data consistency, expert optimization."
        }
        
        selected_persona = persona_map.get(level, persona_map['mid'])
        
        system_prompt = f"""
        You are an expert System Design Interviewer acting as: {selected_persona}
        Current Phase: **Step {current_step}: {step_name}**
        
        Problem: {specific_problem}
        
        Candidate Inputs for this step:
        - Functional Reqs: {context.get('functional_req')}
        - Non-Functional Reqs: {context.get('non_functional_req')}
        - Entities: {context.get('entities')}
        - API: {context.get('api')}
        - Diagram Code: {context.get('flow') or context.get('hld') or context.get('diagram')}
        
        Your Goal:
        - Guide the candidate through **Step {current_step}**.
        - If they are on Step 1, focus only on Requirements.
        - If they are on Step 2, focus on Data Model.
        - And so on.
        - Critique what they have entered in the context above.
        - Be concise. One question at a time.
        """
        
        # Build history for Gemini
        gemini_history = []
        for msg in chat_history:
            role = 'user' if msg['role'] == 'user' else 'model'
            gemini_history.append({'role': role, 'parts': msg['parts']})
            
        chat = model.start_chat(history=gemini_history)
        
        full_prompt = f"{system_prompt}\n\nCandidate: {user_message}"
        response = chat.send_message(full_prompt)
        return {"reply": response.text}

    except Exception as e:
        print(f"AI Interview Error: {e}")
        return {"error": str(e)}

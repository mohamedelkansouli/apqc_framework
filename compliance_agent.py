import ollama

def run(industry: str, hierarchy_id: str, step_name: str, model_name: str = "llama3.2:3b"):
    """
    Agent qui analyse une étape métier et détermine son niveau de risque de conformité.
    """
    print("\n" + "=" * 80)
    print(f"AGENT: Compliance Analysis for {hierarchy_id} - {step_name}")
    print("=" * 80)

    system_prompt = """
    You are an expert in corporate compliance, legal risk, and regulatory frameworks (e.g., GDPR, SOX, HIPAA, ISO).
    You will be given a business step from the APQC framework.
    Your goal is to analyze the compliance risks associated with this step.

    Strict Rules:
    1. Analyze the user's prompt.
    2. If the prompt is a completely unrelated general knowledge question, a greeting, or a recipe (e.g., "What is the capital of France?"), reply STRICTLY with "OUT_OF_SCOPE".
    3. IMPORTANT: If the user's input matches or is very similar to one of the industries in the list (e.g., "education", "bank", "retail", "health"), you MUST reply with the EXACT industry name from the list (e.g., "Education", "Banking", "Retail").
    4. If the prompt is a business sector, a product (like "cars", "planes", "software"), or a service, you MUST map it to the closest industry in the list.
    5. If the industry is genuinely unclear, or too general (like "I have a company"), reply STRICTLY with "CrossIndustry".
    6. Do not add any explanation, extra text, or quotes: you must return ONLY the exact name or "OUT_OF_SCOPE".
    """

    user_prompt = f"""
    Industry: {industry}
    Step: {hierarchy_id} - {step_name}
    
    Analyze the compliance risk for this business step.
    """

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0.1}
        )
        
        result = response['message']['content'].strip()
        
        # Affichage formaté
        print("🛡️  COMPLIANCE ANALYSIS RESULT")
        print("-" * 80)
        print(result)
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        print("Fallback: Unable to perform compliance analysis.")
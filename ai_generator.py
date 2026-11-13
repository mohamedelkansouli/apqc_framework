import ollama

def run(industry: str, hierarchy_id: str, step_name: str, model_name: str = "llama3.2:3b"):
    """
    Agent qui analyse une étape métier et détermine si elle peut être automatisée par l'IA.
    """
    print("\n" + "=" * 80)
    print(f"AGENT: Automation Feasibility for {hierarchy_id} - {step_name}")
    print("=" * 80)

    system_prompt = """
    You are an expert in business process automation and Artificial Intelligence.
    You will be given a specific business step from the APQC framework.
    Your goal is to determine if this step can be fully or partially automated using AI, 
    or if it requires human intervention.

    Strict Rules:
    1. Analyze the step name.
    2. Decide if it can be automated by AI (e.g., data analysis, text generation, customer support) 
       or if it must be done manually (e.g., physical tasks, complex human negotiation, legal responsibility).
    3. If automation is possible, start your answer with "[AI AUTOMATION]" and explain briefly how AI can do it.
    4. If it is not possible, start your answer with "[MANUAL TASK]" and explain briefly why AI cannot do it.
    5. Keep your answer concise (max 3 sentences).
    """

    user_prompt = f"""
    Industry: {industry}
    Step: {hierarchy_id} - {step_name}
    
    Can this be automated by AI or is it a manual task?
    """

    try:
        # Appel à Ollama
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0.2} # Un peu de température pour avoir une réponse naturelle
        )
        
        result = response['message']['content'].strip()
        
        # Affichage du résultat
        if "[AI AUTOMATION]" in result:
            print("✅ FEASIBILITY: Automated by AI")
            print("-" * 80)
            print(result.replace("[AI AUTOMATION]", "").strip())
        elif "[MANUAL TASK]" in result:
            print("❌ FEASIBILITY: Manual Task Required")
            print("-" * 80)
            print(result.replace("[MANUAL TASK]", "").strip())
        else:
            # Fallback si l'IA ne respecte pas le format
            print("⚠️ FEASIBILITY: Unknown")
            print("-" * 80)
            print(result)

    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        print("Fallback: Unable to analyze. Please consider manual intervention.")

    print("=" * 80 + "\n")
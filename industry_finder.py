import json
import ollama

VALID_INDUSTRIES = [
    'AerospaceAndDefense', 'Airline', 'Automotive', 'Banking', 'Broadcasting',
    'CityGovernment', 'ConsumerElectronics', 'ConsumerProducts', 'CrossIndustry',
    'Education', 'HealthInsurancePayor', 'HealthcareProvider', 'LifeSciences',
    'PetroleumDownstream', 'PetroleumUpstream', 'PropertyAndCasualtyInsurance',
    'Retail', 'Telecommunications', 'Utilities'
]


def detect_industry(user_prompt: str, model_name: str = "llama3.2:3b") -> str:
    system_prompt = f"""
    You are an industry router agent specialized in business process analysis (APQC framework).
    Here is the exhaustive and official list of industries available in our database:
    {VALID_INDUSTRIES}

    Strict Rules:
    1. Analyze the user's prompt.
    2. If the prompt is a completely unrelated general knowledge question, a greeting, or a recipe (e.g., "What is the capital of France?"), you MUST reply with "OUT_OF_SCOPE".
    3. If the prompt is a business sector, a product (like "cars", "planes", "software"), or a service, you MUST map it to the closest industry in the list (e.g., "cars" -> "Automotive" or "Retail", "planes" -> "AerospaceAndDefense"). Do not mark short business words as out of scope.
    4. If the industry is genuinely unclear, or too general (like "I have a company"), you MUST reply with "CrossIndustry".
    5. IMPORTANT: You must output your answer in a valid JSON format. 
       Example: {{"industry": "Education"}}
       Example: {{"industry": "OUT_OF_SCOPE"}}
    """

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            format="json",  # Force le modèle à répondre en JSON
            options={"temperature": 0.0}
        )
        
        raw_content = response['message']['content'].strip()
        
        # 1. On parse le JSON
        try:
            data = json.loads(raw_content)
            detected = data.get("industry", "CrossIndustry")
        except json.JSONDecodeError:
            # Sécurité si le modèle hallucine et sort un texte non-JSON
            print("Warning: Model returned invalid JSON, falling back.")
            return "CrossIndustry"
            
        # 2. On vérifie que la réponse est valide
        if detected == "OUT_OF_SCOPE":
            return "OUT_OF_SCOPE"
        elif detected in VALID_INDUSTRIES:
            return detected
        else:
            return "CrossIndustry"
            
    except Exception as e:
        print(f"Error communicating with Ollama: {e}")
        return "CrossIndustry"


def run() -> str:
    """Boucle interactive. Retourne l'industrie validée par l'utilisateur."""
    while True:
        user_prompt = input("\nWrite about your industry : ")
        industry = detect_industry(user_prompt)

        # Gestion du hors-scope
        if industry == "OUT_OF_SCOPE":
            print("\n" + "!" * 80)
            print("ERROR: Your input seems to be out of scope. Please describe a business sector or industry.")
            print("!" * 80)
            continue  # On recommence directement la boucle
            
        # Affichage du résultat
        if industry == "CrossIndustry":
            print("*" * 80)
            print(
                "Your industry seems to not be part of the APQC referential so let's apply "
                "CrossIndustry framework.\n\nFor your information here is the list of APQC industries:\n"
                + str(VALID_INDUSTRIES)
            )
            print("*" * 80)
        else:
            print("*" * 80)
            print("Your industry detected from the APQC referential is " + industry)
            print("*" * 80)

        # Confirmation
        while True:
            confirmation = input("Is this correct? (Y/N) : ").strip().upper()
            if confirmation in ("Y", "N"):
                break
            print("Please answer with 'Y' or 'N'.")

        if confirmation == "Y":
            print(f"Great! Proceeding with industry: {industry}")
            return industry
        else:
            print("Let's try again.\n")


if __name__ == "__main__":
    result = run()
    print("Résultat :", result)
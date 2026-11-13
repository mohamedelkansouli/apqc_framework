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
    2. If the prompt is a general knowledge question, a greeting, or completely unrelated to business/industry (e.g., "What is the capital of France?"), reply STRICTLY with "OUT_OF_SCOPE".
    3. Select ONLY the exact name of the industry from the list above that best matches their sector or context.
    4. If the industry is unclear, or too general, reply STRICTLY with "CrossIndustry".
    5. Do not add any explanation, extra text, or quotes: you must return ONLY the exact name or "OUT_OF_SCOPE".
    """

    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0.0}
        )
        
        detected = response['message']['content'].strip()
        
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

        # --- NOUVEAU : Gestion du hors-scope ---
        if industry == "OUT_OF_SCOPE":
            print("\n" + "!" * 80)
            print("ERROR: Your input seems to be out of scope. Please describe a business sector or industry.")
            print("!" * 80)
            continue  # On recommence directement la boucle sans passer par la confirmation
        # ---------------------------------------

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
import industry_finder
import display_steps
import ai_generator
import compliance_agent

def main():
    # 1) Détection de l'industrie
    industry = industry_finder.run()
    
    # 2) Navigation dans les étapes
    final_hierarchy, final_name = display_steps.run(industry)
    
    # 3) Choix de l'action (comme sur ton schéma)
    print("\n" + "=" * 50)
    print("What would you like to do next?")
    print("  [1] AI steps generation (Automation feasibility)")
    print("  [2] Compliance level suggestion")
    choice = input("Your choice (1 or 2): ").strip()
    
    # 4) Exécution de l'agent choisi
    if choice == "1":
        ai_generator.run(industry, final_hierarchy, final_name)
    elif choice == "2":
        compliance_agent.run(industry, final_hierarchy, final_name)
    else:
        print("Invalid choice. Defaulting to Compliance.")
        compliance_agent.run(industry, final_hierarchy, final_name)

if __name__ == "__main__":
    main()
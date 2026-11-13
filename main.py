import industry_finder
import display_steps
import ai_generator 

def main():
    # 1) Détection de l'industrie
    industry = industry_finder.run()
    
    # 2) Navigation et affichage des étapes
    final_hierarchy, final_name = display_steps.run(industry)

    # 3) AI step generation or not 
    ai_generator.run(industry, final_hierarchy, final_name)

    
    print("\n" + "="*50)
    print(f"Finished navigating. You selected: {final_hierarchy} - {final_name}")

if __name__ == "__main__":
    main()
import industry_finder
import display_steps

def main():
    # 1) Détection de l'industrie
    industry = industry_finder.run()
    
    # 2) Navigation et affichage des étapes
    final_hierarchy, final_name = display_steps.run(industry)
    
    print("\n" + "="*50)
    print(f"Finished navigating. You selected: {final_hierarchy} - {final_name}")

if __name__ == "__main__":
    main()
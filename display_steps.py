import sqlite3
import os

DB_PATH = "all_apqc.db"
BOX_WIDTH = 74  # Largeur intérieure de la boîte

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_children(industry: str, parent_hierarchy: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    if parent_hierarchy.endswith(".0"):
        prefix = parent_hierarchy[:-2] + "."
        depth_target = 1
    else:
        prefix = parent_hierarchy + "."
        depth_target = parent_hierarchy.count(".") + 1

    cur.execute(
        """
        SELECT apqc_id, hierarchy_id, Name
        FROM all_apqc
        WHERE industry = ? AND hierarchy_id LIKE ?
        """,
        (industry, f"{prefix}%"),
    )
    rows = cur.fetchall()
    con.close()

    children = [
        (apqc_id, hid, name)
        for apqc_id, hid, name in rows
        if hid.count(".") == depth_target
    ]

    def sort_key(row):
        return tuple(int(p) for p in row[1].split("."))

    return sorted(children, key=sort_key)

def get_node_name(industry: str, hierarchy_id: str) -> str:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        "SELECT Name FROM all_apqc WHERE industry = ? AND hierarchy_id = ?",
        (industry, hierarchy_id),
    )
    row = cur.fetchone()
    con.close()
    return row[0] if row else "(unknown)"

def print_box(text: str, is_last: bool = False):
    """Affiche une boîte ASCII avec le texte."""
    # S'assurer que le texte ne dépasse pas
    if len(text) > BOX_WIDTH:
        text = text[:BOX_WIDTH-3] + "..."
    
    # Ligne du haut
    print("  ┌" + "─" * (BOX_WIDTH + 2) + "┐")
    # Ligne de texte
    print("  │ " + text.ljust(BOX_WIDTH) + " │")
    
    # Ligne du bas avec ou sans la flèche
    if is_last:
        print("  └" + "─" * (BOX_WIDTH + 2) + "┘")
    else:
        # Centrer le connecteur ┬
        mid = (BOX_WIDTH + 2) // 2
        print("  └" + "─" * mid + "┬" + "─" * (BOX_WIDTH + 2 - mid - 1) + "┘")
        # Flèche ▼ en dessous
        print(" " * (mid + 4) + "▼")

def run(industry: str) -> tuple[str, str]:
    current_hierarchy = "1.0"
    history = []

    while True:
        clear_screen()
        current_name = get_node_name(industry, current_hierarchy)
        children = get_children(industry, current_hierarchy)

        print(f"Chemin : {industry} > {current_hierarchy} {current_name}")
        print("-" * 85)
        print()

        if not children:
            print(f"  (Aucune sous-étape disponible pour {current_hierarchy}.)")
            input("\nAppuyez sur [Entrée] pour sélectionner cette étape et continuer...")
            return current_hierarchy, current_name

        # Affichage des boîtes
        for i, (_, hid, name) in enumerate(children, start=1):
            label = f"[{i}] {hid} - {name}"
            is_last = (i == len(children))
            print_box(label, is_last)

        # Menu
        print()
        prompt = f"Choisir une étape pour afficher ses enfants (1-{len(children)})"
        if history:
            prompt += ", [R] Retour"
        prompt += ", ou [Q] Quitter et garder cette étape : "

        choice = input(prompt).strip().upper()

        if choice == "Q":
            return current_hierarchy, current_name
        elif choice == "R":
            if history:
                current_hierarchy = history.pop()
            else:
                print("Vous êtes déjà au niveau racine. Appuyez sur Entrée.")
                input()
        elif choice.isdigit() and 1 <= int(choice) <= len(children):
            history.append(current_hierarchy)
            current_hierarchy = children[int(choice) - 1][1]
        else:
            print("Entrée invalide. Appuyez sur Entrée pour réessayer.")
            input()
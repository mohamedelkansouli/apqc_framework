import sqlite3
import os

DB_PATH = "all_apqc.db"
BOX_WIDTH = 74

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_children(industry: str, parent_hierarchy: str):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    
    if parent_hierarchy == "ROOT":
        # 1. Racine : on cherche tout ce qui finit par .0 (ex: 1.0, 2.0, 4.0)
        cur.execute(
            "SELECT apqc_id, hierarchy_id, Name FROM all_apqc WHERE industry = ? AND hierarchy_id LIKE '%.0'",
            (industry,)
        )
        rows = cur.fetchall()
        # On garde ceux qui ont exactement 1 point (pour exclure 1.1.0 s'il y en a)
        children = [(a, h, n) for a, h, n in rows if h.count(".") == 1]
        
    elif parent_hierarchy.endswith(".0"):
        # 2. Catégorie (ex: 4.0) : ses enfants sont 4.1, 4.2 (donc le préfixe SQL est "4.")
        base = parent_hierarchy.replace(".0", ".")
        cur.execute(
            "SELECT apqc_id, hierarchy_id, Name FROM all_apqc WHERE industry = ? AND hierarchy_id LIKE ?",
            (industry, f"{base}%")
        )
        rows = cur.fetchall()
        # On garde ceux qui ont 1 point (ex: 4.1, 4.2) et on exclut le parent (4.0)
        children = [(a, h, n) for a, h, n in rows if h.count(".") == 1 and h != parent_hierarchy]
        
    else:
        # 3. Sous-niveau (ex: 4.1) : ses enfants sont 4.1.1, 4.1.2
        base = parent_hierarchy + "."
        cur.execute(
            "SELECT apqc_id, hierarchy_id, Name FROM all_apqc WHERE industry = ? AND hierarchy_id LIKE ?",
            (industry, f"{base}%")
        )
        rows = cur.fetchall()
        # On garde ceux qui ont un point de plus que le parent
        depth_target = parent_hierarchy.count(".") + 1
        children = [(a, h, n) for a, h, n in rows if h.count(".") == depth_target]

    con.close()

    def sort_key(row):
        return tuple(int(p) for p in row[1].split("."))

    return sorted(children, key=sort_key)


def get_node_name(industry: str, hierarchy_id: str) -> str:
    if hierarchy_id == "ROOT":
        return "APQC Categories"
        
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
    if len(text) > BOX_WIDTH:
        text = text[:BOX_WIDTH-3] + "..."
    
    print("  ┌" + "─" * (BOX_WIDTH + 2) + "┐")
    print("  │ " + text.ljust(BOX_WIDTH) + " │")
    
    if is_last:
        print("  └" + "─" * (BOX_WIDTH + 2) + "┘")
    else:
        mid = (BOX_WIDTH + 2) // 2
        print("  └" + "─" * mid + "┬" + "─" * (BOX_WIDTH + 2 - mid - 1) + "┘")
        print(" " * (mid + 4) + "▼")


def run(industry: str) -> tuple[str, str]:
    current_hierarchy = "ROOT"
    history = []

    while True:
        clear_screen()
        current_name = get_node_name(industry, current_hierarchy)
        children = get_children(industry, current_hierarchy)

        if current_hierarchy == "ROOT":
            print(f"Chemin : {industry}")
        else:
            print(f"Chemin : {industry} > {current_hierarchy} {current_name}")
        print("-" * 85)
        print()

        if not children:
            print(f"  (Aucune sous-étape disponible pour {current_hierarchy}.)")
            input("\nAppuyez sur [Entrée] pour sélectionner cette étape et continuer...")
            return current_hierarchy, current_name

        for i, (_, hid, name) in enumerate(children, start=1):
            label = f"[{i}] {hid} - {name}"
            is_last = (i == len(children))
            print_box(label, is_last)

        print()
        prompt = f"Choisir une étape pour afficher ses enfants (1-{len(children)})"
        if history:
            prompt += ", [R] Retour"
        prompt += ", ou [Q] Quitter : "

        choice = input(prompt).strip().upper()

        if choice == "Q":
            if current_hierarchy == "ROOT":
                print("Veuillez sélectionner une catégorie avant de quitter.")
                input("Appuyez sur Entrée pour continuer...")
                continue
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
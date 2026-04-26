import json
import os

class CourseManager:
    def __init__(self, fichier="sauvegarde.txt"):
        self.fichier = fichier
        self.liste_courses = {"articles": []}
        self.charger()

    def charger(self):
        if os.path.exists(self.fichier):
            with open(self.fichier, "r", encoding="utf-8") as f:
                try:
                    self.liste_courses = json.load(f)
                except json.JSONDecodeError:
                    self.liste_courses = {"articles": []}

    def sauvegarder(self):
        with open(self.fichier, "w", encoding="utf-8") as f:
            json.dump(self.liste_courses, f, indent=4, ensure_ascii=False)

    def afficher(self):
        if not self.liste_courses["articles"]:
            print("La liste est vide.")
            return
        print("\n--- LISTE DE COURSES ---")
        for article in self.liste_courses["articles"]:
            statut = "✔" if article["achete"] else "◻"
            print(f"{statut} {article['nom']} (x{article['quantite']}) [{article['categorie']}]")

    def ajouter(self, nom, quantite=1, categorie="Divers"):
        for article in self.liste_courses["articles"]:
            if article["nom"].lower() == nom.lower():
                print("Erreur : article existe déjà.")
                return
        self.liste_courses["articles"].append({
            "nom": nom,
            "quantite": quantite,
            "categorie": categorie,
            "achete": False
        })
        print(f"{nom} ajouté avec succès.")

    def supprimer(self, nom):
        for article in self.liste_courses["articles"]:
            if article["nom"].lower() == nom.lower():
                self.liste_courses["articles"].remove(article)
                print(f"{nom} supprimé avec succès.")
                return
        print("Erreur : article introuvable.")

    def modifier(self, nom, quantite=None, categorie=None):
        for article in self.liste_courses["articles"]:
            if article["nom"].lower() == nom.lower():
                if quantite:
                    article["quantite"] = quantite
                if categorie:
                    article["categorie"] = categorie
                print(f"{nom} modifié avec succès.")
                return
        print("Erreur : article introuvable.")

    def marquer_achete(self, nom):
        for article in self.liste_courses["articles"]:
            if article["nom"].lower() == nom.lower():
                if article["achete"]:
                    print("Déjà acheté.")
                else:
                    article["achete"] = True
                    print(f"{nom} marqué comme acheté.")
                return
        print("Erreur : article introuvable.")

    def afficher_par_categorie(self):
        categories = {}
        for article in self.liste_courses["articles"]:
            categories.setdefault(article["categorie"], []).append(article)
        print("\n--- PAR CATÉGORIE ---")
        for cat, articles in categories.items():
            print(f"{cat} :")
            for a in articles:
                print(f"  - {a['nom']} (x{a['quantite']})")

    def rechercher(self, mot_cle):
        resultats = [a for a in self.liste_courses["articles"] if mot_cle.lower() in a["nom"].lower()]
        if not resultats:
            print("Aucun résultat.")
        else:
            for a in resultats:
                print(f"{a['nom']} (x{a['quantite']}) [{a['categorie']}]")

    def vider(self):
        confirmation = input("Êtes-vous sûr ? (o/n) : ").lower()
        if confirmation in ["o", "oui"]:
            self.liste_courses["articles"].clear()
            print("Liste vidée.")
        else:
            print("Opération annulée.")
            
            
from course_manager import CourseManager

def menu():
    manager = CourseManager()

    while True:
        print("\n=== GESTIONNAIRE DE LISTE DE COURSES ===")
        print("1. Afficher la liste de courses")
        print("2. Ajouter un article")
        print("3. Supprimer un article")
        print("4. Modifier un article")
        print("5. Marquer un article comme acheté")
        print("6. Afficher les articles par catégorie")
        print("7. Rechercher un article")
        print("8. Vider la liste")
        print("9. Sauvegarder et quitter")

        choix = input("Choisissez une option : ")

        if choix == "1":
            manager.afficher_liste()
        elif choix == "2":
            nom = input("Nom de l'article : ")
            quantite = input("Quantité (défaut 1) : ")
            categorie = input("Catégorie (défaut Divers) : ")
            manager.ajouter(nom, int(quantite) if quantite else 1, categorie if categorie else "Divers")
        elif choix == "3":
            manager.supprimer(input("Nom de l'article à supprimer : "))
        elif choix == "4":
            nom = input("Nom de l'article à modifier : ")
            quantite = input("Nouvelle quantité (laisser vide pour ne pas changer) : ")
            categorie = input("Nouvelle catégorie (laisser vide pour ne pas changer) : ")
            manager.modifier(nom, int(quantite) if quantite else None, categorie if categorie else None)
        elif choix == "5":
            manager.marquer_achete(input("Nom de l'article : "))
        elif choix == "6":
            manager.afficher_par_categorie()
        elif choix == "7":
            manager.rechercher(input("Mot-clé : "))
        elif choix == "8":
            manager.vider()
        elif choix == "9":
            manager.sauvegarder()
            print("Liste sauvegardée. Au revoir !")
            break
        else:
            print("Option invalide.")

if __name__ == "__main__":
    menu()

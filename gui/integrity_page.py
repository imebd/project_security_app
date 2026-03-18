import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.hashing import HashManager


COLORS = {
    "page": "#F5F3FF",       # violet très clair pour fond
    "card": "#EDE9FE",       # violet clair pour les cartes
    "card2": "#FDF2FA",      # rose pâle pour les textbox
    "text": "#5B21B6",       # violet foncé pour texte
    "muted": "#A78BFA",      # violet clair pour textes secondaires
    "btn": "#EC4899",        # rose pastel pour boutons
    "hover": "#DB2777",      # rose plus foncé au hover
}


class IntegrityPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["page"])

        self.hash_manager = HashManager()

        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self, text="Module Intégrité", font=ctk.CTkFont(size=28, weight="bold"), text_color=COLORS["text"])
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        left = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        left.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        right = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        right.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)

        self.result_box = ctk.CTkTextbox(left, fg_color=COLORS["card2"], text_color=COLORS["text"], height=420)
        self.result_box.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        ctk.CTkButton(left, text="Calculer SHA-256", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.calculate_hash).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(left, text="Vérifier intégrité", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.verify_integrity).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(left, text="Simuler modification", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.modify_file).pack(fill="x", padx=20, pady=(8, 20))

        ctk.CTkLabel(right, text="Zone pédagogique", text_color=COLORS["text"], font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w"
        )

        pedagogic = ctk.CTkTextbox(right, fg_color=COLORS["card2"], text_color=COLORS["text"])
        pedagogic.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        pedagogic.insert(
            "1.0",
            "Intégrité (CIA)\n"
            "- SHA-256 calcule une empreinte unique d'un fichier ou d'un texte.\n"
            "- Si le fichier change, le hash change.\n\n"
            "Objectif : détecter toute modification non autorisée.\n\n"
            "Limites :\n"
            "- Le hash ne chiffre pas le contenu.\n"
            "- Il ne prouve pas à lui seul l'identité de l'auteur.\n"
            "- Il faut comparer avec une valeur de référence fiable."
        )
        pedagogic.configure(state="disabled")

    def _set_result(self, text: str):
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)

    def calculate_hash(self):
        filepath = filedialog.askopenfilename(title="Choisir un fichier")
        if not filepath:
            return

        try:
            file_hash = self.hash_manager.calculate_sha256(filepath)
            self._set_result(f"Fichier : {filepath}\n\nSHA-256 :\n{file_hash}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de calculer le hash.\n{e}")

    def verify_integrity(self):
        filepath = filedialog.askopenfilename(title="Choisir un fichier à vérifier")
        if not filepath:
            return

        expected_hash = ctk.CTkInputDialog(text="Entrez le hash attendu :", title="Vérification").get_input()
        if not expected_hash:
            messagebox.showerror("Erreur", "Le hash attendu est vide.")
            return

        try:
            result = self.hash_manager.verify_hash(filepath, expected_hash)
            if result:
                messagebox.showinfo("Résultat", "Le fichier est intact.")
            else:
                messagebox.showerror("Résultat", "Le fichier a été modifié ou le hash est incorrect.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de vérifier l'intégrité.\n{e}")

    def modify_file(self):
        filepath = filedialog.askopenfilename(title="Choisir un fichier à modifier")
        if not filepath:
            return

        try:
            self.hash_manager.simulate_modification(filepath)
            messagebox.showinfo("Simulation", "Le fichier a été modifié pour la démonstration.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de modifier le fichier.\n{e}")
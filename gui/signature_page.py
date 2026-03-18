import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.asymmetric import AsymmetricCipher
from core.signature import DigitalSignature


COLORS = {
    "page": "#F5F3FF",    # violet très pâle pour le fond général
    "card": "#EDE9FE",    # violet clair pour les cartes
    "card2": "#FDF2FA",   # rose très pâle pour les textbox
    "text": "#5B21B6",    # violet foncé pour le texte, lisible sur clair
    "btn": "#EC4899",     # rose pastel vif pour les boutons
    "hover": "#DB2777",   # rose plus intense au survol
}


class SignaturePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["page"])

        self.asymmetric = AsymmetricCipher()
        self.signature_manager = DigitalSignature()
        self.private_key = None
        self.public_key = None
        self.current_signature = None

        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self, text="Module Signature", font=ctk.CTkFont(size=28, weight="bold"), text_color=COLORS["text"])
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        left = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        left.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

        right = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        right.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)

        self.text_input = ctk.CTkTextbox(left, height=160, fg_color=COLORS["card2"], text_color=COLORS["text"])
        self.text_input.pack(fill="x", padx=20, pady=(20, 10))
        self.text_input.insert("1.0", "Message à signer.")

        self.result_box = ctk.CTkTextbox(left, height=240, fg_color=COLORS["card2"], text_color=COLORS["text"])
        self.result_box.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        ctk.CTkButton(left, text="Générer clés RSA", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.generate_keys).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(left, text="Signer texte", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.sign_text).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(left, text="Vérifier signature texte", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.verify_text_signature).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(left, text="Signer fichier", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.sign_file).pack(fill="x", padx=20, pady=8)
        ctk.CTkButton(left, text="Vérifier signature fichier", fg_color=COLORS["btn"], hover_color=COLORS["hover"], command=self.verify_file_signature).pack(fill="x", padx=20, pady=(8, 20))

        ctk.CTkLabel(right, text="Zone pédagogique", text_color=COLORS["text"], font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w"
        )

        pedagogic = ctk.CTkTextbox(right, fg_color=COLORS["card2"], text_color=COLORS["text"])
        pedagogic.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        pedagogic.insert(
            "1.0",
            "Authentification & Non-répudiation\n"
            "- La clé privée sert à signer.\n"
            "- La clé publique sert à vérifier.\n\n"
            "Objectifs :\n"
            "- prouver l'origine du message\n"
            "- garantir qu'il n'a pas été modifié\n\n"
            "Limites :\n"
            "- la clé privée doit rester secrète\n"
            "- une signature invalide peut venir d'un fichier modifié, d'une mauvaise clé, ou d'une signature erronée"
        )
        pedagogic.configure(state="disabled")

    def _set_result(self, text: str):
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)

    def generate_keys(self):
        self.private_key, self.public_key = self.asymmetric.generate_keys()
        self._set_result("Clés RSA générées avec succès.")

    def sign_text(self):
        if self.private_key is None:
            messagebox.showerror("Erreur", "Génère d'abord les clés RSA.")
            return

        text = self.text_input.get("1.0", "end").strip()
        if not text:
            messagebox.showerror("Erreur", "Le texte à signer est vide.")
            return

        signature_b64 = self.signature_manager.sign_text(self.private_key, text)
        self._set_result(f"Signature Base64 :\n{signature_b64}")

    def verify_text_signature(self):
        if self.public_key is None:
            messagebox.showerror("Erreur", "Génère d'abord les clés RSA.")
            return

        text = self.text_input.get("1.0", "end").strip()
        signature_b64 = self.result_box.get("1.0", "end").replace("Signature Base64 :", "").strip()

        if not text or not signature_b64:
            messagebox.showerror("Erreur", "Texte ou signature manquant.")
            return

        valid = self.signature_manager.verify_text_signature(self.public_key, text, signature_b64)
        if valid:
            messagebox.showinfo("Résultat", "Signature valide.")
        else:
            messagebox.showerror("Résultat", "Signature invalide.")

    def sign_file(self):
        if self.private_key is None:
            messagebox.showerror("Erreur", "Génère d'abord les clés RSA.")
            return

        filepath = filedialog.askopenfilename(title="Choisir un fichier à signer")
        if not filepath:
            return

        try:
            self.current_signature = self.signature_manager.sign_file(self.private_key, filepath)
            self._set_result("Signature de fichier créée avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de signer le fichier.\n{e}")

    def verify_file_signature(self):
        if self.public_key is None:
            messagebox.showerror("Erreur", "Génère d'abord les clés RSA.")
            return
        if self.current_signature is None:
            messagebox.showerror("Erreur", "Aucune signature de fichier disponible.")
            return

        filepath = filedialog.askopenfilename(title="Choisir le fichier à vérifier")
        if not filepath:
            return

        valid = self.signature_manager.verify_signature(self.public_key, filepath, self.current_signature)
        if valid:
            messagebox.showinfo("Résultat", "Signature fichier valide.")
        else:
            messagebox.showerror("Résultat", "Signature fichier invalide.")
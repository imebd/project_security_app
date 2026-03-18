import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.symmetric import SymmetricCipher
from core.asymmetric import AsymmetricCipher


COLORS = {
    "page": "#F5F3FF",    # violet très pâle pour le fond général
    "card": "#EDE9FE",    # violet clair pour les cartes
    "card2": "#FDF2FA",   # rose très pâle pour les textbox
    "text": "#5B21B6",    # violet foncé pour le texte, lisible sur clair
    "muted": "#A78BFA",   # violet clair pour textes secondaires / labels
    "conf": "#EC4899",    # rose pastel pour accents (optionnel)
    "btn": "#EC4899",     # rose pastel pour boutons
    "btn_hover": "#DB2777", # rose plus foncé au survol
}


class ConfidentialityPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["page"])

        self.symmetric = SymmetricCipher()
        self.asymmetric = AsymmetricCipher()
        self.private_key = None
        self.public_key = None

        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Module Confidentialité",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        left = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        left.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")
        left.grid_columnconfigure((0, 1, 2), weight=1)

        right = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        right.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(left, text="Texte d'entrée", text_color=COLORS["text"], font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=20, pady=(20, 10), sticky="w"
        )

        self.input_text = ctk.CTkTextbox(left, height=140, fg_color=COLORS["card2"], text_color=COLORS["text"])
        self.input_text.grid(row=1, column=0, columnspan=3, padx=20, pady=(0, 12), sticky="nsew")
        self.input_text.insert("1.0", "Bonjour, ceci est un test de chiffrement.")

        self.password_entry = ctk.CTkEntry(left, placeholder_text="Mot de passe AES", width=220)
        self.password_entry.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        self.key_entry = ctk.CTkEntry(left, placeholder_text="Clé AES générée (optionnel)")
        self.key_entry.grid(row=2, column=1, columnspan=2, padx=(0, 20), pady=8, sticky="ew")

        btn_style = {"fg_color": COLORS["btn"], "hover_color": COLORS["btn_hover"], "text_color": "white", "height": 40}

        ctk.CTkButton(left, text="Générer clé AES", command=self.generate_aes_key, **btn_style).grid(row=3, column=0, padx=20, pady=8, sticky="ew")
        ctk.CTkButton(left, text="AES chiffrer", command=self.aes_encrypt_text, **btn_style).grid(row=3, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(left, text="AES déchiffrer", command=self.aes_decrypt_text, **btn_style).grid(row=3, column=2, padx=(8, 20), pady=8, sticky="ew")

        ctk.CTkButton(left, text="Générer clés RSA", command=self.generate_rsa_keys, **btn_style).grid(row=4, column=0, padx=20, pady=8, sticky="ew")
        ctk.CTkButton(left, text="RSA chiffrer", command=self.rsa_encrypt_text, **btn_style).grid(row=4, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(left, text="RSA déchiffrer", command=self.rsa_decrypt_text, **btn_style).grid(row=4, column=2, padx=(8, 20), pady=8, sticky="ew")

        ctk.CTkButton(left, text="Hybride chiffrer", command=self.hybrid_encrypt_text, **btn_style).grid(row=5, column=0, padx=20, pady=8, sticky="ew")
        ctk.CTkButton(left, text="Hybride déchiffrer", command=self.hybrid_decrypt_text, **btn_style).grid(row=5, column=1, padx=8, pady=8, sticky="ew")
        ctk.CTkButton(left, text="Chiffrer fichier AES", command=self.encrypt_file_aes, **btn_style).grid(row=5, column=2, padx=(8, 20), pady=8, sticky="ew")

        ctk.CTkLabel(left, text="Résultat", text_color=COLORS["text"], font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=6, column=0, columnspan=3, padx=20, pady=(18, 10), sticky="w"
        )

        self.output_text = ctk.CTkTextbox(left, height=220, fg_color=COLORS["card2"], text_color=COLORS["text"])
        self.output_text.grid(row=7, column=0, columnspan=3, padx=20, pady=(0, 10), sticky="nsew")

        self.performance_label = ctk.CTkLabel(
            left,
            text="Performance : en attente",
            text_color=COLORS["muted"]
        )
        self.performance_label.grid(row=8, column=0, columnspan=3, padx=20, pady=(0, 20), sticky="w")

        ctk.CTkLabel(right, text="Zone pédagogique", text_color=COLORS["text"], font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w"
        )

        self.pedagogic = ctk.CTkTextbox(right, fg_color=COLORS["card2"], text_color=COLORS["text"])
        self.pedagogic.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.pedagogic.insert(
            "1.0",
            "Confidentialité (CIA)\n"
            "- AES protège rapidement les données avec une clé secrète partagée.\n"
            "- RSA protège surtout l'échange de clé et permet le chiffrement asymétrique.\n"
            "- Le chiffrement hybride combine la vitesse d'AES et la flexibilité de RSA.\n\n"
            "Objectif : garantir que seul le destinataire autorisé puisse lire les données.\n\n"
            "Limites :\n"
            "- AES exige une bonne gestion des mots de passe/clés.\n"
            "- RSA est plus lent et peu adapté aux gros volumes de données.\n"
            "- Le mode hybride est plus réaliste en pratique."
        )
        self.pedagogic.configure(state="disabled")

    def _set_output(self, text: str):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)

    def generate_aes_key(self):
        key = self.symmetric.generate_aes_key()
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, key)
        self._set_output(f"Clé AES générée (Base64) :\n{key}")

    def generate_rsa_keys(self):
        self.private_key, self.public_key = self.asymmetric.generate_keys()
        self._set_output("Paire RSA générée avec succès.\nClé privée et clé publique chargées en mémoire.")

    def aes_encrypt_text(self):
        text = self.input_text.get("1.0", "end").strip()
        password = self.password_entry.get().strip()

        if not text:
            messagebox.showerror("Erreur", "Le texte à chiffrer est vide.")
            return
        if not password:
            messagebox.showerror("Erreur", "Veuillez entrer un mot de passe AES.")
            return

        start = time.perf_counter()
        encrypted = self.symmetric.encrypt_text(text, password)
        duration = (time.perf_counter() - start) * 1000

        self._set_output(encrypted)
        self.performance_label.configure(text=f"Performance : AES chiffrement = {duration:.2f} ms")

    def aes_decrypt_text(self):
        encrypted = self.output_text.get("1.0", "end").strip()
        password = self.password_entry.get().strip()

        if not encrypted:
            messagebox.showerror("Erreur", "Aucun texte chiffré à déchiffrer.")
            return
        if not password:
            messagebox.showerror("Erreur", "Veuillez entrer le mot de passe AES.")
            return

        try:
            start = time.perf_counter()
            decrypted = self.symmetric.decrypt_text(encrypted, password)
            duration = (time.perf_counter() - start) * 1000
            self._set_output(decrypted)
            self.performance_label.configure(text=f"Performance : AES déchiffrement = {duration:.2f} ms")
        except Exception:
            messagebox.showerror("Erreur", "Mot de passe incorrect ou texte chiffré invalide.")

    def rsa_encrypt_text(self):
        if self.public_key is None:
            messagebox.showerror("Erreur", "Génère d'abord la paire RSA.")
            return

        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showerror("Erreur", "Le texte est vide.")
            return

        start = time.perf_counter()
        encrypted = self.asymmetric.encrypt_text(self.public_key, text)
        duration = (time.perf_counter() - start) * 1000

        self._set_output(encrypted)
        self.performance_label.configure(text=f"Performance : RSA chiffrement = {duration:.2f} ms")

    def rsa_decrypt_text(self):
        if self.private_key is None:
            messagebox.showerror("Erreur", "Génère d'abord la paire RSA.")
            return

        encrypted = self.output_text.get("1.0", "end").strip()
        if not encrypted:
            messagebox.showerror("Erreur", "Aucun texte RSA à déchiffrer.")
            return

        try:
            start = time.perf_counter()
            decrypted = self.asymmetric.decrypt_text(self.private_key, encrypted)
            duration = (time.perf_counter() - start) * 1000

            self._set_output(decrypted)
            self.performance_label.configure(text=f"Performance : RSA déchiffrement = {duration:.2f} ms")
        except Exception:
            messagebox.showerror("Erreur", "Clé privée incorrecte ou contenu RSA invalide.")

    def hybrid_encrypt_text(self):
        if self.public_key is None:
            messagebox.showerror("Erreur", "Génère d'abord la paire RSA.")
            return

        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showerror("Erreur", "Le texte est vide.")
            return

        start = time.perf_counter()
        payload = self.asymmetric.hybrid_encrypt_text(self.public_key, text)
        duration = (time.perf_counter() - start) * 1000

        self._set_output(payload)
        self.performance_label.configure(text=f"Performance : Hybride chiffrement = {duration:.2f} ms")

    def hybrid_decrypt_text(self):
        if self.private_key is None:
            messagebox.showerror("Erreur", "Génère d'abord la paire RSA.")
            return

        payload = self.output_text.get("1.0", "end").strip()
        if not payload:
            messagebox.showerror("Erreur", "Aucun contenu hybride à déchiffrer.")
            return

        try:
            start = time.perf_counter()
            plaintext = self.asymmetric.hybrid_decrypt_text(self.private_key, payload)
            duration = (time.perf_counter() - start) * 1000

            self._set_output(plaintext)
            self.performance_label.configure(text=f"Performance : Hybride déchiffrement = {duration:.2f} ms")
        except Exception:
            messagebox.showerror("Erreur", "Contenu hybride invalide ou clé privée incorrecte.")

    def encrypt_file_aes(self):
        password = self.password_entry.get().strip()
        if not password:
            messagebox.showerror("Erreur", "Veuillez entrer un mot de passe AES.")
            return

        input_file = filedialog.askopenfilename(title="Choisir le fichier à chiffrer")
        if not input_file:
            return

        output_file = filedialog.asksaveasfilename(
            title="Enregistrer le fichier chiffré",
            defaultextension=".enc"
        )
        if not output_file:
            return

        try:
            start = time.perf_counter()
            self.symmetric.encrypt_file(input_file, output_file, password)
            duration = (time.perf_counter() - start) * 1000

            self._set_output(f"Fichier AES chiffré avec succès :\n{output_file}")
            self.performance_label.configure(text=f"Performance : AES fichier = {duration:.2f} ms")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du chiffrement du fichier.\n{e}")
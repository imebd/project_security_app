import customtkinter as ctk
from tkinter import messagebox
from core.certificate import CertificateManager


COLORS = {
    "page": "#F5F3FF",       # violet très clair pour le fond
    "card": "#EDE9FE",       # violet clair pour les cartes
    "card2": "#FDF2FA",      # rose pâle pour les textbox
    "text": "#5B21B6",       # violet foncé pour texte
    "btn": "#EC4899",        # rose pastel boutons
    "hover": "#DB2777",      # rose plus foncé au hover
}


class CertificatePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLORS["page"])

        self.cert_manager = CertificateManager()
        self.current_cert = None
        self.current_private_key = None

        self.grid_columnconfigure((0, 1), weight=1, uniform="a")
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Module Certificat",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"]
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")

        left = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        left.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew")

        right = ctk.CTkFrame(self, fg_color=COLORS["card"], corner_radius=18)
        right.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)

        self.cn_entry = ctk.CTkEntry(left, placeholder_text="Nom commun (ex: ensaf.local)")
        self.cn_entry.pack(fill="x", padx=20, pady=(20, 10))

        self.org_entry = ctk.CTkEntry(left, placeholder_text="Organisation (ex: ENSA Fes)")
        self.org_entry.pack(fill="x", padx=20, pady=10)
        self.org_entry.insert(0, "ENSA Fes")

        self.country_entry = ctk.CTkEntry(left, placeholder_text="Pays (ex: MA)")
        self.country_entry.pack(fill="x", padx=20, pady=10)
        self.country_entry.insert(0, "MA")

        self.days_entry = ctk.CTkEntry(left, placeholder_text="Durée de validité en jours")
        self.days_entry.pack(fill="x", padx=20, pady=10)
        self.days_entry.insert(0, "365")

        ctk.CTkButton(
            left,
            text="Générer certificat auto-signé",
            fg_color=COLORS["btn"],
            hover_color=COLORS["hover"],
            command=self.generate_certificate
        ).pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            left,
            text="Afficher informations certificat",
            fg_color=COLORS["btn"],
            hover_color=COLORS["hover"],
            command=self.show_certificate_info
        ).pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkButton(
            left,
            text="Sauvegarder certificat",
            fg_color=COLORS["btn"],
            hover_color=COLORS["hover"],
            command=self.save_certificate_files
        ).pack(fill="x", padx=20, pady=(0, 20))

        self.result_box = ctk.CTkTextbox(left, height=260, fg_color=COLORS["card2"], text_color=COLORS["text"])
        self.result_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        ctk.CTkLabel(
            right,
            text="Zone pédagogique",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        pedagogic = ctk.CTkTextbox(right, fg_color=COLORS["card2"], text_color=COLORS["text"])
        pedagogic.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        pedagogic.insert(
            "1.0",
            "Certificat numérique\n"
            "- Un certificat lie une identité à une clé publique.\n"
            "- Il est utilisé dans HTTPS et dans les systèmes de confiance.\n\n"
            "Objectif : authentifier une entité.\n\n"
            "Lien avec le modèle CIA :\n"
            "- surtout Authenticité et Confiance\n\n"
            "Limites :\n"
            "- Un certificat auto-signé n'a pas le même niveau de confiance\n"
            "  qu'un certificat signé par une autorité de certification réelle.\n"
            "- Il faut protéger la clé privée associée.\n"
            "- Il faut gérer correctement les dates de validité."
        )
        pedagogic.configure(state="disabled")

    def _set_result(self, text: str):
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", text)

    def generate_certificate(self):
        common_name = self.cn_entry.get().strip()
        organization = self.org_entry.get().strip() or "ENSA Fes"
        country = self.country_entry.get().strip() or "MA"
        days_str = self.days_entry.get().strip()

        if not common_name:
            messagebox.showerror("Erreur", "Le nom commun est obligatoire.")
            return

        try:
            days_valid = int(days_str)
        except ValueError:
            messagebox.showerror("Erreur", "La durée de validité doit être un entier.")
            return

        try:
            private_key, cert = self.cert_manager.generate_self_signed_certificate(
                common_name=common_name,
                organization=organization,
                country=country,
                days_valid=days_valid
            )
            self.current_private_key = private_key
            self.current_cert = cert

            self._set_result(
                "Certificat auto-signé généré avec succès.\n\n"
                f"Nom commun : {common_name}\n"
                f"Organisation : {organization}\n"
                f"Pays : {country}\n"
                f"Validité : {days_valid} jours"
            )

            messagebox.showinfo("Succès", "Certificat généré avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de générer le certificat.\n{e}")

    def show_certificate_info(self):
        if self.current_cert is None:
            messagebox.showerror("Erreur", "Aucun certificat généré pour le moment.")
            return

        try:
            info = self.cert_manager.get_certificate_info(self.current_cert)
            self._set_result(info)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'afficher les informations.\n{e}")

    def save_certificate_files(self):
        if self.current_cert is None or self.current_private_key is None:
            messagebox.showerror("Erreur", "Génère d'abord un certificat.")
            return

        try:
            self.cert_manager.save_private_key(self.current_private_key, "cert_private_key.pem")
            self.cert_manager.save_certificate(self.current_cert, "certificate.pem")

            messagebox.showinfo(
                "Succès",
                "Fichiers sauvegardés :\n- cert_private_key.pem\n- certificate.pem"
            )
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de sauvegarder les fichiers.\n{e}")
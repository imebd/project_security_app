import customtkinter as ctk
from gui.confidentiality_page import ConfidentialityPage
from gui.integrity_page import IntegrityPage
from gui.signature_page import SignaturePage
from gui.certificate_page import CertificatePage


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


COLORS = {
    "sidebar": "#F3E8FF",   # mauve pastel clair
    "content": "#FFF5F7",   # fond rose très clair pour la page
    "text": "#5B21B6",      # texte violet foncé pour contraste
    "conf": "#C084FC",      # bouton mauve clair
    "integ": "#F9A8D4",     # bouton rose clair
    "sign": "#9D4EDD",      # bouton violet très clair
    "cert": "#D946EF",      # bouton rose pastel
}


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Application de Cryptographie en Python")
        self.geometry("1360x820")
        self.minsize(1180, 700)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=260, fg_color=COLORS["sidebar"], corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.content = ctk.CTkFrame(self, fg_color=COLORS["content"], corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew")

        title = ctk.CTkLabel(
            self.sidebar,
            text="Projet OpenSSL → Python",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text"]
        )
        title.pack(padx=20, pady=(30, 20), anchor="w")

        self.pages = {
            "Confidentialité": ConfidentialityPage(self.content),
            "Intégrité": IntegrityPage(self.content),
            "Signature": SignaturePage(self.content),
            "Certificat": CertificatePage(self.content),
        }

        for page in self.pages.values():
            page.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkButton(
            self.sidebar,
            text="Confidentialité",
            fg_color=COLORS["conf"],
            hover_color="#A855F7",
            height=42,
            command=lambda: self.show_page("Confidentialité")
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Intégrité",
            fg_color=COLORS["integ"],
            hover_color="#EC4899",
            height=42,
            command=lambda: self.show_page("Intégrité")
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Signature",
            fg_color=COLORS["sign"],
            hover_color="#C084FC",
            height=42,
            command=lambda: self.show_page("Signature")
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.sidebar,
            text="Certificat",
            fg_color=COLORS["cert"],
            hover_color="#F472B6",
            height=42,
            command=lambda: self.show_page("Certificat")
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkLabel(
            self.sidebar,
            text="Apparence",
            text_color=COLORS["text"],
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=20, pady=(30, 8), anchor="w")

        self.appearance_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["System", "Light", "Dark"],
            command=self.change_appearance
        )
        self.appearance_menu.set("System")
        self.appearance_menu.pack(fill="x", padx=20, pady=(0, 20))

        self.show_page("Confidentialité")

    def show_page(self, name: str):
        self.pages[name].lift()

    def change_appearance(self, mode: str):
        ctk.set_appearance_mode(mode)
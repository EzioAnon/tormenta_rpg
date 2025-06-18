from tkinter import ttk
from data.pericias import TODAS_PERICIAS

class CharacterSheet:
    def __init__(self, parent, personagem):
        self.personagem = personagem
        self.create_pericias_tab()

    def create_pericias_tab(self):
        frame = ttk.Frame(self.parent)
        
        for i, pericia in enumerate(TODAS_PERICIAS):
            lbl = ttk.Label(frame, text=f"{pericia.nome}:")
            lbl.grid(row=i, column=0, sticky="e")
            
            modificador = self.personagem.calcular_modificador_pericia(pericia.nome)
            val = ttk.Label(frame, text=f"{modificador:+}")
            val.grid(row=i, column=1)
            
            # Adicione checkboxes para perícias treinadas se necessário
import json
import os
from personagem import Personagem

def salvar_personagens(personagens, arquivo='personagens.json'):
    with open(arquivo, 'w') as f:
        json.dump([p.to_dict() for p in personagens], f, indent=2)

def carregar_personagens(arquivo='personagens.json'):
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as f:
            data = json.load(f)
            return [Personagem.from_dict(p) for p in data]
    return []
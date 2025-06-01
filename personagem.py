from enum import Enum
from typing import Dict, List
#oiiii
class Raca(Enum):
    HUMANO = "Humano"  # +2 em 3 atributos diferentes
    ANAO = "Anão"
    DAHLLAN = "Dahllan"
    ELFO = "Elfo"
    GOBLIN = "Goblin"
    LEFOU = "Lefou"  # +2 em 3 atributos diferentes (exceto Carisma)
    MINOTAURO = "Minotauro"
    QAREEN = "Qareen"
    GOLEM = "Golem"
    HYNNE = "Hynne"
    KLIREN = "Kliren"
    MEDUSA = "Medusa"
    OSTEON = "Osteon"  # +2 em 3 atributos diferentes (exceto Constituição)
    SEREIA = "Sereia/Tritão"  # +2 em 3 atributos diferentes
    SILFIDE = "Sílfide"
    SURAGGEL = "Suraggel"
    TROG = "Trog"

class Classe(Enum):
    GUERREIRO = "Guerreiro"
    MAGO = "Mago"
    LADINO = "Ladino"
    CLERIGO = "Clérigo"

# Modificadores fixos (para raças sem escolha de atributos)
MODIFICADORES_RACA_FIXOS = {
    Raca.ANAO: {'constituicao': 4, 'sabedoria': 2, 'destreza': -2},
    Raca.DAHLLAN: {'sabedoria': 4, 'destreza': 2, 'inteligencia': -2},
    Raca.ELFO: {'inteligencia': 4, 'destreza': 2, 'constituicao': -2},
    Raca.GOBLIN: {'destreza': 4, 'inteligencia': 2, 'carisma': -2},
    Raca.LEFOU: {'carisma': -2},  # +2 em 3 atributos será adicionado depois
    Raca.MINOTAURO: {'forca': 4, 'constituicao': 2, 'sabedoria': -2},
    Raca.QAREEN: {'carisma': 4, 'inteligencia': 2, 'sabedoria': -2},
    Raca.GOLEM: {'forca': 4, 'constituicao': 2, 'carisma': -2},
    Raca.HYNNE: {'destreza': 4, 'carisma': 2, 'forca': -2},
    Raca.KLIREN: {'inteligencia': 4, 'carisma': 2, 'forca': -2},
    Raca.MEDUSA: {'destreza': 4, 'carisma': 2},
    Raca.OSTEON: {'constituicao': -2},  # +2 em 3 atributos será adicionado depois
    Raca.SILFIDE: {'carisma': 4, 'destreza': 2, 'forca': -4},
    Raca.SURAGGEL: {'sabedoria': 4, 'destreza': 4, 'carisma': 2, 'inteligencia': 2},
    Raca.TROG: {'constituicao': 4, 'forca': 2, 'inteligencia': -2}
}

MODIFICADORES_CLASSE = {
    Classe.GUERREIRO: {'forca': 2, 'constituicao': 1},
    Classe.MAGO: {'inteligencia': 2, 'sabedoria': 1},
    Classe.LADINO: {'destreza': 2, 'carisma': 1},
    Classe.CLERIGO: {'sabedoria': 2, 'carisma': 1}
}

class Personagem:
    @staticmethod
    def calcular_modificador(valor):
        if valor == 1:
            return -5
        elif 2 <= valor <= 3:
            return -4
        elif 4 <= valor <= 5:
            return -3
        elif 6 <= valor <= 7:
            return -2
        elif 8 <= valor <= 9:
            return -1
        elif 10 <= valor <= 11:
            return 0
        elif 12 <= valor <= 25:
            return (valor - 10) // 2
        else:
            return 7 + (valor - 26) // 2
    
    def __init__(self, nome, raca, classe, atributos_base, atributos_escolhidos=None, nivel=1, ouro=0):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.nivel = nivel
        self.ouro = ouro
        self.atributos_base = atributos_base
        self.atributos_escolhidos = atributos_escolhidos or {}
        self.atributos = self.calcular_atributos_finais()
        self.habilidades = []
        self.equipamentos = []
    
    def calcular_atributos_finais(self):
        atributos_finais = self.atributos_base.copy()
        
        # Aplica modificadores fixos
        for atributo, bonus in MODIFICADORES_RACA_FIXOS.get(self.raca, {}).items():
            atributos_finais[atributo] += bonus
        
        # Aplica modificadores escolhidos para raças especiais
        for atributo, bonus in self.atributos_escolhidos.items():
            atributos_finais[atributo] += bonus
        
        # Aplica bônus de classe
        for atributo, bonus in MODIFICADORES_CLASSE.get(self.classe, {}).items():
            atributos_finais[atributo] += bonus
            
        return atributos_finais
    
    def get_modificador(self, atributo):
        return self.calcular_modificador(self.atributos[atributo])
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'raca': self.raca.value,
            'classe': self.classe.value,
            'nivel': self.nivel,
            'ouro': self.ouro,
            'atributos_base': self.atributos_base,
            'atributos_escolhidos': self.atributos_escolhidos,
            'atributos': self.atributos,
            'habilidades': self.habilidades,
            'equipamentos': self.equipamentos
        }
    
    @classmethod
    def from_dict(cls, data):
        raca = Raca(data['raca'])
        classe = Classe(data['classe'])
        personagem = cls(
            data['nome'],
            raca,
            classe,
            data['atributos_base'],
            data.get('atributos_escolhidos', {}),
            data['nivel'],
            data['ouro']
        )
        personagem.habilidades = data['habilidades']
        personagem.equipamentos = data['equipamentos']
        return personagem
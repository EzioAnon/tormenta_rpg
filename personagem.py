from enum import Enum

class Raca(Enum):
    HUMANO = "Humano"
    ELFO = "Elfo"
    ANAO = "Anão"
    HALFLING = "Halfling"

class Classe(Enum):
    GUERREIRO = "Guerreiro"
    MAGO = "Mago"
    LADINO = "Ladino"
    CLERIGO = "Clérigo"

MODIFICADORES_RACA = {
    Raca.HUMANO: {'forca': 1, 'destreza': 1, 'constituicao': 1, 'inteligencia': 1, 'sabedoria': 1, 'carisma': 1},
    Raca.ELFO: {'destreza': 2, 'inteligencia': 1, 'constituicao': -1},
    Raca.ANAO: {'constituicao': 2, 'forca': 1, 'carisma': -1},
    Raca.HALFLING: {'destreza': 2, 'carisma': 1, 'forca': -1}
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
            return - 5
        elif 2 <= valor <= 3:
            return -4
        elif 4 <= valor <= 5:
            return -3
        elif 6 <= valor <= 7:
            return -2
        elif 8 <= valor <= 9:
            return -1
        elif 10 <= valor <= 25:
            return (valor - 10)//2
        else:
            return 10//2
    def __init__(self, nome, raca, classe, atributos_base, nivel=1, ouro=0):
        """
        atributos_rolados: dict com valores rolados para cada atributo
        Exemplo: {'forca': 15, 'destreza': 12, ...}
        """
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.nivel = nivel
        self.ouro = ouro
        self.atributos_base = atributos_base
        self.atributos = self.calcular_atributos_finais()
        self.habilidades = []
        self.equipamentos = []
    
    def calcular_atributos_finais(self):
        """Aplica modificadores de raça e classe aos valores base"""
        atributos_finais = self.atributos_base.copy()

        for atributo, bonus in MODIFICADORES_RACA.get(self.raca, {}).items():
            atributos_finais[atributo] += bonus
        for atributo, bonus in MODIFICADORES_CLASSE.get(self.classe, {}).items():
            atributos_finais[atributo] += bonus
        
        return atributos_finais

    def get_modificador(self, atributo):
        """Retorna o modificador para um atributo específico"""
        return self.calcular_modificador(self.atributos[atributo])
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'raca': self.raca.value,
            'classe': self.classe.value,
            'nivel': self.nivel,
            'ouro': self.ouro,
            'atributos_base': self.atributos_base,
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
            data['nivel'], 
            data['ouro']
        )
        personagem.habilidades = data['habilidades']
        personagem.equipamentos = data['equipamentos']
        return personagem
from enum import Enum

class Raca(Enum):
    HUMANO = "Humano"#mecanis diferentes
    ANAO = "Anão"
    DAHLLAN = "Dahllan"
    ELFO = "Elfo"
    GOBLIN = "Goblin"
    LEFOU = "Lefou"#mecanis diferentes
    MINOTAURO = "Minotauro"
    QAREEN = "Qareen"
    GOLEM = "Golem"
    HYNNE = "Hynne"
    KLIREN = "Kliren"
    MEDUSA = "Medusa"
    OSTEON = "Osteon"#mecanis diferentes
    SEREIA = "Sereia/Tritão"#mecanis diferentes
    SILFIDE = "Sílfide"
    SURAGGEL = "Suraggel"#mecanis diferentes
    TROG = "Trog"


class Classe(Enum):
    GUERREIRO = "Guerreiro"
    MAGO = "Mago"
    LADINO = "Ladino"
    CLERIGO = "Clérigo"

MODIFICADORES_RACA = {
    Raca.HUMANO: {},#+2 em 3 atributos diferentes
    Raca.ANAO: {'constituicao': 4, 'sabedoria': 2, 'destreza': -2},
    Raca.DAHLLAN: {'sabedoria': 4,'destreza': 2, 'inteligencia': -2},
    Raca.ELFO: {'inteligencia': 4, 'destreza':2,'constituicao': -2},
    Raca.GOBLIN:{'destreza': 4, 'inteligencia': 2, 'carisma': -2},
    Raca.LEFOU: {'carisma':-2},# +2 em tres atributos diferentes
    Raca.MINOTAURO:{'forca': 4, 'constituicao': 2, 'sabedoria': -2},
    Raca.QAREEN: {'carisma': 4, 'inteligencia': 2, 'sabedoria': -2},
    Raca.GOLEM: {'forca': 4, 'constituicao': 2, 'carisma': -2},
    Raca.HYNNE: {'destreza': 4, 'carisma': 2, 'forca': -2},
    Raca.KLIREN: {'inteligencia': 4, 'carisma': 2, 'forca': -2},
    Raca.MEDUSA: {'destreza': 4, 'carisma': 2},
    Raca.OSTEON: {'constituicao': -2},# +2 em tres atributos, menos const.
    Raca.SEREIA: {},# +2 em tres atributos diferentes
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
            return - 5
        elif 2 <= valor <= 3:
            return -4
        elif 4 <= valor <= 5:
            return -3
        elif 6 <= valor <= 7:
            return -2
        elif 8 <= valor <= 9:
            return -1
        elif 10 <= valor <= 11:
            return -1
        elif 12 <= valor <= 25:
            return (valor - 10)//2
        else:
            return 7 + (valor - 26)//2
    
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
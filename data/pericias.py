from enum import Enum
from data.enums import AtributoChave  # Você precisará criar este Enum
from data.enums import Classe
class Pericia:
    def __init__(self, nome, atributo_chave, requer_treinamento=False, penalidade_armadura=False):
        self.nome = nome
        self.atributo_chave = atributo_chave
        self.requer_treinamento = requer_treinamento
        self.penalidade_armadura = penalidade_armadura

# Lista completa de perícias (adaptar para seu sistema)
TODAS_PERICIAS = [
    Pericia("Acrobacia", AtributoChave.DESTREZA, penalidade_armadura=True),
    Pericia("Adestramento", AtributoChave.CARISMA,requer_treinamento = True),
    Pericia("Atletismo", AtributoChave.FORCA),
    Pericia("Atuação",AtributoChave.CARISMA),
    Pericia("Cavalgar",AtributoChave.DESTREZA),
    Pericia("Conhecimento", AtributoChave.INTELIGENCIA, requer_treinamento=True),
    Pericia("Cura",AtributoChave.SABEDORIA),
    Pericia("Diplomacia",AtributoChave.CARISMA),
    Pericia("Enganação",AtributoChave.CARISMA),
    Pericia("Fortitude",AtributoChave.CONSTITUICAO),
    Pericia("Furtividade",AtributoChave.DESTREZA, penalidade_armadura = True),
    Pericia("Guerra",AtributoChave.INTELIGENCIA, requer_treinamento = True),
    Pericia("Iniciativa",AtributoChave.DESTREZA),
    Pericia("Intimidação",AtributoChave.CARISMA),
    Pericia("Intuição",AtributoChave.SABEDORIA),
    Pericia("Investigação",AtributoChave.INTELIGENCIA),
    Pericia("Jogatina",AtributoChave.CARISMA, requer_treinamento = True),
    Pericia("Ladinagem",AtributoChave.DESTREZA, requer_treinamento = True, penalidade_armadura = True),
    Pericia("Luta",AtributoChave.FORCA),
    Pericia("Misticismo",AtributoChave.INTELIGENCIA, requer_treinamento = True),
    Pericia("Nobreza",AtributoChave.INTELIGENCIA, requer_treinamento = True),
    Pericia("Ofício",AtributoChave.INTELIGENCIA, requer_treinamento = True),
    Pericia("Percepção",AtributoChave.SABEDORIA),
    Pericia("Pilotagem",AtributoChave.DESTREZA, requer_treinamento = True),
    Pericia("Pontaria",AtributoChave.DESTREZA),
    Pericia("Reflexos",AtributoChave.DESTREZA),
    Pericia("Religião",AtributoChave.SABEDORIA,requer_treinamento = True),
    Pericia("Sobrevivência",AtributoChave.SABEDORIA),
    Pericia("Vontade",AtributoChave.SABEDORIA),
    

    
]
PERICIAS_POR_NOME = {p.nome: p for p in TODAS_PERICIAS}

PERICIAS_POR_CLASSE = {
    
    'Arcanista': {
        'fixas': [
            'Misticismo',
            'Vontade'
        ],
        'escolhas': [
            'Conhecimento',
            'Iniciativa',
            'Ofício',
            'Percepção'
        ],
        'quantidade_escolhas': 1
    },
    'Bárbaro': {
        'fixas': [
            'Fortitude',
            'Luta'
        ],
        'escolhas': [
            'Adestramento',
            'Atletismo',
            'Cavalgar',
            'Iniciativa',
            'Intimidação',
            'Ofício',
            'Percepção',
            'Pontaria',
            'Sobrevivência',
            'Vontade'
        ],
        'quantidade_escolhas': 4
    },
    'Bardo': {
        'fixas': [
            'Atuação',
            'Reflexos'
        ],
        'escolhas': [
            'Acrobacia',
            'Cavalgar',
            'Conhecimento',
            'Diplomacia',
            'Enganação',
            'Furtividade',
            'Iniciativa',
            'Intuição',
            'Investigação',
            'Jogatina',
            'Ladinagem',
            'Luta',
            'Misticismo',
            'Nobreza',
            'Percepção',
            'Pontaria',
            'Religião',
            'Vontade'
        ],
        'quantidade_escolhas': 6
    },
    'Bucaneiro': {
        'fixas': [
            {'escolha': ['Luta', 'Pontaria'],
             'quantidade': 1},
            'Reflexos'
        ],
        'escolhas': [
            'Acrobacia',
            'Atletismo',
            'Atuação',
            'Enganação',
            'Fortitude',
            'Furtividade',
            'Iniciativa',
            'Intimidação',
            'Jogatina',
            'Luta',
            'Ofício',
            'Percepção',
            'Pilotagem',
            'Pontaria'
        ],
        'quantidade_escolhas': 4
    },
    'Caçador': {
        'fixas': [
            {'escolha': ['Luta', 'Pontaria'],
             'quantidade': 1},
            'Sobrevivência'
        ],
        'escolhas': [
            'Adestramento',
            'Atletismo',
            'Cavalgar',
            'Cura',
            'Fortitude',
            'Furtividade',
            'Iniciativa',
            'Investigação',
            'Luta',
            'Ofício',
            'Percepção',
            'Pontaria',
            'Reflexos'
        ],
        'quantidade_escolhas': 6
    },
    'Clérigo': {
        'fixas': [
            'Religião',
            'Vontade'
        ],
        'escolhas': [
            'Conhecimento',
            'Cura',
            'Diplomacia',
            'Fortitude',
            'Iniciativa',
            'Intuição',
            'Luta',
            'Misticismo',
            'Nobreza',
            'Ofício',
            'Percepção'
        ],
        'quantidade_escolhas': 2
    },
    'Druida': {
        'fixas': [
            'Sobrevivência',
            'Vontade'
        ],
        'escolhas': [
            'Adestramento',
            'Atletismo',
            'Cavalgar',
            'Conhecimento',
            'Cura',
            'Fortitude',
            'Iniciativa',
            'Intuição',
            'Luta',
            'Misticismo',
            'Ofício',
            'Percepção',
            'Religião'
        ],
        'quantidade_escolhas': 4
    },
    'Guerreiro': {
        'fixas': [
            'Fortitude',
            {'escolha': ['Luta', 'Pontaria'],
             'quantidade': 1}
        ],
        'escolhas': [
            'Adestramento',
            'Atletismo',
            'Cavalgar',
            'Guerra',
            'Iniciativa',
            'Intimidação',
            'Luta',
            'Ofício',
            'Percepção',
            'Pontaria',
            'Reflexos'
        ],
        'quantidade_escolhas': 2
    },
    'Inventor': {
        'fixas': [
            'Ofício',
            'Vontade'
        ],
        'escolhas': [
            'Conhecimento',
            'Cura',
            'Diplomacia',
            'Fortitude',
            'Iniciativa',
            'Investigação',
            'Luta',
            'Misticismo',
            'Ofício',
            'Pilotagem',
            'Pontaria',
            'Percepção'
        ],
        'quantidade_escolhas': 4
    },
    'Ladino': {
        'fixas': [
            'Ladinagem',
            'Reflexos'
        ],
        'escolhas': [
            'Acrobacia',
            'Atletismo',
            'Atuação',
            'Cavalgar',
            'Conhecimento',
            'Diplomacia',
            'Enganação',
            'Furtividade',
            'Iniciativa',
            'Intimidação',
            'Intuição',
            'Investigação',
            'Jogatina',
            'Luta',
            'Ofício',
            'Percepção',
            'Pilotagem',
            'Pontaria'
        ],
        'quantidade_escolhas': 8
    },
    'Lutador': {
        'fixas': [
            'Fortitude',
            'Luta'
        ],
        'escolhas': [
            'Acrobacia',
            'Adestramento',
            'Atletismo',
            'Enganação',
            'Furtividade',
            'Iniciativa',
            'Intimidação',
            'Ofício',
            'Percepção',
            'Pontaria',
            'Reflexos'
        ],
        'quantidade_escolhas': 4
    },
    'Nobre': {
        'fixas': [
            {'escolha': ['Diplomacia', 'Intimidação'],
             'quantidade': 1},
            'Vontade'
        ],
        'escolhas': [
            'Adestramento',
            'Atuação',
            'Cavalgar',
            'Conhecimento',
            'Enganação',
            'Fortitude',
            'Guerra',
            'Iniciativa',
            'Intuição',
            'Investigação',
            'Jogatina',
            'Luta',
            'Nobreza',
            'Ofício',
            'Percepção',
            'Pontaria'
        ],
        'quantidade_escolhas': 4
    },
    'Paladino': {
        'fixas': [
            'Luta',
            'Vontade'
        ],
        'escolhas': [
            'Adestramento',
            'Atletismo',
            'Cavalgar',
            'Cura',
            'Diplomacia',
            'Fortitude',
            'Guerra',
            'Iniciativa',
            'Intuição',
            'Nobreza',
            'Percepção',
            'Religião'
        ],
        'quantidade_escolhas': 2
    }
}

def get_pericias_classe(classe_enum):
    return PERICIAS_POR_CLASSE.get(classe_enum.value, {})
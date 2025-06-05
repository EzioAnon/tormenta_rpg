from .enums import Raca, Classe

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
    Classe.ARCANISTA : {
        'pv': {'base': 8,  'por_nivel': 2},
        'pm': {'base': 0, 'por_nivel': 6} #PM BASE VARIA, FALTA ADICIONAR ESSE MECANICA
    },
    Classe.BARBARO : {
        'pv': {'base': 24,  'por_nivel': 6},
        'pm': {'base': 0, 'por_nivel': 3}
        },
    Classe.BARDO : {
        'pv': {'base': 12,  'por_nivel': 3},
        'pm': {'base': 0, 'por_nivel': 4}
        },
    Classe.BUCANEIRO : {
        'pv': {'base': 16,  'por_nivel': 4},
        'pm': {'base': 0, 'por_nivel': 3}
        },
    Classe.CACADOR: {
        'pv': {'base': 16,  'por_nivel': 4},
        'pm': {'base': 0, 'por_nivel': 4}
        },
    Classe.CAVALEIRO: {
        'pv': {'base': 20,  'por_nivel': 5},
        'pm': {'base': 0, 'por_nivel': 3}
        },  
    Classe.CLERIGO: {
        'pv': {'base': 16,  'por_nivel': 4},
        'pm': {'base': 0, 'por_nivel': 5}
        },  
    Classe.DRUIDA: {
        'pv': {'base': 16,  'por_nivel': 4},
        'pm': {'base': 0, 'por_nivel': 4}
        },         
    Classe.GUERREIRO : {
        'pv': {'base': 20,  'por_nivel': 5},
        'pm': {'base': 0, 'por_nivel': 3}
        },
    Classe.INVENTOR: {
        'pv': {'base': 12,  'por_nivel': 3},
        'pm': {'base': 0, 'por_nivel': 4}
        },
    Classe.LADINO: {
        'pv': {'base': 12,  'por_nivel': 3},
        'pm': {'base': 0, 'por_nivel': 4}
        },
    Classe.LUTADOR: {
        'pv': {'base': 20,  'por_nivel': 5},
        'pm': {'base': 0, 'por_nivel': 3}
        },
    Classe.NOBRE: {
        'pv': {'base': 16,  'por_nivel': 4},
        'pm': {'base': 0, 'por_nivel': 4}
        },
    Classe.PALADINO: {
        'pv': {'base': 20,  'por_nivel': 5},
        'pm': {'base': 0, 'por_nivel': 3}
        },
}
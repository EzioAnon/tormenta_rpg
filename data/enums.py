from enum import Enum

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
    ARCANISTA = "Arcanista"
    BARBARO = "Bárbaro"
    BARDO = "Bardo"
    BUCANEIRO = "Bucaneiro"
    CACADOR = "Caçador"
    CAVALEIRO = "Cavaleiro"
    CLERIGO = "Clérigo"
    DRUIDA = "Druida"
    GUERREIRO = "Guerreiro"
    INVENTOR = "Inventor"
    LADINO = "Ladino"
    LUTADOR = "Lutador"
    NOBRE = "Nobre"
    PALADINO = "Paladino"
   
class AtributoChave(Enum):
    FORCA = "Força"
    DESTREZA = "Destreza"
    CONSTITUICAO = "Constituição"
    INTELIGENCIA = "Inteligência"
    SABEDORIA = "Sabedoria"
    CARISMA = "Carisma"
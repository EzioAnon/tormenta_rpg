from data.enums import Raca, Classe
from data.modificadores import MODIFICADORES_RACA_FIXOS, MODIFICADORES_CLASSE
from data.tabelas import TABELA_XP



class Personagem:
    TABELA_XP = TABELA_XP
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
    
    def __init__(self, nome, raca, classe, atributos_base, atributos_escolhidos=None, nivel=1, ouro=0, xp = 0):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.nivel = nivel
        self.ouro = ouro
        self.xp = xp
        self.atributos_base = atributos_base
        self.atributos_escolhidos = atributos_escolhidos or {}
        self.atributos = self.calcular_atributos_finais()
        self.habilidades = []
        self.equipamentos = []
        self.pv_max = self.calcular_pv_max()
        self.pm_max = self.calcular_pm_max()
        self.pv_atual = self.pv_max
        self.pm_atual = self.pm_max
    


    def calcular_atributos_finais(self):
        atributos_finais = self.atributos_base.copy()
        
        # Aplica modificadores fixos
        for atributo, bonus in MODIFICADORES_RACA_FIXOS.get(self.raca, {}).items():
            atributos_finais[atributo] += bonus
        
        # Aplica modificadores escolhidos para raças especiais
        for atributo, bonus in self.atributos_escolhidos.items():
            atributos_finais[atributo] += bonus
   
        return atributos_finais
    
    def calcular_pv_max(self):
        modificador_const = self.get_modificador('constituicao')
        pv_base = MODIFICADORES_CLASSE[self.classe]['pv']['base']
        pv_por_nivel = MODIFICADORES_CLASSE[self.classe]['pv']['por_nivel']
        return pv_base + modificador_const + (pv_por_nivel * (self.nivel - 1))
    
    def calcular_pm_max(self):
        pm_base = MODIFICADORES_CLASSE[self.classe]['pm']['base']
        pm_por_nivel = MODIFICADORES_CLASSE[self.classe]['pm']['por_nivel']
        return pm_base  + (pm_por_nivel * (self.nivel - 1))
    
    def adicionar_xp(self,  quantidade):
        self.xp += quantidade
        self.calcular_nivel_por_xp()

    
    def verificar_subida_nivel(self, novo_nivel):
        novo_nivel = self.calcular_nivel_atual()

        if novo_nivel > self.nivel:
            niveis_ganhos = novo_nivel - self.nivel
            self.subir_de_nivel(niveis_ganhos)
    
    def calcular_nivel_atual(self):
        for nivel, xp_necessario in enumerate(self.TABELA_XP, start=1):
            if self.xp < xp_necessario:
                return nivel -1
        return len(self.TABELA_XP)
    
    def subir_de_nivel(self, niveis_ganhos = 1):
        nivel_anterior = self.nivel
        self.nivel += niveis_ganhos    
    
        # Atualiza PV e PM máximos
        pv_antes = self.pv_max
        pm_antes = self.pm_max
    
        self.pv_max = self.calcular_pv_max()
        self.pm_max = self.calcular_pm_max()
    
        # Ajusta os valores atuais proporcionalmente
        self.pv_atual = max(1, self.pv_atual + (self.pv_max - pv_antes))
        self.pm_atual = max(0, self.pm_atual + (self.pm_max - pm_antes))
        


    
    def get_modificador(self, atributo):
        return self.calcular_modificador(self.atributos[atributo])
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'raca': self.raca.value,
            'classe': self.classe.value,
            'nivel': self.nivel,
            'ouro': self.ouro,
            'xp':self.xp,
            'atributos_base': self.atributos_base,
            'atributos_escolhidos': self.atributos_escolhidos,
            'atributos': self.atributos,
            'habilidades': self.habilidades,
            'equipamentos': self.equipamentos,
            'equipamentos': self.equipamentos,
            'pv_max': self.pv_max,
            'pm_max': self.pm_max,
            'pv_atual': self.pv_atual,
            'pm_atual': self.pm_atual

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
            data['ouro'],
            data.get('xp', 0)
        )
        personagem.habilidades = data['habilidades']
        personagem.equipamentos = data['equipamentos']
        personagem.pv_max = data.get('pv_max', personagem.calcular_pv_max())
        personagem.pm_max = data.get('pm_max', personagem.calcular_pm_max())
        personagem.pv_atual = data.get('pv_atual', personagem.pv_max)
        personagem.pm_atual = data.get('pm_atual', personagem.pm_max)

        return personagem
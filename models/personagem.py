from data.enums import Raca,Classe
from data.modificadores import MODIFICADORES_RACA_FIXOS, MODIFICADORES_CLASSE
from data.tabelas import TABELA_XP
from data.pericias import TODAS_PERICIAS, PERICIAS_POR_NOME


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
        self.pericias_treinadas = set()
        self.pericias_extras = set()
        self.pericias_classe = {
            'fixas': set(),
            'escolhidas': set(),
            'escolhas_obrigatorias': [],
            'quantidade_escolhas_obrigatorias': 0
        }
        self.bonus_int_pericias = self.calcular_bonus_int_pericias()
        self.penalidade_armadura = False
    
    def calcular_bonus_int_pericias(self):
        modificador_int = self.get_modificador('inteligencia')
        return max(0, modificador_int)
    
    def adicionar_pericia_treinada(self, nome_pericia):
     """Adiciona uma perícia à lista de treinadas (unifica todas as origens)"""
    
     # Verifica se é uma perícia fixa ou escolhida da classe
     if nome_pericia in self.pericias_classe.get('fixas', set()):
        self.pericias_treinadas.add(nome_pericia)
        return
    
     # 2. Verifica se é escolha da classe
     if nome_pericia in self.pericias_classe.get('escolhidas', set()):
         self.pericias_treinadas.add(nome_pericia)
         return
     
     # Verifica se é uma perícia extra por inteligência
     bonus = self.calcular_bonus_int_pericias()
     if len(self.pericias_extras) >= bonus:
        raise ValueError(f"Limite de {self.bonus_int_pericias} pericias extras") 
     
     self.pericias_extras.add(nome_pericia)
     self.pericias_treinadas.add(nome_pericia)
    
    
    def todas_pericias_treinadas(self):
        """Retorna todas as perícias treinadas"""
        fixas = self.pericias_classe.get('fixas', set())
        escolhidas = self.pericias_classe.get('escolhidas', set())
        extras = {p.nome if hasattr(p, 'nome') else p for p in self.pericias_extras}
        return fixas.union(escolhidas).union(extras)

    
    def definir_pericias_iniciais(self):
        from data.pericias import PERICIAS_POR_CLASSE
        classe_info = PERICIAS_POR_CLASSE.get(self.classe,{})
        self.pericias_classe = {
            'fixas': set(classe_info.get('fixas',[])),
            'escolhidas': classe_info.get('escolhas',[]),
            'quantidade_escolhas': classe_info.get('quantidade_escolhas', 0),
            'extras': set()

        }
          
    
    def escolher_pericias_iniciais(self, escolhas_fixas, escolhas_normais):
        """
        escolhas_fixas: Lista de perícias escolhidas das opções obrigatórias
        escolhas_normais: Lista de perícias escolhidas das opções normais
        """
        # Valida escolhas obrigatórias
        obrigatorias = self.pericias_classe.get('escolhas_obrigatorias', [])
        qtd_obrigatoria = self.pericias_classe.get('quantidade_escolhas_obrigatorias', 0)
        
        if len(escolhas_fixas) != qtd_obrigatoria:
            raise ValueError(f"Deve escolher {qtd_obrigatoria} perícias obrigatórias")
            
        for nome in escolhas_fixas:
            if nome not in [p.nome for p in obrigatorias]:
                raise ValueError(f"{nome} não é uma opção válida")
            self.pericias_classe['fixas'].add(nome)
        
        # Valida escolhas normais
        qtd_normal = PERICIAS_POR_NOME[self.classe]['quantidade_escolhas']
        if len(escolhas_normais) != qtd_normal:
            raise ValueError(f"Deve escolher {qtd_normal} perícias normais")
            
        for nome in escolhas_normais:
            if nome not in [p.nome for p in PERICIAS_POR_NOME[self.classe]['escolhas']]:
                raise ValueError(f"{nome} não é uma perícia válida para esta classe")
            self.pericias_classe['escolhidas'].add(nome)
   
    def adicionar_pericia_extra(self, nome_pericia):
        """Adiciona uma perícia extra baseada em Inteligência"""
        if len(self.pericias_extras) >= self.bonus_int_pericias:
            raise ValueError("Número máximo de perícias extras atingido")
        self.pericias_extras.add(nome_pericia)
    
    def atualizar_pericias_inteligencia(self, novo_modificador):
        """Atualiza quando o modificador de Int aumenta permanentemente"""
        novo_bonus = max(0, novo_modificador)
        diferenca = novo_bonus - self.bonus_int_pericias
        
        if diferenca > 0:
            self.bonus_int_pericias = novo_bonus
            return diferenca   
        return 0
    
    def validar_pericias_obrigatorias(self):
     """Verifica se todas as escolhas obrigatórias foram feitas"""
     obrigatorias = self.pericias_classe.get('escolhas_obrigatorias', [])
     qtd_obrigatoria = self.pericias_classe.get('quantidade_escolhas_obrigatorias', 0)
    
     # Conta quantas das obrigatórias foram selecionadas
     selecionadas = sum(1 for p in obrigatorias if p in self.pericias_treinadas)
     return selecionadas >= qtd_obrigatoria

    def atualizar_pericias_por_inteligencia(self, novo_modificador_int):
        """Ajusta perícias extras quando Inteligência aumenta permanentemente"""
        bonus_atual = self.calcular_bonus_int_pericias()
        novo_bonus = max(0, novo_modificador_int)
    
        if novo_bonus > bonus_atual:
            return novo_bonus - bonus_atual  # Retorna quantas novas pode adicionar
        return 0
    
    
    def todas_pericias_treinadas(self):
        """Retorna todas as perícias treinadas"""
        return (self.pericias_classe['fixas'] | 
                self.pericias_classe['escolhidas'] | 
                self.pericias_extras)

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
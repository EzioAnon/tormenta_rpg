import tkinter as tk
from tkinter import ttk, messagebox
from data.pericias import get_pericias_classe, PERICIAS_POR_NOME, Pericia

class PericiasWindow(tk.Toplevel):
    def __init__(self, parent, personagem, callback=None):
        super().__init__(parent)
        self.personagem = personagem
        self._callback = callback
        self.vars = {}  # Dicionário para armazenar as variáveis das checkboxes
        self.pericias_obrigatorias_selecionadas = []
        self.pericias_extras_selecionadas = []
        
        self.title("Selecionar Perícias")
        self.geometry("700x500")
        
        self.carregar_pericias()
        self.criar_interface()
    
    def criar_interface(self):
        notebook = ttk.Notebook(self)
        
        # Frame para perícias da classe
        frame_classe = ttk.Frame(notebook)
        pericias_classe = get_pericias_classe(self.personagem.classe)
        self.criar_frame_pericias(frame_classe, "Perícias da Classe", pericias_classe)
        notebook.add(frame_classe, text="Classe")
        
        # Frame para perícias extras (se aplicável)
        if getattr(self.personagem, 'bonus_int_pericias', 0) > 0:
         frame_extras = ttk.Frame(notebook)
         pericias_treinadas = self.personagem.todas_pericias_treinadas()
         pericias_disponiveis = [
             p for p in PERICIAS_POR_NOME.values() 
             if p.nome not in pericias_treinadas
         ]
         self.criar_frame_pericias(
             frame_extras,
             f"Escolha {self.personagem.bonus_int_pericias} perícias extras",
             pericias_disponiveis
         )
         notebook.add(frame_extras, text="Extras") 
        
        notebook.pack(expand=True, fill="both")
        ttk.Button(self, text="Confirmar", command=self.salvar).pack(pady=10)
    
    def criar_frame_pericias(self, frame, titulo, pericias_info):
        ttk.Label(frame, text=titulo, font=('Arial', 11, 'bold')).pack(pady=5)
        
        if isinstance(pericias_info, dict):
            # Trata estrutura de dicionário (perícias fixas + escolhas)
            if 'fixas' in pericias_info:
                for item in pericias_info['fixas']:
                    if isinstance(item, dict):
                        qtd = item.get('quantidade_escolhas_obrigatorias',item.get('quantidade', 0) )
                        self.criar_selecao(
                            frame, 
                            item['escolha'],
                            qtd,
                            "Escolha obrigatória:"
                            )
                    else:
                        ttk.Label(frame, text=f"• {item} (Fixa)").pack(anchor='w')
                        self.pericias_obrigatorias_selecionadas.append(item)
            
            if 'escolhas' in pericias_info:
                qtd = pericias_info.get('quantidade_escolhas_obrigatorias',
                                        pericias_info.get('quantidade_escolhas', 0))
                self.criar_selecao(
                    frame, 
                    pericias_info['escolhas'],
                    qtd,
                    "Escolha:"
                )
        else:
            # Trata lista direta de perícias
            self.criar_selecao(frame, pericias_info, len(pericias_info))
    
    def criar_selecao(self, frame, pericias, max_selecoes, titulo=""):
        if titulo:
            ttk.Label(frame, text=titulo).pack(anchor='w')
        
        container = ttk.Frame(frame)
        container.pack(anchor='w', padx=20)
        
        # Verifica se é lista de objetos Pericia ou strings
        is_pericia_objects = bool(pericias) and isinstance(pericias[0], Pericia)
        
        for item in pericias:
            pericia = item if is_pericia_objects else PERICIAS_POR_NOME.get(item)
            if not pericia:
                continue
                
            var = tk.IntVar()
            nome_atributo = str(pericia.atributo_chave).split('.')[-1]
            
            cb = ttk.Checkbutton(
                container,
                text=f"{pericia.nome} ({nome_atributo})",
                variable=var,
                onvalue=1,
                offvalue=0
            )
            cb.pack(anchor='w')
            self.vars[pericia.nome] = var
    
    def salvar(self):
     try:
         
         for nome in self.pericias_obrigatorias_selecionadas:
             self.personagem.adicionar_pericia_treinada(nome)
         extras_selecionadas = [
              nome for nome, var in self.vars.items()
              if var.get() == 1 and nome not in self.pericias_obrigatorias_selecionadas
          ]
         bonus_disponivel = self.personagem.calcular_bonus_int_pericias()
         if len(extras_selecionadas) > bonus_disponivel:
             raise ValueError(f"Selecione no máximo {bonus_disponivel} perícias extras")
         for nome in extras_selecionadas:
             self.personagem.adicionar_pericia_treinada(nome)
         
         self._callback(self.personagem)
         self.destroy()
        
     except Exception as e:
         messagebox.showerror("Erro", f"Erro ao salvar perícias: {str(e)}")
         raise
    
    def carregar_pericias(self):
        try:
            self.classe_info = get_pericias_classe(self.personagem.classe)
        except Exception as e:
            raise ValueError(f"Erro ao carregar perícias: {str(e)}")
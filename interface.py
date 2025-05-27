import tkinter as tk
from tkinter import ttk, messagebox
from personagem import Raca, Classe, Personagem, MODIFICADORES_RACA, MODIFICADORES_CLASSE
from persistence import salvar_personagens, carregar_personagens

class RPGInterface:
    def __init__(self, root_window, return_to_menu_callback):
        self.root = root_window
        self.return_to_menu = return_to_menu_callback
        self.personagens = carregar_personagens()
        
        # Variáveis de controle
        self.raca_var = tk.StringVar()
        self.classe_var = tk.StringVar()
        self.raca_var.trace('w', self.atualizar_bonus)
        self.classe_var.trace('w', self.atualizar_bonus)
        
        self.criar_widgets()
        self.atualizar_lista()
    
    def atualizar_bonus(self, *args):
        """Atualiza os bônus e modificadores quando raça/classe mudam"""
        try:
            raca_nome = self.raca_var.get()
            classe_nome = self.classe_var.get()
            
            if not raca_nome or not classe_nome:
                return
                
            raca = Raca(raca_nome)
            classe = Classe(classe_nome)
            
            # Atualiza bônus e modificadores para cada atributo
            for atributo in self.atributos_vars:
                valor_base = self.atributos_vars[atributo].get()
                
                # Calcula bônus de raça/classe
                bonus = 0
                bonus += MODIFICADORES_RACA.get(raca, {}).get(atributo, 0)
                bonus += MODIFICADORES_CLASSE.get(classe, {}).get(atributo, 0)
                
                # Atualiza label de bônus
                self.bonus_labels[atributo].config(
                    text=f"+{bonus}" if bonus >= 0 else f"{bonus}",
                    foreground="green" if bonus > 0 else "red" if bonus < 0 else "black"
                )
                
                # Calcula valor total e modificador
                valor_total = valor_base + bonus
                modificador = Personagem.calcular_modificador(valor_total)
                
                # Atualiza label de modificador
                self.modificadores_vars[atributo].set(
                    f"+{modificador}" if modificador >= 0 else f"{modificador}"
                )
                
        except ValueError:
            pass
    
    def criar_widgets(self):
        # Configuração inicial do grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Botão Voltar
        ttk.Button(
            main_frame,
            text="Voltar ao Menu",
            command=self.return_to_menu
        ).grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        
        # Frame de criação
        criar_frame = ttk.LabelFrame(main_frame, text="Criar Personagem", padding="10")
        criar_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configurar colunas
        criar_frame.columnconfigure(1, weight=1)
        criar_frame.columnconfigure(3, minsize=50)  # Coluna para modificadores
        
        # Nome
        ttk.Label(criar_frame, text="Nome:").grid(row=0, column=0, sticky="e")
        self.nome_entry = ttk.Entry(criar_frame)
        self.nome_entry.grid(row=0, column=1, columnspan=3, sticky="ew")
        
        # Raça
        ttk.Label(criar_frame, text="Raça:").grid(row=1, column=0, sticky="e")
        self.raca_combo = ttk.Combobox(
            criar_frame, 
            textvariable=self.raca_var,
            values=[r.value for r in Raca], 
            state='readonly'
        )
        self.raca_combo.grid(row=1, column=1, columnspan=3, sticky="ew")
        
        # Classe
        ttk.Label(criar_frame, text="Classe:").grid(row=2, column=0, sticky="e")
        self.classe_combo = ttk.Combobox(
            criar_frame, 
            textvariable=self.classe_var,
            values=[c.value for c in Classe], 
            state='readonly'
        )
        self.classe_combo.grid(row=2, column=1, columnspan=3, sticky="ew")
        
        # Ouro
        ttk.Label(criar_frame, text="Ouro:").grid(row=3, column=0, sticky="e")
        self.ouro_entry = ttk.Entry(criar_frame, width=10)
        self.ouro_entry.insert(0, "0")
        self.ouro_entry.grid(row=3, column=1, sticky="w")
        
        # Cabeçalho dos atributos
        ttk.Label(criar_frame, text="Atributos (valores rolados):").grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Label(criar_frame, text="Bônus").grid(row=4, column=2)
        ttk.Label(criar_frame, text="Modificador").grid(row=4, column=3)
        
        self.atributos_vars = {}
        self.modificadores_vars = {}
        self.bonus_labels = {}
        
        atributos = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma']
        for i, atributo in enumerate(atributos):
            # Nome do atributo
            ttk.Label(criar_frame, text=f"{atributo.capitalize()}:").grid(row=5+i, column=0, sticky="e")
            
            # Entrada do valor rolado
            self.atributos_vars[atributo] = tk.IntVar(value=10)
            entry = ttk.Entry(
                criar_frame, 
                textvariable=self.atributos_vars[atributo], 
                width=5
            )
            entry.grid(row=5+i, column=1, sticky="w")
            entry.bind('<KeyRelease>', lambda e, a=atributo: self.atualizar_modificador(a))
            
            # Label para bônus de raça/classe
            self.bonus_labels[atributo] = ttk.Label(criar_frame, text="+0", width=5)
            self.bonus_labels[atributo].grid(row=5+i, column=2)
            
            # Label para modificador
            self.modificadores_vars[atributo] = tk.StringVar(value="+0")
            ttk.Label(
                criar_frame, 
                textvariable=self.modificadores_vars[atributo],
                width=5
            ).grid(row=5+i, column=3)
        
        # Botão criar personagem
        ttk.Button(
            criar_frame, 
            text="Criar Personagem", 
            command=self.criar_personagem
        ).grid(row=12, column=0, columnspan=4, pady=10)
        
        # Lista de personagens
        lista_frame = ttk.LabelFrame(main_frame, text="Personagens", padding="10")
        lista_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)
        
        self.lista_personagens = tk.Listbox(lista_frame, height=10)
        scroll = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.lista_personagens.yview)
        self.lista_personagens.configure(yscrollcommand=scroll.set)
        
        self.lista_personagens.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")
        
        # Botões de ação
        botoes_frame = ttk.Frame(lista_frame)
        botoes_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            botoes_frame, 
            text="Ver Detalhes", 
            command=self.ver_detalhes_personagem
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            botoes_frame, 
            text="Remover", 
            command=self.remover_personagem
        ).pack(side=tk.LEFT, padx=5)
    
    def atualizar_modificador(self, atributo):
        """Atualiza o modificador quando o valor base muda"""
        try:
            valor_base = self.atributos_vars[atributo].get()
            
            # Obtém raça e classe atuais
            raca = Raca(self.raca_var.get()) if self.raca_var.get() else None
            classe = Classe(self.classe_var.get()) if self.classe_var.get() else None
            
            # Calcula bônus
            bonus = 0
            if raca:
                bonus += MODIFICADORES_RACA.get(raca, {}).get(atributo, 0)
            if classe:
                bonus += MODIFICADORES_CLASSE.get(classe, {}).get(atributo, 0)
            
            # Calcula valor total e modificador
            valor_total = valor_base + bonus
            modificador = Personagem.calcular_modificador(valor_total)
            
            # Atualiza modificador
            self.modificadores_vars[atributo].set(
                f"+{modificador}" if modificador >= 0 else f"{modificador}"
            )
            
        except:
            pass
    
    def criar_personagem(self):
        try:
            nome = self.nome_entry.get()
            if not nome:
                raise ValueError("Nome é obrigatório")
            
            raca = Raca(self.raca_var.get())
            classe = Classe(self.classe_var.get())
            ouro = int(self.ouro_entry.get())
            
            # Coletar valores rolados dos atributos
            atributos_base = {
                'forca': self.atributos_vars['forca'].get(),
                'destreza': self.atributos_vars['destreza'].get(),
                'constituicao': self.atributos_vars['constituicao'].get(),
                'inteligencia': self.atributos_vars['inteligencia'].get(),
                'sabedoria': self.atributos_vars['sabedoria'].get(),
                'carisma': self.atributos_vars['carisma'].get()
            }
            
            personagem = Personagem(nome, raca, classe, atributos_base, 1, ouro)
            self.personagens.append(personagem)
            salvar_personagens(self.personagens)
            self.atualizar_lista()
            self.limpar_formulario()
            
            messagebox.showinfo("Sucesso", f"Personagem {nome} criado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao criar personagem: {str(e)}")
    
    def ver_detalhes_personagem(self):
        selecionado = self.lista_personagens.curselection()
        if not selecionado:
            return
        
        personagem = self.personagens[selecionado[0]]
        messagebox.showinfo(
            "Detalhes do Personagem",
            f"Nome: {personagem.nome}\n"
            f"Raça: {personagem.raca.value}\n"
            f"Classe: {personagem.classe.value}\n"
            f"Nível: {personagem.nivel}\n"
            f"Ouro: {personagem.ouro}\n"
            f"Atributos: {personagem.atributos}\n"
            f"Habilidades: {', '.join(personagem.habilidades) or 'Nenhuma'}\n"
            f"Equipamentos: {', '.join(personagem.equipamentos) or 'Nenhum'}"
        )
    
    def remover_personagem(self):
        selecionado = self.lista_personagens.curselection()
        if not selecionado:
            return
        
        nome = self.personagens[selecionado[0]].nome
        if messagebox.askyesno("Confirmar", f"Remover o personagem {nome}?"):
            del self.personagens[selecionado[0]]
            salvar_personagens(self.personagens)
            self.atualizar_lista()
    
    def atualizar_lista(self):
        self.lista_personagens.delete(0, tk.END)
        for p in self.personagens:
            self.lista_personagens.insert(tk.END, f"{p.nome} - {p.raca.value} {p.classe.value} (Nível {p.nivel})")
    
    def limpar_formulario(self):
        self.nome_entry.delete(0, tk.END)
        self.raca_combo.set('')
        self.classe_combo.set('')
        self.ouro_entry.delete(0, tk.END)
        self.ouro_entry.insert(0, "0")
        for atributo in self.atributos_vars:
            self.atributos_vars[atributo].set(10)
            self.modificadores_vars[atributo].set("+0")
            self.bonus_labels[atributo].config(text="+0", foreground="black")
import tkinter as tk
from tkinter import ttk, messagebox
from personagem import Raca, Classe, Personagem, MODIFICADORES_RACA_FIXOS, MODIFICADORES_CLASSE
from persistence import carregar_personagens, salvar_personagens
class RPGInterface:
    def __init__(self, root_window, return_to_menu_callback):
        self.root = root_window
        self.return_to_menu = return_to_menu_callback
        self.personagens = carregar_personagens()
        
        self.raca_var = tk.StringVar()
        self.classe_var = tk.StringVar()
        self.raca_var.trace('w', self.atualizar_interface_raca)
        self.classe_var.trace('w', self.atualizar_modificadores)
        
        self.atributos_vars = {}
        self.modificadores_vars = {}
        self.bonus_labels = {}
        self.checkboxes_atributos = {}  # Para as raças especiais
        
        self.criar_widgets()
        self.atualizar_lista()
    
    def criar_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de criação
        criar_frame = ttk.LabelFrame(main_frame, text="Criar Personagem", padding=10)
        criar_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
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
        
        # Frame para seleção de atributos especiais
        self.frame_atributos_especiais = ttk.LabelFrame(criar_frame, text="Escolha 3 Atributos para Bônus (+2 cada)", padding=10)
        self.frame_atributos_especiais.grid(row=4, column=0, columnspan=4, sticky="ew", pady=5)
        self.frame_atributos_especiais.grid_remove()  # Escondido inicialmente
        
        # Atributos
        ttk.Label(criar_frame, text="Atributos (valores rolados):").grid(row=5, column=0, columnspan=4, pady=5)
        
        atributos = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma']
        for i, atributo in enumerate(atributos):
            # Nome do atributo
            ttk.Label(criar_frame, text=f"{atributo.capitalize()}:").grid(row=6+i, column=0, sticky="e")
            
            # Entrada do valor rolado
            self.atributos_vars[atributo] = tk.IntVar(value=10)
            ttk.Entry(
                criar_frame, 
                textvariable=self.atributos_vars[atributo], 
                width=5
            ).grid(row=6+i, column=1, sticky="w")
            
            # Label para bônus fixos
            self.bonus_labels[atributo] = ttk.Label(criar_frame, text="+0", width=5)
            self.bonus_labels[atributo].grid(row=6+i, column=2)
            
            # Label para modificador
            self.modificadores_vars[atributo] = tk.StringVar(value="+0")
            ttk.Label(
                criar_frame, 
                textvariable=self.modificadores_vars[atributo],
                width=5
            ).grid(row=6+i, column=3)
        
        # Botão criar
        ttk.Button(
            criar_frame, 
            text="Criar Personagem", 
            command=self.criar_personagem
        ).grid(row=13, column=0, columnspan=4, pady=10)
        
        # Lista de personagens
        lista_frame = ttk.LabelFrame(main_frame, text="Personagens", padding=10)
        lista_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.lista_personagens = tk.Listbox(lista_frame, height=10)
        scroll = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.lista_personagens.yview)
        self.lista_personagens.configure(yscrollcommand=scroll.set)
        
        self.lista_personagens.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botões de ação
        botoes_frame = ttk.Frame(lista_frame)
        botoes_frame.pack(fill=tk.X, pady=5)
        
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
    
    def atualizar_interface_raca(self, *args):
        """Atualiza a interface quando a raça é alterada"""
        try:
            raca_nome = self.raca_var.get()
            if not raca_nome:
                return
                
            raca = Raca(raca_nome)
            
            # Limpa o frame de atributos especiais
            for widget in self.frame_atributos_especiais.winfo_children():
                widget.destroy()
            
            # Mostra/Esconde o frame de atributos especiais
            if raca in [Raca.HUMANO, Raca.LEFOU, Raca.OSTEON, Raca.SEREIA]:
                self.frame_atributos_especiais.grid()
                
                # Cria checkboxes para os atributos permitidos
                atributos_permitidos = ['forca', 'destreza', 'constituicao', 'inteligencia', 'sabedoria', 'carisma']
                
                # Remove atributos proibidos
                if raca == Raca.LEFOU:
                    atributos_permitidos.remove('carisma')
                elif raca == Raca.OSTEON:
                    atributos_permitidos.remove('constituicao')
                
                # Cria checkboxes
                self.checkboxes_atributos = {}
                for i, atributo in enumerate(atributos_permitidos):
                    var = tk.IntVar()
                    cb = ttk.Checkbutton(
                        self.frame_atributos_especiais,
                        text=f"+2 {atributo.capitalize()}",
                        variable=var,
                        onvalue=2,
                        offvalue=0
                    )
                    cb.grid(row=i//3, column=i%3, sticky="w", padx=5, pady=2)
                    self.checkboxes_atributos[atributo] = var
                
                # Label de instrução
                ttk.Label(
                    self.frame_atributos_especiais,
                    text="Selecione exatamente 3 atributos:",
                    font=('Arial', 9, 'italic')
                ).grid(row=2, column=0, columnspan=3, pady=5)
            else:
                self.frame_atributos_especiais.grid_remove()
            
            # Atualiza bônus fixos
            self.atualizar_bonus_fixos()
            
        except ValueError:
            pass
    
    def atualizar_bonus_fixos(self):
        """Atualiza os bônus fixos de raça na interface"""
        try:
            raca_nome = self.raca_var.get()
            raca = Raca(raca_nome) if raca_nome else None
        
            
            # Atualiza labels de bônus fixos
            for atributo in self.bonus_labels:
                bonus_raca = MODIFICADORES_RACA_FIXOS.get(raca, {}).get(atributo, 0) if raca else 0
             
                    
                self.bonus_labels[atributo].config(
                    text=f"{bonus_raca}" if bonus_raca != 0 else "0",
                foreground="green" if bonus_raca > 0 else "red" if bonus_raca < 0 else "black"
            )

            
            # Atualiza modificadores
            self.atualizar_modificadores()
            
        except ValueError:
            pass
    
    def atualizar_modificadores(self,*args):
        """Atualiza todos os modificadores na interface"""
        try:
            raca_nome = self.raca_var.get()
            raca = Raca(raca_nome) if raca_nome else None

            
            
            # Calcula bônus totais (fixos + escolhidos)
            bonus_total = {}
            for atributo in self.bonus_labels:
                # Bônus fixos
                bonus = MODIFICADORES_RACA_FIXOS.get(raca, {}).get(atributo, 0) if raca else 0
                
                # Bônus escolhidos (para raças especiais)
                if raca in [Raca.HUMANO, Raca.LEFOU, Raca.OSTEON, Raca.SEREIA]:
                    bonus += self.checkboxes_atributos.get(atributo, tk.IntVar(value=0)).get()
                
                
                
                bonus_total[atributo] = bonus
            
            # Atualiza modificadores
            for atributo in self.modificadores_vars:
                valor_base = self.atributos_vars[atributo].get()
                valor_total = valor_base + bonus_total[atributo]
                modificador = Personagem.calcular_modificador(valor_total)
                
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
            
            # Coletar valores rolados
            atributos_base = {
                'forca': self.atributos_vars['forca'].get(),
                'destreza': self.atributos_vars['destreza'].get(),
                'constituicao': self.atributos_vars['constituicao'].get(),
                'inteligencia': self.atributos_vars['inteligencia'].get(),
                'sabedoria': self.atributos_vars['sabedoria'].get(),
                'carisma': self.atributos_vars['carisma'].get()
            }
            
            # Coletar atributos escolhidos para raças especiais
            atributos_escolhidos = {}
            if raca in [Raca.HUMANO, Raca.LEFOU, Raca.OSTEON, Raca.SEREIA]:
                # Verifica se selecionou exatamente 3 atributos
                selecionados = [
                    (atributo, var.get()) 
                    for atributo, var in self.checkboxes_atributos.items() 
                    if var.get() > 0
                ]
                
                if len(selecionados) != 3:
                    raise ValueError("Selecione exatamente 3 atributos para receber +2")
                
                atributos_escolhidos = {atributo: bonus for atributo, bonus in selecionados}
            
            # Cria o personagem
            personagem = Personagem(
                nome=nome,
                raca=raca,
                classe=classe,
                atributos_base=atributos_base,
                atributos_escolhidos=atributos_escolhidos,
                ouro=ouro,
                xp = 0
            )
            
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
            f"XP: {personagem.xp}/{Personagem.TABELA_XP[personagem.nivel] if personagem.nivel < len(Personagem.TABELA_XP) else 'Máximo'}\n"
            f"PV: {personagem.pv_atual}/{personagem.pv_max}\n"
            f"PM: {personagem.pm_atual}/{personagem.pm_max}\n"
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
            self.lista_personagens.insert(tk.END, f"{p.nome} - {p.raca.value} {p.classe.value} (Nível {p.nivel}, PV: {p.pv_atual}/{p.pv_max})")
    
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
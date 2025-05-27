import tkinter as tk
from tkinter import ttk
from interface import RPGInterface

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Manager - Menu Principal")
        self.root.geometry("400x300")
        
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        
        self.create_widgets()
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Título
        ttk.Label(main_frame, text="RPG Manager", font=('Helvetica', 18, 'bold')).pack(pady=20)
        
        # Botões
        ttk.Button(
            main_frame, 
            text="Criar Personagem", 
            command=self.open_character_creator
        ).pack(fill=tk.X, pady=10)
        
        ttk.Button(
            main_frame, 
            text="Batalha (Em Breve)", 
            state='disabled'
        ).pack(fill=tk.X, pady=10)
        
        ttk.Button(
            main_frame, 
            text="Sair", 
            command=self.root.quit
        ).pack(fill=tk.X, pady=10)
    
    def open_character_creator(self):
        # Esconde o menu principal
        self.root.withdraw()
        
        # Cria a janela de criação de personagem
        char_window = tk.Toplevel()
        char_window.title("Criador de Personagens")
        char_window.geometry("800x600")
        char_window.protocol("WM_DELETE_WINDOW", lambda: self.return_to_menu(char_window))
        
        # Configurar pesos para expansão
        char_window.columnconfigure(0, weight=1)
        char_window.rowconfigure(0, weight=1)
        
        # Inicia a interface de criação com callback para voltar
        RPGInterface(char_window, lambda: self.return_to_menu(char_window))
    
    def return_to_menu(self, window):
        window.destroy()
        self.root.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()
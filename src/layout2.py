# layout.py
import tkinter as tk
import sys
import os
import shutil
import time
import threading
from tkinter import ttk
from tkinter import filedialog, messagebox
from main import handle_xml_folder

class App(tk.Tk):
    # Construtor da classe
    def __init__(self):
        super().__init__()

        self.title("Antecipação ICMS")
        self.configure(bg='gray15')

        # Centralizar a janela
        window_width = 400
        window_height = 400
        self.center_window(window_width, window_height)

        self.folder_path = None
        self.file_sheet = None
        self.folder_to_download = None
        self.icon_open = tk.PhotoImage(file="assets/ideen.png")

        label_style = {'bg': 'gray15', 'fg': 'white'}
        button_exit_style = {
            'bg': '#ff2424',
            'fg': 'white',
            'activebackground': 'gray50',
            'activeforeground': 'white',
            'borderwidth': 1
        }
        button_style = {
            'bg': 'gray20',
            'fg': 'white',
            'activebackground': 'gray50',
            'activeforeground': 'white',
            'borderwidth': 1
        }

        # Tela inicial
        self.start_frame = tk.Frame(self, bg="gray15")
        self.start_frame.pack(fill='both', expand=True)

        self.start_label = tk.Label(self.start_frame, text="Escolha a opção desejada:", **label_style)
        self.start_label.pack(pady=20, padx=20)

        self.start_button = tk.Button(
            self.start_frame,
            text="Selecionar pasta com XMLs",
            command=self.select_xml_folder,
            **button_style
        )
        self.start_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        self.select_sheet_button = tk.Button(
            self.start_frame,
            text="Selecionar planilha",
            command=self.select_sheet,
            **button_style
        )
        self.select_sheet_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        self.generate_result_button = tk.Button(
            self.start_frame,
            text="Gerar Resultado",
            command=self.process_directory,
            **button_style
        )
        self.generate_result_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        self.exit_button = tk.Button(
            self.start_frame,
            text="Sair",
            command=sys.exit,
            **button_exit_style
        )
        self.exit_button.pack(pady=10, padx=20, ipadx=10, ipady=5)

        self.developer_label = tk.Label(
            self.start_frame,
            text="Desenvolvido por IDeeN Tecnologia",
            compound="left",
            image=self.icon_open,
            **label_style
        )
        self.developer_label.pack(pady=20, padx=20)

        # Tela de carregamento
        self.loading_frame = tk.Frame(self, bg="gray15")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", troughcolor='#3e3e3e', background='#4caf50',
                        thickness=20, bordercolor='#2e2e2e', lightcolor='#4caf50', darkcolor='#4caf50')

        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(
            self.loading_frame,
            variable=self.progress_var,
            maximum=100,  # O máximo será ajustado durante o processamento
            orient="horizontal",
            length=300,
            mode="determinate",
            style="TProgressbar"
        )
        self.progress_bar.pack(pady=10, padx=20, fill='x')

        self.progress_bar_label = tk.Label(
            self.loading_frame,
            text=f"Processando XML 0 de 0",  # Inicialmente sem valor real
            **label_style
        )
        self.progress_bar_label.pack(pady=20)

        self.developer_label = tk.Label(
            self.loading_frame,
            text="Desenvolvido por IDeeN Tecnologia",
            compound="left",
            **label_style
        )
        self.developer_label.pack(pady=20, padx=20)

        # Tela de resultado
        self.result_frame = tk.Frame(self, bg="gray15")

        self.result_label = tk.Label(self.result_frame, text="Processo concluído!", **label_style)
        self.result_label.pack(pady=20)

        self.download_button = tk.Button(
            self.result_frame,
            text="Baixar Resultado",
            command=self.download_folder_modified,
            **button_style
        )
        self.download_button.pack(pady=10)

        self.return_button = tk.Button(
            self.result_frame,
            text="Voltar ao Início",
            command=self.return_to_start,
            **button_style
        )
        self.return_button.pack(pady=10)

        self.developer_label = tk.Label(
            self.result_frame,
            text="Desenvolvido por IDeeN Tecnologia",
            image=self.icon_open,
            compound="left",
            **label_style
        )
        self.developer_label.pack(pady=20, padx=20)

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.geometry(f'{width}x{height}+{x}+{y}')

    def select_xml_folder(self):
        self.folder_path = filedialog.askdirectory(
            initialdir="/",
            title="Selecione a pasta"
        )
        if self.folder_path:
            xml_files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
            if not xml_files:
                messagebox.showerror("Erro", "Nenhum arquivo XML encontrado na pasta selecionada.")

    def select_sheet(self):
        self.file_sheet = filedialog.askopenfilename(filetypes=[("Arquivos XLS", "*.xls")])

    def process_directory(self):
        if not self.folder_path or not self.file_sheet:
            messagebox.showerror("Erro", "Por favor, selecione a pasta de XMLs e a planilha antes de continuar.")
            return

        # Mudando para a tela de carregamento e iniciando o processamento
        self.start_frame.pack_forget()  # Escondendo a tela inicial
        self.loading_frame.pack(fill='both', expand=True)  # Exibindo a tela de processamento

        # Atualizar a barra de progresso com o número total de XMLs
        self.progress_var.set(0)
        threading.Thread(target=self.run_process).start()  # Executando o XML em segundo plano para a tela não travar

    def update_progress(self, current, total):
        # Atualizar a barra de progresso dinamicamente
        self.progress_var.set(current)
        self.progress_bar.config(maximum=total)
        self.progress_bar_label.config(text=f"Processando XML {current} de {total}")
        self.update_idletasks()
        time.sleep(0.05)

    def run_process(self):
        try:
            # Passando o callback para atualização do progresso
            result = handle_xml_folder(self.folder_path, self.file_sheet, self.update_progress)

            # Verifica se o resultado é um caminho válido
            if isinstance(result, str) and os.path.isfile(result):
                self.folder_to_download = result
            else:
                self.folder_to_download = None
                messagebox.showerror("Erro", "Falha ao processar a pasta: o retorno não é um caminho válido.")

        finally:
            self.loading_frame.pack_forget()  # Escondendo tela de processamento
            self.result_frame.pack(fill='both', expand=True)  # Exibindo tela de resultado

    def download_folder_modified(self):
        if not self.folder_to_download:
            messagebox.showwarning("Erro", "Nenhum arquivo para download.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension='.zip',
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
            title="Salvar arquivo ZIP"
        )

        # Verificando se um caminho de salvamento foi escolhido
        if not save_path:
            messagebox.showinfo("Cancelado", "Operação de salvamento cancelada.")
            return

        try:
            # Copiar o arquivo processado para o caminho selecionado
            shutil.copy(self.folder_to_download, save_path)
            messagebox.showinfo("Download concluído", f"Resultado salvo em: {save_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")

    def return_to_start(self):
        self.result_frame.pack_forget()
        self.start_frame.pack(fill='both', expand=True)

# Criação da aplicação
app = App()
app.mainloop()

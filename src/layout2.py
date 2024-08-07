import tkinter as tk
import sys
import time
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import shutil
import threading
from main import handle_xml_folder


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Antecipação ICMS")
        self.geometry("400x400")
        self.configure(bg='gray15')

        self.folder_path = None
        self.file_sheet = None
        self.folder_to_download = None

        label_style = {'bg': '#515151', 'fg': 'white'}
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
        self.start_frame = tk.Frame(self, bg="#515151")
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
            **label_style
        )
        self.developer_label.pack(pady=20, padx=20)

        # Tela de carregamento
        self.loading_frame = tk.Frame(self, bg="#515151")

        self.loading_label = tk.Label(self.loading_frame, text="Processando...", **label_style)
        self.loading_label.pack(pady=20)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.loading_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(pady=10, padx=20, fill='x')

        # Tela de resultado
        self.result_frame = tk.Frame(self, bg="#515151")

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

    def select_xml_folder(self):
        """Seleciona a pasta com os arquivos XML."""
        self.folder_path = filedialog.askdirectory(
            initialdir="/",
            title="Selecione a pasta"
        )
        if self.folder_path:
            xml_files = [f for f in os.listdir(self.folder_path) if f.endswith('.xml')]
            if not xml_files:
                messagebox.showerror("Erro", "Nenhum arquivo XML encontrado na pasta selecionada.")
            else:
                print(f"Pasta selecionada: {self.folder_path}")
                print("Arquivos XML na pasta:", xml_files)

    def select_sheet(self):
        """Seleciona a planilha de entrada."""
        self.file_sheet = filedialog.askopenfilename(filetypes=[("Arquivos XLS", "*.xls")])
        if self.file_sheet:
            print("Arquivo selecionado: ", self.file_sheet)

    def process_directory(self):
        """Processa o diretório e manipula XML."""
        if not self.folder_path or not self.file_sheet:
            messagebox.showerror("Erro", "Por favor, selecione a pasta de XMLs e a planilha antes de continuar.")
            return

        # Mudar para a tela de carregamento e iniciar o processamento
        self.start_frame.pack_forget()
        self.loading_frame.pack(fill='both', expand=True)
        threading.Thread(target=self.run_process).start()

    def run_process(self):
        """Função de execução em segundo plano."""
        try:
            # Simulação de processamento
            for i in range(101):
                time.sleep(0.05)  # Simula tempo de processamento
                self.progress_var.set(i)
                self.update_idletasks()

            # Substituir pelo seu método real de manipulação de XML
            result = handle_xml_folder(self.folder_path, self.file_sheet)
            print(f"Retorno de handle_xml_folder: {result} (tipo: {type(result)})")
            
            if isinstance(result, str) and os.path.isfile(result):
                self.folder_to_download = result
                self.folder_ready_to_download = True
            else:
                self.folder_to_download = None
                messagebox.showerror("Erro", "Falha ao processar a pasta: o retorno não é um caminho válido.")

        finally:
            # Exibir a tela de resultado após o processamento
            self.loading_frame.pack_forget()
            self.result_frame.pack(fill='both', expand=True)

    def download_folder_modified(self):
        """Baixa o resultado modificado."""
        if not self.folder_to_download:
            messagebox.showwarning("Erro", "Nenhum arquivo para download.")
            return

        # Abrir diálogo de salvamento
        save_path = filedialog.asksaveasfilename(
            defaultextension='.zip',
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
            title="Salvar arquivo ZIP"
        )

        # Verificar se um caminho de salvamento foi escolhido
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
        """Retorna à tela inicial."""
        self.result_frame.pack_forget()
        self.start_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()

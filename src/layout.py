import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
import shutil
from tkinter import filedialog, messagebox, BooleanVar
from main import handle_xml_folder

folder_to_download = None
        
def select_xml_folder():
    global folder_path
    folder_path = filedialog.askdirectory(
        initialdir="/",
        title="Select folder"
    )
    if folder_path:
        xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
        if not xml_files:
            messagebox.showerror("Error", "No XML files found in the selected folder.")
        else:
            print(f"Selected folder: {folder_path}")
            print("XML files in folder:", xml_files)
    
def select_sheet():
    global file_sheet
    file_sheet = filedialog.askopenfilename(filetypes=[("Arquivos XLS", "*.xls")]    )
    if file_sheet:
        print("Arquivo selecionado: ", file_sheet)
                       
def process_directory():
    global folder_to_download
    result = handle_xml_folder(folder_path, file_sheet)
    print(f"Retorno de handle_xml_folder: {result} (tipo: {type(result)})")
    if isinstance(result, str):
        folder_to_download = result
        folder_ready_to_download.set(True)
    else:
        folder_to_download = None
        messagebox.showerror("Erro", "Falha ao processar a pasta: o retorno não é um caminho válido.")
        
def download_folder_modified():
    global folder_to_download
    
    # Verificar se folder_to_download é um caminho válido
    if folder_to_download is None:
        messagebox.showwarning("Erro", "Nenhum arquivo para download.")
        return

    if not isinstance(folder_to_download, str):
        messagebox.showerror("Erro", "O caminho do arquivo não é uma string.")
        return

    # Verificar se o caminho é um arquivo
    if not os.path.isfile(folder_to_download):
        messagebox.showwarning("Erro", "Caminho inválido ou não é um arquivo.")
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
        shutil.copy(folder_to_download, save_path)
        messagebox.showinfo("Download concluído", f"Resultado salvo em: {save_path}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar o arquivo: {e}")
        
def toggle_download_button(*args):
    if folder_ready_to_download.get():
        download_button.pack(pady=10, padx=20, ipadx=10, ipady=5)
    else:
        download_button.pack_forget()

root = tk.Tk()
root.title("Antecipação ICMS")
root.configure(bg='gray15')

label_style = {'bg': 'gray15', 'fg': 'white'}  
button_style = {'bg': 'gray20', 'fg': 'white', 'activebackground': 'gray50', 'activeforeground': 'white', 'borderwidth': 1}

label = tk.Label(root, text="Escolha a opção desejada:", **label_style)
label.pack(pady=10, padx=20)

button = tk.Button(root, text="Selecionar pasta com XMLs", command=select_xml_folder, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)

button = tk.Button(root, text="Selecionar planilha", command=select_sheet, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)

button = tk.Button(root, text="Gerar Resultado", command=process_directory, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)

folder_ready_to_download = BooleanVar()
folder_ready_to_download.set(False) 

download_button = tk.Button(root, text="Baixar Resultado", command=download_folder_modified, **button_style)

folder_ready_to_download.trace_add("write", toggle_download_button)

button = tk.Button(root, text="Sair", command=sys.exit, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)

label = tk.Label(root, text="Desenvolvido por IDeeN Tecnologia", compound="left", **label_style)
label.pack(ipadx=10, ipady=1)

root.mainloop()
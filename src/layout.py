import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
import shutil
from tkinter import filedialog, messagebox, BooleanVar
from main import handle_xml_folder

folder_to_download = None
 
def clear_files():
    files = os.listdir(f"./files/")
    for file in files:
        if file.endswith(".xlsx") or file.endswith(".csv"):
            os.remove(f"./files/" + file)
    
    if os.path.exists("./files/DF") and os.path.exists("./files/GO"):
        shutil.rmtree("./files/DF/")
        shutil.rmtree("./files/GO/")

def escolhe_estado_window():
    new_window = Toplevel(root)
    new_window.title("Antecipação ICMS")
    new_window.configure(bg='gray15')  
    #center_window(new_window, 300, 250)
   # new_window.iconbitmap('img/logo.ico')

    label = tk.Label(new_window, text="Selecione qual SNG deseja processar:", **label_style)
    label.pack(pady=10, padx=20)

    button = tk.Button(new_window, text=" SNG DF", command=progress_window, image=logo_df, compound="left", **button_style)
    button.pack(pady=10, padx=20, ipadx=10, ipady=5)  

    button = tk.Button(new_window, text=" SNG GO", command=rpa_sng_go, image=logo_go, compound="left", **button_style)
    button.pack(pady=10, padx=20, ipadx=10, ipady=5) 

    button = tk.Button(new_window, text="Cancelar", command=new_window.destroy, **button_style)
    button.pack(pady=10, padx=20, ipadx=10, ipady=5)
    
    label = tk.Label(new_window, text=" Desenvolvido por IDeeN Tecnologia",  image=icon_open, compound="left", **label_style)
    label.pack(ipadx=10, ipady=1)
    
def parar_loop():
    global continua_loop
    continua_loop = False 
    
def progress_window():
    progress_window = Toplevel(root)
    progress_window.title("RPA SNG")
   # center_window(progress_window, 400, 180)
    progress_window.configure(bg='gray15')  
    #progress_window.iconbitmap('img/logo.ico')
    
    # Configurar a barra de progresso
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TProgressbar", troughcolor='#3e3e3e', background='#4caf50', 
                    thickness=20, bordercolor='#2e2e2e', lightcolor='#4caf50', darkcolor='#4caf50')

    progress = ttk.Progressbar(progress_window, orient="horizontal", length=300, mode="determinate", style="TProgressbar")
    progress.pack(pady=10, padx=20)

    # Configurar o rótulo de progresso
    progress_label = tk.Label(progress_window, text="Processando Chassi 0 de 0", **label_style)
    progress_label.pack(pady=10)
    
    button = tk.Button(progress_window, text="Cancelar", command=lambda: [progress_window.destroy(), parar_loop()], **button_style)
    button.pack(pady=10, padx=20, ipadx=10, ipady=5)
    
    footer = tk.Label(progress_window, text=" Desenvolvido por IDeeN Tecnologia", image=icon_open, compound="left", **label_style)
    footer.pack(ipadx=10, ipady=1)
    
    def rpa_sng(): 
        
        global continua_loop
        continua_loop = True
        
        if not continua_processo:
                
            if file_path != "":
                if not os.path.exists("./files/"):
                    os.makedirs("./files/")
                clear_files()
                shutil.copyfile(file_path, 'files/CHASSIS.xlsx')
                #save_to_csv2([["Chassi"]], "CHASSI-LIDOS")
            else:
                #aviso("Nenhum arquivo selecionado!")
                sys.exit()
        
        else:
            
            if not os.path.isfile('files/CHASSIS.xlsx') or not os.path.isfile('files/CHASSI-LIDOS.csv'): 
                #aviso("Não existem processamentos antigos pendentes")
                sys.exit()

            #else:
                
                # if len(ler_arquivo_csv('files/CHASSI-LIDOS.csv', ";")) == 0: 
                #     aviso("Não existem processamentos antigos pendentes")
                #     sys.exit()

        #chassis = pd.read_excel("./files/CHASSIS.xlsx", header=None).values
        
        # lidos = ler_arquivo_csv("./files/CHASSI-LIDOS.csv", ";")
        
        # if len(lidos) == len(chassis):
        #     aviso("Não existem processamentos antigos pendentes")
        
        # else:
            
        #     logging.basicConfig(level=logging.INFO, filename="programa.log", format="%(asctime)s - %(levelname)s - %(message)s")
            
        #     logging.info(f"-=-=-=-=-=-=-= RPA SNG (GO & DF) - INICIADO -=-=-=-=-=-=-=.") 

        #     for index, value in enumerate(chassis):
                
        #         if continua_loop:
                
        #             chassi = value[0].strip()
                    
        #             indice = index+1
                    
        #             progress['value'] = ((indice) / len(chassis)) * 100
        #             progress_label.config(text=f"Processando Chassi ({chassi}) {indice} de {len(chassis)}")
        #             # Atualiza a interface gráfica
        #             progress_window.update()
                                    
        #             if chassi in lidos:
        #               pass  continue
        #             else:
                        
        #                 try:
        #                     sng_df = SngDf()
                            
        #                     sng_df.login(chassi)
        #                     extract_info = sng_df.extract_info(chassi)
                            
        #                     if extract_info == False:
        #                         sng_go = SngGo()
                            
        #                         sng_go.login(chassi)
        #                         sng_go.extractInfo(chassi)
                        
        #                 except:
        #                     logging.error(f"GRAVAME) Chassi: {chassi} - Ocorreu um erro!")
        #                     continue
                            
        #         else:
        #             break
                    
        #     lidos_final = ler_arquivo_csv("files/CHASSI-LIDOS.csv", ";")
            
        #     logging.info(f"-=-=-=-=-=-=-= RPA SNG (GO & DF) - TERMINADO -=-=-=-=-=-=-=.") 
            
        #     if len(lidos_final) == len(chassis):
        #         aviso("Todos os chassis foram lidos!")
        #     else:
        #         aviso("Alguns chassis não foram lidos, continue o processamento!")
                
   # rpa_sng()
        
def continuar_processo():
    global continua_processo
    continua_processo = True
    progress_window()

    global file_path
    file_path = filedialog.askopenfilename(
        initialdir="/",
        title="Select XML file",
        filetypes=(("XML files", "*.xml"),)
    )
    if file_path:
        print(f"Selected file: {file_path}")
        process_file(file_path)

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
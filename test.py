import os, shutil, sys, time, logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import Toplevel
from utils.manipula_csv import *
from rpas.sngdf import SngDf
from rpas.snggo import SngGo
from utils.screens import *
 
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
    new_window.title("RPA SNG")
    new_window.configure(bg='gray15')
    center_window(new_window, 300, 250)
    new_window.iconbitmap('img/logo.ico')

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
    center_window(progress_window, 400, 180)
    progress_window.configure(bg='gray15')
    progress_window.iconbitmap('img/logo.ico')
    
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
                save_to_csv2([["Chassi"]], "CHASSI-LIDOS")
            else:
                aviso("Nenhum arquivo selecionado!")
                sys.exit()
        
        else:
            
            if not os.path.isfile('files/CHASSIS.xlsx') or not os.path.isfile('files/CHASSI-LIDOS.csv'): 
                aviso("Não existem processamentos antigos pendentes")
                sys.exit()

            else:
                
                if len(ler_arquivo_csv('files/CHASSI-LIDOS.csv', ";")) == 0: 
                    aviso("Não existem processamentos antigos pendentes")
                    sys.exit()

        chassis = pd.read_excel("./files/CHASSIS.xlsx", header=None).values
        
        lidos = ler_arquivo_csv("./files/CHASSI-LIDOS.csv", ";")
        
        if len(lidos) == len(chassis):
            aviso("Não existem processamentos antigos pendentes")
        
        else:
            
            logging.basicConfig(level=logging.INFO, filename="programa.log", format="%(asctime)s - %(levelname)s - %(message)s")
            
            logging.info(f"-=-=-=-=-=-=-= RPA SNG (GO & DF) - INICIADO -=-=-=-=-=-=-=.") 

            for index, value in enumerate(chassis):
                
                if continua_loop:
                
                    chassi = value[0].strip()
                    
                    indice = index+1
                    
                    progress['value'] = ((indice) / len(chassis)) * 100
                    progress_label.config(text=f"Processando Chassi ({chassi}) {indice} de {len(chassis)}")
                    # Atualiza a interface gráfica
                    progress_window.update()
                                    
                    if chassi in lidos:
                        continue
                    else:
                        
                        try:
                            sng_df = SngDf()
                            
                            sng_df.login(chassi)
                            extract_info = sng_df.extract_info(chassi)
                            
                            if extract_info == False:
                                sng_go = SngGo()
                            
                                sng_go.login(chassi)
                                sng_go.extractInfo(chassi)
                        
                        except:
                            logging.error(f"GRAVAME) Chassi: {chassi} - Ocorreu um erro!")
                            continue
                            
                else:
                    break
                    
            lidos_final = ler_arquivo_csv("files/CHASSI-LIDOS.csv", ";")
            
            logging.info(f"-=-=-=-=-=-=-= RPA SNG (GO & DF) - TERMINADO -=-=-=-=-=-=-=.") 
            
            if len(lidos_final) == len(chassis):
                aviso("Todos os chassis foram lidos!")
            else:
                aviso("Alguns chassis não foram lidos, continue o processamento!")
                
    rpa_sng()
    
def choose_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.xlsx"),("all files","*.*")))
    global continua_processo
    continua_processo = False
    if file_path:
        progress_window()
        
def continuar_processo():
    global continua_processo
    continua_processo = True
    progress_window()

root = tk.Tk()
root.title("RPA SNG")
center_window(root, 400, 250)
root.configure(bg='gray15')  
root.iconbitmap('img/logo.ico')

icon_open = tk.PhotoImage(file="./img/ideen.png")
logo_df = tk.PhotoImage(file="./img/logo-df.png")
logo_go = tk.PhotoImage(file="./img/logo-go.png")

label_style = {'bg': 'gray15', 'fg': 'white'}  
button_style = {'bg': 'gray20', 'fg': 'white', 'activebackground': 'gray50', 'activeforeground': 'white', 'borderwidth': 1}

label = tk.Label(root, text="Escolha a opção desejada:", **label_style)
label.pack(pady=10, padx=20)

button = tk.Button(root, text="Novo processamento", command=choose_file, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)  

button = tk.Button(root, text="Continuar processamento", command=continuar_processo, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)

button = tk.Button(root, text="Sair", command=sys.exit, **button_style)
button.pack(pady=10, padx=20, ipadx=10, ipady=5)

label = tk.Label(root, text=" Desenvolvido por IDeeN Tecnologia",  image=icon_open, compound="left", **label_style)
label.pack(ipadx=10, ipady=1)

root.mainloop()

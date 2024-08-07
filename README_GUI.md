# Antecipação ICMS

Este projeto é uma interface gráfica do usuário (GUI) desenvolvida em Python utilizando o Tkinter. A aplicação permite selecionar uma pasta contendo arquivos XML e uma planilha de entrada, processar esses arquivos, e fornecer uma opção para baixar o resultado processado.

## Requisitos

- Python 3.10.12
- Bibliotecas:
  - `tkinter`
  - `ttk`
  - `threading`
  - `os`
  - `shutil`
  - `time`
  - `sys`


## Estrutura do Projeto

```plaintext
├── main.py          
├── app.py           
└── README.md        
```

## Instalação

1. Clone este repositório:
    ```sh
    git clone
    ```

2. Navegue até o diretório do projeto:
    ```sh
    cd antecipacao-icms
    ```

3. Certifique-se de ter todas as dependências instaladas. Você pode instalar as bibliotecas necessárias usando `pip`:
    ```sh
    pip install tkinter
    ```

## Uso

1. Execute a aplicação:
    ```sh
    python3 src/teste.py
    ```

2. A interface da aplicação será exibida com as seguintes opções:
    - **Selecionar pasta com XMLs**: Escolha a pasta que contém os arquivos XML.
    - **Selecionar planilha**: Escolha a planilha de entrada.
    - **Gerar Resultado**: Inicia o processamento dos arquivos XML.
    - **Sair**: Fecha a aplicação.

3. Após iniciar o processamento, uma tela de carregamento será exibida.

4. Ao concluir o processamento, uma tela de resultado será exibida com a opção de baixar o resultado processado.
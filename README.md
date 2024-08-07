## Script de Processamento de XML e Adição de Tags de ICMS

#### Descrição Geral

Este script é utilizado para processar arquivos XML de notas fiscais eletrônicas (NFe) e adicionar uma tag chamada `ICMSANTECIP` com valores formatados, baseados em uma planilha de detalhamento fornecida. A remoção de namespaces nos arquivos XML também é realizada para facilitar a manipulação dos dados.

#### Dependências

O script depende das seguintes bibliotecas:

- `os`: Para manipulação de arquivos e diretórios.
- `xml.etree.ElementTree` (ET): Para manipulação e parsing de XML.
- `pandas` (pd): Para leitura e manipulação de planilhas Excel.

#### Funções

1. **remove_namespace(doc, namespace)**

   - **Descrição**: Remove namespaces dos elementos XML.
   - **Parâmetros**:
     - `doc`: Documento XML carregado.
     - `namespace`: Namespace a ser removido.
   - **Retorno**: Nenhum.

2. **formatar_valor(valor)**

   - **Descrição**: Formata valores removendo a indicação de moeda e ajustando a pontuação.
   - **Parâmetros**:
     - `valor`: Valor em formato de string com indicação de moeda.
   - **Retorno**: Valor formatado como string.

3. **criar_icmsantecip_sem_ns(item, dados)**
   - **Descrição**: Cria a tag `ICMSANTECIP` com subelementos contendo valores formatados e adiciona ao elemento `imposto`.
   - **Parâmetros**:
     - `item`: Elemento XML onde a nova tag será adicionada.
     - `dados`: Dicionário com os dados a serem inseridos nas sub-tags.
   - **Retorno**: Nenhum.

#### Caminhos de Diretórios

- **input_folder**: Diretório onde os arquivos XML de entrada estão localizados.
- **output_folder**: Diretório onde os arquivos XML processados serão salvos.
- **planilha_path**: Caminho para a planilha de detalhamento em formato Excel.

#### Processamento dos Arquivos XML

1. Carregar a planilha de detalhamento usando `pandas`.
2. Iterar sobre todos os arquivos XML na pasta de entrada.
3. Para cada arquivo XML:
   - Carregar o arquivo XML.
   - Remover namespaces específicos para facilitar a manipulação.
   - Iterar sobre os itens no XML e adicionar a tag `ICMSANTECIP` conforme os dados da planilha de detalhamento.
   - Salvar o XML processado na pasta de saída.

### Instruções de Uso

1. **Instalar Dependências**:

   - Certifique-se de ter as bibliotecas `pandas` e `xml.etree.ElementTree` instaladas. Use `pip install pandas` se necessário.

2. **Configurar Caminhos**:

   - Atualize os caminhos `input_folder`, `output_folder` e `planilha_path` conforme necessário.

3. **Executar o Script**:
   - Execute o script em um ambiente Python. O script processará os arquivos XML na pasta de entrada e salvará os arquivos ajustados na pasta de saída.

</br></br>

<div align="center" justify="center">

<img src="./assets/Icon-IdeeN.png" width="130rem" alt="Icon IdeeN" /> <p>IdeeN Tecnologia ©</p>

</div>

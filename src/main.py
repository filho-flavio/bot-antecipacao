# main.py
import os
import xml.etree.ElementTree as ET
import pandas as pd
from tempfile import mkdtemp
import zipfile

# Função para remover namespaces
def remove_namespace(doc, namespace):
    ns = f'{{{namespace}}}'
    nsl = len(ns)
    for elem in doc.iter():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

# Função para formatar valores sem a indicação de moeda
def formatar_valor(valor):
    valor_str = str(valor).replace('R$', '').strip()
    return valor_str.replace('.', '').replace(',', '.')

# Função para criar a tag ICMSANTECIP com valores formatados
def criar_icmsantecip_sem_ns(item, dados):
    icms_antecip = ET.Element("ICMSANTECIP")
    for key, value in dados.items():
        sub_element = ET.SubElement(icms_antecip, key)
        sub_element.text = formatar_valor(value)
    # Adicionar o ICMSANTECIP ao elemento imposto
    item.append(icms_antecip)

# Iterar sobre todos os arquivos XML na pasta de entrada
def handle_xml_folder(input_folder, sheet_file, update_progress):
    # Ler a planilha Excel
    sheet = pd.read_excel(sheet_file, header=1)

    # cria um diretório temporário para salvar os arquivos XML modificados
    temp_dir = mkdtemp()
    modified_xml_paths = []

    # Obter todos os arquivos XML
    xml_files = [f for f in os.listdir(input_folder) if f.endswith('.xml')]
    total_files = len(xml_files)

    # Certifique-se de que a lista de arquivos não está vazia
    if total_files == 0:
        return None

    for index, filename in enumerate(xml_files):
        file_path = os.path.join(input_folder, filename)
        tree = ET.parse(file_path)
        root = tree.getroot()

        remove_namespace(root, 'http://www.portalfiscal.inf.br/nfe')
        remove_namespace(root, 'http://www.w3.org/2000/09/xmldsig#')

        for det in root.findall('.//det'):
            n_item = det.get('nItem')
            danfe = root.find('.//protNFe/infProt/chNFe').text
            match = sheet[(sheet['DANFE'] == danfe) & (sheet['Nº ITEM'] == int(n_item))]

            if not match.empty:
                dados = {
                    'ICMS_DO_PRODUTO': match['ICMS DO PRODUTO'].values[0],
                    'VALOR_BASE_CALC': match['VALOR BASE CALC'].values[0],
                    'VALOR_ICMS_CALC': match['VALOR ICMS CALC'].values[0],
                    'ICMS_A_PAGAR': match['ICMS A PAGAR'].values[0]
                }

                imposto_tag = det.find(".//imposto")
                icms_tag = imposto_tag.find('.//ICMS')
                if icms_tag is not None:
                    criar_icmsantecip_sem_ns(icms_tag, dados)

        # Salvando o XML modificado em um novo arquivo no diretório temporário
        modified_file_path = os.path.join(temp_dir, filename)
        tree.write(modified_file_path, encoding='utf-8', xml_declaration=True)
        modified_xml_paths.append(modified_file_path)

        # Atualizar o progresso
        update_progress(index + 1, total_files)  # Atualiza o progresso para a UI

    # Cria um arquivo ZIP para armazenar todos os arquivos XML modificados
    zip_file_path = os.path.join(temp_dir, 'modified_xmls.zip')
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in modified_xml_paths:
            zipf.write(file_path, os.path.basename(file_path))

    # Retorna o caminho do arquivo ZIP
    return zip_file_path

print("Processamento concluído.")

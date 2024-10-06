# ---------------------------------------------------------------------------
# Primeiro trabalho de Organização e Recuperação da Informação 2024-1
#
# ENTREGAVEIS:
#     1. Implementação de um gerador de índice invertido ;
#     2. Implementação do modelo booleano para recuperação de informação;
#
# ALUNO: João Pedro Corrêa de Melo Mendes - 12111BSI200.
# ---------------------------------------------------------------------------

import spacy
import sys


# TESTE INSTALAÇÃO

# texto3 = "O rato roeu a roupa do rei de Roma."
# doc3 = nlp(texto3)
# sintaxe = [ (t.orth_, t.dep_) for t in doc3 ]
# print(sintaxe)

# 1° Definir base de documentos
# 2° Indexar base de documentos
# 3° Definir modelo para base de consulta

def read_file(txt_file):
    f = open(txt_file, 'r')
    file_data = [line.strip() for line in f.readlines()]
    return file_data



def main():
    nlp = spacy.load("pt_core_news_lg")


    if len(sys.argv) != 3:
        print("Uso correto: python3 modelo_booleano.py base.txt consulta.txt")
        sys.exit(1)

    base_path = sys.argv[1]
    consulta_path = sys.argv[2]

    # Ler os arquivos e descobrir base de dados.
    base_files = read_file(base_path)
    print(base_files)


    # Criando base de dados em string.
    base_data = set()

    # doc3 = nlp(texto3)
    # sintaxe = [ (t.orth_, t.dep_) for t in doc3 ]
    # print(sintaxe)

    for file in base_files:
        file_raw = read_file(file)
        file_raw = str(file_raw)
        # print(file_raw)

        file_info = nlp(file_raw)
        # print(file_info)

        tokens = list(file_info)

        for t in tokens:
            if not t.is_stop and not t.is_punct:
                ## Aqui ja deveria formular  o dicionário...
                ## NECESSÁRIO MONTAR SAIDA DEPOIS DA FORAM --> Palavra: DOC1, QTD.DOC1 DOC2, QTD.DOC2 ...,... ÇÇÇ,ÇÇÇ
                ## VAMOS CRIAR ENTÃO ESSE INDICE INVERTIDO
                base_data.add(t)



    print(base_data)

    # Consulta Booleana
    consulta_bool = read_file(consulta_path)
    print(consulta_bool)




# Rodar Sistema RI
main()

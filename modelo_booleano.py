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

def read_file(txt_file):
    f = open(txt_file, 'r')
    file_data = [line.strip() for line in f.readlines()]
    f.close()
    return file_data


def alfa_ord(reversed_index):
    return dict(sorted(reversed_index.items()))


def create_index_file(reversed_index, file_name="indice.txt"):
    with open(file_name, 'w') as f:
        for word, doc_info in reversed_index.items():
            str_format = [f"{doc},{count}" for doc, count in doc_info.items()]
            file_lines = f"{word}: {' '.join(str_format)}\n"

            f.write(file_lines)
    f.close()
    return

def bool_query(reversed_index, consult_bool, base_files, output_file="resposta.txt"):
    f = open(output_file, 'w')
    try:
        for query in consult_bool:
            result_docs = set()

            terms = query.split()
            if terms:
                if terms[0].startswith("!"):
                    first_word = terms[0][1:]  # Remover o operador de negação
                    result_docs = set(reversed_index.get(first_word, {}).keys())
                    result_docs = set()

                else:
                    result_docs = set(reversed_index.get(terms[0], {}).keys())

                for i in range(1, len(terms)):
                    term = terms[i]

                    if term == "&":
                        i += 1
                        if i < len(terms):
                            next_word = terms[i]
                            result_docs.intersection_update(reversed_index.get(next_word, {}).keys())

                    elif term == "|":
                        i += 1
                        if i < len(terms):
                            next_word = terms[i]
                            result_docs.update(reversed_index.get(next_word, {}).keys())

                    elif term.startswith("!"):
                        next_word = term[1:]
                        if next_word in reversed_index:
                            result_docs.difference_update(reversed_index[next_word].keys())

            file_names = [base_files[doc - 1] for doc in sorted(result_docs)]

            f.write(f"{len(result_docs)}\n")
            for file_name in file_names:
                f.write(f"{file_name}\n")
    finally:
        f.close()


def main():
    nlp = spacy.load("pt_core_news_lg")
    reversed_index = {}

    if len(sys.argv) != 3:
        print("Uso correto: python3 modelo_booleano.py base.txt consulta.txt")
        sys.exit(1)

    if sys.argv[1] == "" or sys.argv[2] == "":
        print("Uso correto: python3 modelo_booleano.py base.txt consulta.txt")
        sys.exit(1)

    base_path = sys.argv[1]
    consult_path = sys.argv[2]

    # 1 - INDICE INVERTIDO ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    base_files = read_file(base_path)
    print(base_files)

    file_count = 0

    for file in base_files:
        file_count += 1
        file_raw = read_file(file)
        file_raw = str(file_raw)

        file_info = nlp(file_raw)
        # print(file_info)

        tokens = list(file_info)

        for token in tokens:
            if not token.is_stop and not token.is_punct:
                word = token.text

                if word not in reversed_index:
                    reversed_index[word] = {file_count: 1}
                else:

                    if file_count in reversed_index[word]:
                        reversed_index[word][file_count] += 1
                    else:
                        reversed_index[word][file_count] = 1

    # print(reversed_index)
    reversed_index_ord = alfa_ord(reversed_index)
    create_index_file(reversed_index_ord)

    # 2 - CONSULTA BOOLEANA ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    consult_bool = read_file(consult_path)
    # print(consult_bool)
    bool_query(reversed_index_ord, consult_bool, base_files)


main()

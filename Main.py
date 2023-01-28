import sys
sys.path.insert(1, './Análise léxica')

import AnalisadorLexico as lex
import pandas as pd

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabela_tokens = lex.realizarAnaliseLexica(codigo)

# Guardando resultado da analise em um arquivo
arquivo = open("SaídaLéxico.txt", 'w')
str = tabela_tokens.to_string()
arquivo.write(str)

# Imprimindo toda a tabela no console de execucao
with pd.option_context('display.max_rows', None,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ): print(tabela_tokens)
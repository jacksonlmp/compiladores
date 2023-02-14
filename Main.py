import sys
sys.path.insert(1, './AnaliseLexica')
import AnalisadorLexico as lex
import pandas as pd
from tabulate import tabulate

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabela_tokens = lex.realizarAnaliseLexica(codigo)

# Imprimindo toda a tabela no console de execucao
with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                       'display.precision', 3,
                       ): print(tabulate(tabela_tokens, headers='keys', tablefmt='pretty'))

codigo.close()
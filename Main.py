import sys
sys.path.insert(1, './AnaliseLexica')
sys.path.insert(1, './AnaliseSintatica')
import AnalisadorLexico as lex
import AnalisadorSintatico as sint
import pandas as pd
from tabulate import tabulate

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabelaDeTokens = lex.realizarAnaliseLexica(codigo)

codigo.close()

with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                       'display.precision', 3,
                       ): print(tabulate(tabelaDeTokens, headers='keys', tablefmt='pretty'))

tabelaDeSimbolos = sint.realizarAnaliseSintatica(tabelaDeTokens)
print(tabulate(tabelaDeSimbolos, headers='keys', tablefmt='pretty'))
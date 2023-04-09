import sys
sys.path.insert(1, './AnaliseLexica')
sys.path.insert(1, './AnaliseSintatica')
sys.path.insert(1, './AnaliseSemantica')
sys.path.insert(1, './CodigoIntermediario')
import AnalisadorLexico as lex
import AnalisadorSintatico as sint
import AnalisadorSemantico as semantico
import TresEnderecos as tradutorCodigo3End
import pandas as pd
from tabulate import tabulate

def imprimirTabelaDeTokens(tabelaDeTokens):
    print('+-----+--------------------+----------------+-------+')
    print('|                 Tabela de tokens                  |')
    print
    with pd.option_context('display.max_rows', None,
                            'display.max_columns', None,
                        'display.precision', 3,
                        ): print(tabulate(tabelaDeTokens, headers='keys', tablefmt='pretty'))


def imprimirTabelaSimbolos(tabelaDeSimbolos):
    print('\n+----+----------------+----------------+---------+-------+------------------+---------------+--------------+----------------+----------------+')
    print('|                                                            Tabela de simbolos                                                              |')
    print(tabulate(tabelaDeSimbolos, headers='keys', tablefmt='pretty'))


def imprimirCodigoIntermediario(tabelaDeTokens, tabelaDeSimbolos):
    print('\n+-----+--------------------+----------------+-------+')
    print('|              Codigo de 3 enderecos                |')
    tradutorCodigo3End.gerarCodigo(tabelaDeTokens, tabelaDeSimbolos)
    print('+-----+--------------------+----------------+-------+\n')

# Programa a ser analisado
codigo = open('CodigoDeExemplo.txt', 'r')

tabelaDeTokens = lex.realizarAnaliseLexica(codigo)

codigo.close()

imprimirTabelaDeTokens(tabelaDeTokens)

tabelaDeSimbolos = sint.realizarAnaliseSintatica(tabelaDeTokens)
semantico.realizarAnaliseSemantica(tabelaDeTokens, tabelaDeSimbolos)

imprimirTabelaSimbolos(tabelaDeSimbolos)
imprimirCodigoIntermediario(tabelaDeTokens, tabelaDeSimbolos)

print("Codigo compilado com sucesso!")
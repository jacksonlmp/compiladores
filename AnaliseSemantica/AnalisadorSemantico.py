import pandas as pd
import VerificadorDeRegras as semantico
import UnicidadeDeNomes as unicidade

def lookAhead(posicao):
    return posicao + 1

# Percorre toda a tabela de tokens, atribuindo aos metodos responsaveis por cada verificacao
def realizarAnaliseSemantica(tabelaDeTokens, tabelaDeSimbolos):
    tokens = (tabelaDeTokens[tabelaDeTokens.columns[0:1:]]).values
    lexemas = (tabelaDeTokens[tabelaDeTokens.columns[1:2:]]).values
    numeroLinhas = (tabelaDeTokens[tabelaDeTokens.columns[2:3:]]).values

    tabelaDeSimbolos = semantico.verificarTipoDeParametroEArgumentoDeProcedimento(tabelaDeSimbolos)
    tabelaDeSimbolos = semantico.verificarTipoDeParametroEArgumentoDeFuncao(tabelaDeSimbolos)

    unicidade.verificarUnicidadeDeNomes(tabelaDeSimbolos)
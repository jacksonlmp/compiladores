import pandas as pd
import VerificadorDeRegras as semantico

def lookAhead(posicao):
    return posicao + 1

# Percorre toda a tabela de tokens, atribuindo aos metodos responsaveis por cada verificacao
def realizarAnaliseSemantica(tabelaDeTokens, tabelaDeSimbolos):
    tokens = (tabelaDeTokens[tabelaDeTokens.columns[0:1:]]).values
    lexemas = (tabelaDeTokens[tabelaDeTokens.columns[1:2:]]).values
    numeroLinhas = (tabelaDeTokens[tabelaDeTokens.columns[2:3:]]).values

    semantico.verificarTipoDeParametroEArgumentoDeProcedimento(tabelaDeSimbolos)
    semantico.verificarTipoDeParametroEArgumentoDeFuncao(tabelaDeSimbolos)

    quantidadeDeTokens = len(tokens)

    ultimaPosicaoLida = -1 # Para a primeira iteracao, posicaoAtual (zero) deve estar na frente
    for posicaoAtual in range(quantidadeDeTokens):
        if posicaoAtual > ultimaPosicaoLida:
            ultimaPosicaoLida = verificar(posicaoAtual, tokens, lexemas, numeroLinhas, tabelaDeSimbolos)

# Verifica se o codigo esta de acordo com a gramatica
def verificar(posicao, tokens, lexemas, numeroLinhas, tabelaDeSimbolos):
    if tokens[posicao] == 'if' or tokens[posicao] == 'laco':
        return semantico.verificarTiposDentroDeIfEWhile(lookAhead(posicao+1), tokens, lexemas, numeroLinhas, tabelaDeSimbolos)
    return posicao
import pandas as pd
import VerificadorRegras as regras
import ManipuladorTabelaSimbolos as manipuladorTabela

# Faz a analise sintatica e retorna a tabela de simbolos
def realizarAnaliseSintatica(tabelaDeTokens):
    tokens = (tabelaDeTokens[tabelaDeTokens.columns[0:1:]]).values
    lexemas = (tabelaDeTokens[tabelaDeTokens.columns[1:2:]]).values
    numeroLinhas = (tabelaDeTokens[tabelaDeTokens.columns[2:3:]]).values

    analisarSintaxe(tokens, lexemas, numeroLinhas, len(tabelaDeTokens))

    tabelaDeSimbolos = manipuladorTabela.criarTabela(tabelaDeTokens)

    return tabelaDeSimbolos

# Verifica o balanceamento dos parenteses e chaves e se o codigo esta conforme especificado na gramatica
# Em caso de erro, imprime no console e encerra e execucao
def analisarSintaxe(tokens, lexemas, numeroLinhas, quantidadeDeTokens):
    # Verifica se a sequencia de tokens esta correta
    ultimaPosicaoLida = -1 # Para a primeira iteracao, posicaoAtual (zero) deve estar na frente
    for posicaoAtual in range(quantidadeDeTokens):
        if posicaoAtual > ultimaPosicaoLida:
            ultimaPosicaoLida = regras.verificarBloco(posicaoAtual, tokens, lexemas, numeroLinhas)

    regras.verificarBalanceamentoChaveEParentese(tokens)
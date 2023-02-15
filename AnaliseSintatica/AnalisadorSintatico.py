import pandas as pd
import VerificadorRegras as regras

def realizarAnaliseSintatica(tabelaDeTokens):
    tokens = (tabelaDeTokens[tabelaDeTokens.columns[0:1:]]).values
    lexemas = (tabelaDeTokens[tabelaDeTokens.columns[1:2:]]).values
    numeroLinhas = (tabelaDeTokens[tabelaDeTokens.columns[2:3:]]).values

    analisarSintaxe(tokens, lexemas, numeroLinhas, len(tabelaDeTokens))

    # Criar tabela de simbolos
    return "Tabela de simbolos"

# Verifica o balanceamento dos parenteses e chaves e se o codigo esta conforme especificado na gramatica
# Em caso de erro, imprime no console e encerra e execucao
def analisarSintaxe(tokens, lexemas, numeroLinhas, quantidadeDeTokens):
    regras.verificarBalanceamentoChaveEParentese(tokens)

    # Verifica se a sequencia de tokens esta correta
    ultimoIndiceLido = -1 # Para a primeira iteracao, indiceAtual (zero) deve estar na frente
    for indiceAtual in range(quantidadeDeTokens):
        if indiceAtual > ultimoIndiceLido:
            ultimoIndiceLido = regras.verificarBloco(indiceAtual, tokens, lexemas, numeroLinhas)
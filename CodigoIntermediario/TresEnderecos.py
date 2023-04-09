import pandas as pd
import Tradutor as tradutor

def gerarCodigo(tabelaDeTokens, tabelaDeSimbolos):    
    expressoes = []
    # Expressoes de atribuicoes de variaveis
    tamanhoDaTabelaDeSimbolos = len(tabelaDeSimbolos)
    for posicao in range(tamanhoDaTabelaDeSimbolos):
        # Para cada variavel inteira, obtem seu valor
        if tabelaDeSimbolos['Token'][posicao] == 'idVariavel' and tabelaDeSimbolos['Tipo'][posicao] == 'int':
            expressao = tabelaDeSimbolos['Valor'][posicao]
            if(expressao[0] != 'f'): # Nao eh uma funcao
                expressoes.append(expressao)

    # Verificar expressoes dentro de if e while
    lexemas = (tabelaDeTokens[tabelaDeTokens.columns[1:2:]]).values
    quantidadeDeLexemas = len(lexemas)
    '''
    ultimaPosicaoLida = -1 # Para a primeira iteracao, posicaoAtual (zero) deve estar na frente
    for posicaoAtual in range(quantidadeDeLexemas):
        if posicaoAtual > ultimaPosicaoLida:
            if lexemas == 'if' or lexemas == 'while':
                ultimaPosicaoLida = traduzirExpressao(posicaoAtual)
    '''

    tradutor.traduzirExpressoes(expressoes)

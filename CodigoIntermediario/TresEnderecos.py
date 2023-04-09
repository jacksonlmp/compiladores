import pandas as pd
import Tradutor as tradutor

def gerarCodigo(tabelaDeSimbolos):    
    expressoes = []
    # Expressoes de atribuicoes de variaveis
    tamanhoDaTabelaDeSimbolos = len(tabelaDeSimbolos)
    for posicao in range(tamanhoDaTabelaDeSimbolos):
        # Para cada variavel inteira, obtem seu valor
        if tabelaDeSimbolos['Token'][posicao] == 'idVariavel' and tabelaDeSimbolos['Tipo'][posicao] == 'int':
            expressao = tabelaDeSimbolos['Valor'][posicao]
            if(expressao[0] != 'f'): # Nao eh uma funcao
                expressoes.append(expressao)
                               
    tradutor.traduzirExpressoes(expressoes)

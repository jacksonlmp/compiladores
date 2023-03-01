import pandas as pd

# Testar substituicao de tabelaDeTokens["Token"][posicao] por tokens[posicao]

def criarTabela(tabelaDeTokens):
    
    tabelaDeSimbolos = pd.DataFrame(columns=['Token', 'Lexema', 'Tipo', 'Linha', 'Valor', 'QtdParametros', 'Variaveis', 'TiposVariaveis'])

    qtdTokens = len(tabelaDeTokens)
    for posicaoToken in range(qtdTokens):
        # Inserir declaracao de variavel ---> Ex: int vX = 10;
        if tabelaDeTokens["Token"][posicaoToken] == "idVariavel":

            if (tabelaDeTokens["Token"][posicaoToken - 1] == "tipo") and (tabelaDeTokens["Token"][posicaoToken + 1] == "atribuicao"):
                valor = ""
                posicaoLexema = posicaoToken + 2 # Depois do sinal de igual da atribuicao
                # Avalia toda a expressao apos a atribuicao para salvar o resultado final
                while tabelaDeTokens["Token"][posicaoLexema] != "pontoEVirgula":
                    valor += tabelaDeTokens["Lexema"][posicaoLexema]
                    posicaoLexema += 1

                tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["idVariavel", tabelaDeTokens["Lexema"][posicaoToken], tabelaDeTokens["Lexema"][posicaoToken - 1], tabelaDeTokens["Linha"][posicaoToken], valor, "NA","NA","NA"]
            else:
                continue
        
        # Inserir declaracao de procedimento ---> Ex: proc pTeste(int vA, int vB) { ... }
        elif tabelaDeTokens["Token"][posicaoToken] == "procedimento":
            posicaoAux = posicaoToken + 3 # Depois da abertura de parentese, para analisar os argumentos
            qtdParametros = 0
            variaveis = []
            tiposVariaveis = []
            while (tabelaDeTokens["Token"][posicaoAux] != "fechaParentese"):
                if tabelaDeTokens["Token"][posicaoAux] == "idVariavel":
                    qtdParametros += 1
                    variaveis.append(tabelaDeTokens["Lexema"][posicaoAux])
                elif tabelaDeTokens["Token"][posicaoAux] == "tipo":
                    tiposVariaveis.append(tabelaDeTokens["Lexema"][posicaoAux])

                posicaoAux += 1
            tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["procedimento", tabelaDeTokens["Lexema"][posicaoToken + 1], "NA", tabelaDeTokens["Linha"][posicaoToken], "NA", qtdParametros, variaveis, tiposVariaveis]

        # Inserir declaracao de funcao ---> Ex: func int fTeste(int vA, int vB) { ... return vResultado; }
        elif tabelaDeTokens["Token"][posicaoToken] == "funcao":
            posicaoAux = posicaoToken + 4 # Depois da abertura de parentese, para analisar os argumentos
            qtdParametros = 0
            variaveis = []
            tiposVariaveis = []
            while (tabelaDeTokens["Token"][posicaoAux] != "fechaParentese"):
                if tabelaDeTokens["Token"][posicaoAux] == "idVariavel":
                    qtdParametros += 1
                    variaveis.append(tabelaDeTokens["Lexema"][posicaoAux])
                elif tabela_tokens["Token"][j] == "tipo":
                    tiposVariaveis.append(tabelaDeTokens["Lexema"][posicaoAux])

                posicaoAux += 1

            tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["funcao", tabelaDeTokens["Lexema"][posicaoTokeni + 2], tabelaDeTokens["Lexema"][posicaoToken + 1], tabelaDeTokens["Linha"][posicaoToken], "NA", qtdParametros, variaveis, tiposVariaveis]

    return tabelaDeSimbolos
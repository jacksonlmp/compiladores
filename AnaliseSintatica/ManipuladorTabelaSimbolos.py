import pandas as pd
import sys
sys.path.insert(1, '../AnaliseSemantica')
import VerificadorDeRegras as semantico

def criarTabela(tabelaDeTokens):
    
    tabelaDeSimbolos = pd.DataFrame(columns=['Token', 'Lexema', 'Tipo', 'Linha', 'Valor', 
    'QtdParametros', 'Variaveis', 'TiposVariaveis', 'Escopo'])

    qtdTokens = len(tabelaDeTokens)
    for posicaoToken in range(qtdTokens):
        # Inserir declaracao de variavel ---> Ex: int vX = 10;
        if tabelaDeTokens["Token"][posicaoToken] == "idVariavel":

            if (tabelaDeTokens["Token"][posicaoToken - 1] == "tipo") and (tabelaDeTokens["Token"][posicaoToken + 1] == "atribuicao"):
                valor = ""
                posicaoLexema = posicaoToken + 2 # Depois do sinal de igual da atribuicao

                escopo = semantico.verificarEscopo(tabelaDeTokens, posicaoToken)
                
                qtdParametros = 0
                variaveis = []
                tiposVariaveis = []
                ehFuncaoOuProcedimento = False
                if tabelaDeTokens["Token"][posicaoToken+2] == 'idFuncao' or  tabelaDeTokens["Token"][posicaoToken+2] == 'idProcedimento':
                    ehFuncaoOuProcedimento = True

                # Avalia toda a expressao apos a atribuicao para salvar o resultado final
                token = tabelaDeTokens["Token"][posicaoLexema]
                while token != "pontoEVirgula":
                    valor += tabelaDeTokens["Lexema"][posicaoLexema]

                    if ehFuncaoOuProcedimento:
                        if token in ["idVariavel", "constante", "booleano"]:
                            qtdParametros += 1
                            variaveis.append(tabelaDeTokens["Lexema"][posicaoLexema])

                        if token == 'constante':
                            tiposVariaveis.append('int')
                        elif token == 'booleano':
                            tiposVariaveis.append('boolean')
                        elif token == 'idVariavel':
                            tiposVariaveis.append('?')

                    posicaoLexema += 1
                    token = tabelaDeTokens["Token"][posicaoLexema]

                if variaveis == []:
                    tiposVariaveis = []

                tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["idVariavel", tabelaDeTokens["Lexema"][posicaoToken], 
                    tabelaDeTokens["Lexema"][posicaoToken - 1], tabelaDeTokens["Linha"][posicaoToken], valor, qtdParametros,
                    variaveis, tiposVariaveis, escopo]
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
            tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["procedimento", tabelaDeTokens["Lexema"][posicaoToken + 1], 
            "NA", tabelaDeTokens["Linha"][posicaoToken], "NA", qtdParametros, variaveis, tiposVariaveis, "NA"]

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
                elif tabelaDeTokens["Token"][posicaoAux] == "tipo":
                    tiposVariaveis.append(tabelaDeTokens["Lexema"][posicaoAux])

                posicaoAux += 1

            tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["funcao", tabelaDeTokens["Lexema"][posicaoToken + 2], 
            tabelaDeTokens["Lexema"][posicaoToken + 1], tabelaDeTokens["Linha"][posicaoToken], "NA", qtdParametros, 
            variaveis, tiposVariaveis, "NA"]

        # Inserir chamada de procedimento ---> Ex:pImprimirDobro(vSoma);
        elif tabelaDeTokens["Token"][posicaoToken] == "idProcedimento" and tabelaDeTokens["Token"][posicaoToken-1] != 'procedimento':
            posicaoAux = posicaoToken + 1 # Depois da abertura de parentese, para analisar os argumentos
            qtdParametros = 0
            variaveis = []
            tiposVariaveis = []
            token = tabelaDeTokens["Token"][posicaoAux]
            while (token != "fechaParentese"):
                
                if token in ["idVariavel", "constante", "booleano"]:
                    qtdParametros += 1
                    variaveis.append(tabelaDeTokens["Lexema"][posicaoAux])

                    if token == 'constante':
                        tiposVariaveis.append('int')
                    elif token == 'booleano':
                        tiposVariaveis.append('boolean')
                    elif token == 'idVariavel':
                        tiposVariaveis.append('?')

                posicaoAux += 1
                token = tabelaDeTokens["Token"][posicaoAux]

            if variaveis == []:
                tiposVariaveis = []

            escopo = semantico.verificarEscopo(tabelaDeTokens, posicaoToken)
            tabelaDeSimbolos.loc[len(tabelaDeSimbolos)] = ["idProcedimento", tabelaDeTokens["Lexema"][posicaoToken], 
            "NA", tabelaDeTokens["Linha"][posicaoToken], "NA", qtdParametros, 
            variaveis, tiposVariaveis, escopo]

    return tabelaDeSimbolos
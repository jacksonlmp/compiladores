import numpy as np
import sys
sys.path.insert(1, '../AnaliseSemantica')
import VerificadorDeRegras as semantico

# Adianta o ponteiro para ler uma casa a frente
def lookAhead(posicao):
    return posicao + 1

def mensagemErro(mensagem):
    if(isinstance(mensagem, np.ndarray)):
        print(mensagem[0])
    else:
        print(mensagem)
    exit()

# Verifica se as chaves e os parenteses estao duplamente balanceados e retorna o erro caso haja
def verificarBalanceamentoChaveEParentese(listaDeTokens):
    chavesAbertas = 0
    chavesFechadas = 0

    parentesesAbertos = 0
    parentesesFechados = 0

    for token in listaDeTokens:
        if token == "abreChave":
            chavesAbertas += 1
        elif token == "fechaChave":
            chavesFechadas += 1
        elif token == "abreParentese":
            parentesesAbertos += 1
        elif token == "fechaParentese":
            parentesesFechados += 1

    if chavesAbertas > chavesFechadas:
        mensagemErro("Atencao no balanceamento de chaves. Ha mais { do que }.")
    elif chavesAbertas < chavesFechadas:
        mensagemErro("Atencao no balanceamento de chaves. Ha mais } do que {.")

    if parentesesAbertos > parentesesFechados:
        mensagemErro("Atencao no balanceamento de parenteses. Ha mais ( do que ).")
    elif parentesesAbertos < parentesesFechados:
        mensagemErro("Atencao no balanceamento de parenteses. Ha mais ) do que (.")

# Verifica se o codigo esta de acordo com a gramatica
def verificarBloco(posicao, tokens, lexemas, numeroLinhas):
    try:
        if tokens[posicao] == "tipo":
            posicao = lookAhead(posicao)
            return verificarDeclaracaoDeVariavel(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao]  == "if":
            posicao = lookAhead(posicao)
            return verificarIf(posicao, tokens, lexemas, numeroLinhas)
        
        elif tokens[posicao]  == "laco":
            posicao = lookAhead(posicao)
            return verificarLaco(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao]  == "funcao":
            posicao = lookAhead(posicao)
            return verificarDeclaracaoDeFuncao(posicao, tokens, lexemas, numeroLinhas)
        
        elif tokens[posicao]  == "procedimento":
            posicao = lookAhead(posicao)
            return verificarDeclaracaoDeProcedimento(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao]  == "idProcedimento":
            posicao = lookAhead(posicao)
            return verificarChamadaDeProcedimento(posicao, tokens, lexemas, numeroLinhas)

        elif tokens[posicao]  == "print":
            posicao = lookAhead(posicao)
            return verificarPrint(posicao, tokens, lexemas, numeroLinhas)

        else:
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) + ". Lexema "+ lexemas[posicao]
                + " nao esperado. Linguagem nao reconhecida.")

    except IndexError:
        mensagemErro("Excecao: ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1][0]) + ". Linguagem nao reconhecida.")

def verificarDeclaracaoDeVariavel(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "idVariavel":
        posicao = lookAhead(posicao)
        if tokens[posicao]  == "atribuicao":
            posicao = lookAhead(posicao)
            # Analisa se apos a igualdade, ha uma expressao atribuindo valor a variavel
            posicao = verificarExpressao(posicao, tokens, lexemas, numeroLinhas)
            
            # Chegou ao fim. Caso nao indique termino, ocorreu erro sintatico
            if tokens[posicao]  == "pontoEVirgula":
                return posicao
            else:
                mensagemErro("Ocorreu um erro sintatico na declaracao de variavel. Linha " + str(numeroLinhas[posicao][0]) 
                    + ". Lexema " + lexemas[posicao]  + " nao esperado.")
        else:
            mensagemErro("Ocorreu um erro sintatico na atribuicao de variavel. Linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao]  + " nao esperado. Era esperado um =")
    else:
        mensagemErro("Ocorreu um erro sintatico na declaracao de variavel. Linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao]  + " nao esperado.")

# Verifica a estrutura condicional
def verificarIf(posicao, tokens, lexemas, numeroLinhas):
    try:
        if tokens[posicao]  == "abreParentese":
            posicao = lookAhead(posicao)

            # Analisar expressao dentro da estrutura condicional
            posicao = verificarExpressao(posicao, tokens, lexemas, numeroLinhas)

            # Continuacao da condicao apos a expressao
            if tokens[posicao]  == "fechaParentese":
                posicao = lookAhead(posicao)
                
                if tokens[posicao]  == "abreChave":
                    posicao = lookAhead(posicao)
                    while(tokens[posicao]  != "fechaChave"):
                        posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                        posicao = lookAhead(posicao)
                    
                    # Finalizou a execucao. Ou terminou o if ou aconteceu erro (analisamos proximo caractere para verificar)
                    posicao = lookAhead(posicao)
                    if posicao < (len(tokens) - 1):
                        if tokens[posicao]  == "else":
                            posicao = lookAhead(posicao)
                            posicao = verificarElse(posicao, tokens, lexemas, numeroLinhas)
                        else:
                            return posicao - 1
                    return posicao
                else:
                    mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao][0]) 
                        + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de chaves.")
            else:
                mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao][0]) 
                    + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado um fechamento de parenteses.")
        else:
                mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao][0]) 
                    + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de parenteses.")
    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na esturuta condicional. Linha " + str(numeroLinhas[posicao - 1][0]) 
            + ". Lexema " + lexemas[posicao - 1] + " nao esperado.")

# Verifica parte contraria da estrutura condicional
def verificarElse(posicao, tokens, lexemas, numeroLinhas):
    try:    
        if tokens[posicao]  == "abreChave":
            posicao = lookAhead(posicao) 
            while(tokens[posicao]  != "fechaChave"): 
                posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                posicao = lookAhead(posicao)
            
            # Finalizou a execucao. Ou terminou o else ou aconteceu erro
            return posicao    
            
        else:
            mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao][0]) 
                        + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de chaves.")
    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao - 1][0]) 
            + ". Lexema " + lexemas[posicao - 1] + " nao esperado.") 

def verificarLaco(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "abreParentese":
        posicao = verificarExpressao(lookAhead(posicao), tokens, lexemas, numeroLinhas)

        if tokens[posicao] == "fechaParentese":
            posicao = lookAhead(posicao)

            if tokens[posicao] == "abreChave":
                posicao = lookAhead(posicao)
                while tokens[posicao] != "fechaChave":
                    posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                    posicao = lookAhead(posicao)

                    if tokens[posicao] == "auxLaco":
                        posicao = lookAhead(posicao)
                        if tokens[posicao] == "pontoEVirgula":
                            posicao = lookAhead(posicao)
                        else:
                            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
                                + ". Token " + tokens[posicao] + " nao esperado. Era esperado um ;")

                    if posicao > len(tokens)-1:
                        mensagemErro("Ocorreu um erro sintatico. Faltou fechar chaves apos ultima linha")
                
                if tokens[posicao] == "fechaChave":
                    return posicao
                else:
                    mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0])
                        + ". Token " + tokens[posicao] + " nao esperado. Era esperado um fechamento de chave.")
            else:
                mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
                + ". Token " + tokens[posicao] + " nao esperado. Era esperado uma abertura de chave.")
        else:
            mensagemErro("Ocorreu um erro na linha " + str(numeroLinhas[posicao][0])
                + ". Token " + tokens[posicao] + " nao esperado. Era esperado um fechamento de parentese ou expressao valida.")
    else:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
            + ". Token " + tokens[posicao] + " nao esperado. Era esperado uma abertura de parentese.")

def verificarDeclaracaoDeFuncao(posicao, tokens, lexemas, numeroLinhas):
    try:
        if(tokens[posicao] == 'tipo'):
            tipoFuncao = lexemas[posicao]
            posicao = lookAhead(posicao)

            if(tokens[posicao] == 'idFuncao'):
                posicao = lookAhead(posicao)

                if(tokens[posicao] == 'abreParentese'):
                    posicao = lookAhead(posicao)
                    posicao = verificarParametros(posicao, tokens, lexemas, numeroLinhas)
                    
                    if(tokens[posicao] == 'abreChave'):
                        achouReturn = False
                        achouFechaChave = False
                        while not (achouReturn or achouFechaChave) :
                            posicao = lookAhead(posicao)

                            if(tokens[posicao] == 'return'):
                                achouReturn = True  
                                posicao = lookAhead(posicao)   
                                posicao = verificarReturn(posicao, tokens, lexemas, numeroLinhas, tipoFuncao)
                            
                            elif(tokens[posicao] == "fechaChave"):
                                achouFechaChave = True
                                mensagemErro("Ocorreu um erro sintatico na declaracao de funcao. Linha "+ str(numeroLinhas[posicao][0])
                                      +" - '"+ lexemas[posicao] + "' nao esperado. Era esperado um retorno da funcao.")

                            else:
                                posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                        if(achouReturn and tokens[posicao] != 'fechaChave'):
                            mensagemErro("Ocorreu um erro sintatico na declaracao de funcao. Linha "+ str(numeroLinhas[posicao][0])
                                      +" - '"+ lexemas[posicao] + "' nao esperado. Era esperado um fechamento de chave apos o retorno da funcao.")
                        return posicao
                    else:
                        mensagemErro("Ocorreu um erro sintatico na declaracao de funcao. Linha "+ str(numeroLinhas[posicao][0])
                                      +" - '"+ lexemas[posicao] + "' nao esperado. Era esperado uma abertura de chave.")
                else:
                    mensagemErro("Ocorreu um erro sintatico na declaracao de funcao. Linha "+ str(numeroLinhas[posicao][0])
                                  +" - '"+ lexemas[posicao] + "' nao esperado. Era esperado uma abertura de parentese.")
            else:
                mensagemErro("Ocorreu um erro sintatico na declaracao de funcao. Linha "+ str(numeroLinhas[posicao][0])
                              +" - '"+ lexemas[posicao] + "' Era esperado o identificador da funcao.")

        else:
            mensagemErro("Ocorreu um erro sintatico na declaracao de funcao. Linha "+ str(numeroLinhas[posicao][0])
                          +" - '"+ lexemas[posicao] + "' nao esperado. Era esperado o tipo de dado de retorno da funcao.")

    except IndexError:
        mensagemErro("Excecao: ocorreu um erro sintatico na declaracao de funcao. Linha " + str(numeroLinhas[posicao -1][0])
                      + " - " + str(lexemas[posicao-1]) + " incorreto.")    

def verificarDeclaracaoDeProcedimento(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "idProcedimento":
        posicao = lookAhead(posicao)

        if tokens[posicao]  == "abreParentese":
            posicao = lookAhead(posicao)
            
            posicao = verificarParametros(posicao, tokens, lexemas, numeroLinhas)
            
            if tokens[posicao]  == "abreChave":
                posicao = lookAhead(posicao)
                while(not tokens[posicao]  == "fechaChave"):
                    posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                    posicao = lookAhead(posicao)
                
                return posicao

            else:
                mensagemErro("Ocorreu um erro sintatico na declaracao de procedimento. Linha " + str(numeroLinhas[posicao][0]) 
                    + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de chaves.")
        else:
            mensagemErro("Ocorreu um erro sintatico na declaracao de procedimento. Linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de parenteses.")
    else:
        mensagemErro("Ocorreu um erro sintatico na declaracao de procedimento. Linha " + str(numeroLinhas[posicao ]) 
            + ". Lexema " + lexemas[posicao] + " nao esperado.")

def verificarChamadaDeProcedimento(posicao, tokens, lexemas, numeroLinhas):
    posicaoAux = posicao

    if tokens[posicao]  != "abreParentese":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
            + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de parentese.")
    
    posicao = verificarArgumentos(lookAhead(posicao), tokens, lexemas, numeroLinhas)
    if tokens[posicao]  != "pontoEVirgula":
         mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
            + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado um ;")
         
    semantico.verificarSeDeclarouProcedimento(posicaoAux, lexemas, numeroLinhas)    
    return posicao

def verificarPrint(posicao, tokens, lexemas, numeroLinhas):
    if (tokens[posicao]  == "idVariavel") or (tokens[posicao]  == "constante"):
        posicao = lookAhead(posicao)
        if tokens[posicao]  == "pontoEVirgula":
            semantico.verificarSeVariavelExiste(posicao-1, tokens, lexemas, str(numeroLinhas[posicao-1][0]))
            #semantico.verificarEscopoDoPrint(...)
            return posicao
        else:
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao] + " nao esperado.")
    else:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao] + " nao esperado. Verifique o parametro informado na impressao")

# Tipos e variaveis nas chamadas de procedimento e funcao
def verificarParametros(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "tipo":
        posicao = lookAhead(posicao)

        if tokens[posicao]  == "idVariavel":
            posicao = lookAhead(posicao) # Obtendo parametro

            # Apenas um parametro eh obrigatorio, logo, pode ter virgula para verificar outros ou finaliza a assinatura do metodo
            if tokens[posicao]  == "virgula":
                    # Como foi virgula, logo temos mais parametros para verificar
                    return verificarParametros(lookAhead(posicao), tokens, lexemas, numeroLinhas)

            elif tokens[posicao]  == "fechaParentese":
                return lookAhead(posicao)

            else:
                mensagemErro("Ocorreu um erro sintatico nos parametros do metodo, era esperado uma virgula ou fechamento de parentese na linha " 
                + str(numeroLinhas[posicao][0]) + ". Lexema " + lexemas[posicao] + " nao esperado.")
        else:
            mensagemErro("Ocorreu um erro sintatico nos parametros do metodo, era esperado o identificador da variavel na linha " 
                + str(numeroLinhas[posicao][0]) + ". Lexema " + lexemas[posicao] + " nao esperado.")

    elif tokens[posicao]  == "fechaParentese": # Nao recebe parametros
                return lookAhead(posicao)

    else:
        mensagemErro("Ocorreu um erro sintatico nos parametros do metodo, era esperado o tipo do parametro na linha " 
            + str(numeroLinhas[posicao][0]) + ". Lexema " + lexemas[posicao] + " nao esperado.")

# Verifica expressoes para condicionais, lacos e expressoes aritmeticas
def verificarExpressao(posicao, tokens, lexemas, numeroLinhas):
    # Espera-se que seja encontrado um termo no look ahead
    try:    
        if tokens[posicao]  == "idFuncao": # Chamada de funcao
            posicao = lookAhead(posicao)
            posicaoDoArgumento = posicao           

            if tokens[posicao]  == "abreParentese":
                posicao = verificarArgumentos(lookAhead(posicao), tokens, lexemas, numeroLinhas)
                
                semantico.verificarTipoRetornoESeDeclarouFuncao(posicaoDoArgumento, lexemas, numeroLinhas)
                return posicao
            else:
                mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao] + " nao esperado. Era esperado uma abertura de parentese.")

        elif tokens[posicao]  in ['idVariavel', 'booleano', 'constante']:
            if tokens[posicao]  == 'booleano' or tokens[posicao-1] == 'operadorRelacional': # Verificando operador relacional para expressao booleana
                if tokens[posicao-1] == 'atribuicao':    
                    semantico.verificarSeVariavelEhBooleana(posicao, lexemas, numeroLinhas)
                    if lexemas[lookAhead(posicao)] in ['!=', '==']:
                        posicao = lookAhead(posicao+1)
                if (tokens[posicao-1] == 'abreParentese' or tokens[posicao-1] == 'operadorRelacional') and (lexemas[lookAhead(posicao)] == '==' or lexemas[lookAhead(posicao)] == '!='):
                    # Concatenacao de expressao booleana -> ex: true == vA == true != false, onde vA eh booleana
                    posicao = lookAhead(posicao)
                    return verificarExpressao(lookAhead(posicao), tokens, lexemas, numeroLinhas)
                return lookAhead(posicao)
            else:
                if tokens[posicao-1] == 'atribuicao': # Verificando atribuicao de variaveis
                    if tokens[posicao] == 'constante':
                        semantico.verificarSeVariavelEhInteira(posicao, tokens, lexemas, numeroLinhas)
                    else:
                        # Atribuicao de uma variavel a outra
                        semantico.verificarSeVariavelExisteETiposSaoIguais(posicao, tokens, lexemas, str(numeroLinhas[posicao][0]))

                elif tokens[posicao] == 'idVariavel' and (tokens[posicao-2] == 'if' or tokens[posicao-2] == 'laco'):
                    # Verificando se variavel usada em if ou while ja foi declarada
                    semantico.verificarSeVariavelExiste(posicao, tokens, lexemas, str(numeroLinhas[posicao-1][0]))

                valores = ['idVariavel', 'constante']
                operadores = ['operadorAritmetico', 'operadorRelacional']
                token = tokens[posicao]

                ehExpressaoValida = True
                while (ehExpressaoValida):
                    posicao = lookAhead(posicao)
                    token = tokens[posicao]
                    if(token in operadores and tokens[lookAhead(posicao)] not in valores): # operador sem outro valor na frente (ex: 10 + vA +)
                        ehExpressaoValida = False
                        mensagemErro("Ocorreu um erro na linha " + str(numeroLinhas[posicao][0])
                        + ". Sentenca do lexema " + lexemas[posicao] + " invalida. Verifique os tipos e a ordem das constantes, variaveis e operadores.")

                    if(token not in valores and token not in operadores):
                        ehExpressaoValida = False

                    if(token == 'idVariavel'):
                        semantico.verificarSeVariavelExiste(posicao, tokens, lexemas, str(numeroLinhas[posicao][0]))

                    # Trecho de analise semantica
                    valorAnterior = tokens[posicao-1]
                    # Se for o operador, envia o valor anterior e o proximo para analise
                    if(valorAnterior in operadores):
                        operador = lexemas[posicao-1]
                        semantico.compararTipos(tokens, lexemas, numeroLinhas[posicao], posicao, operador, posicao-2)
                    
                return posicao
            
        else:
             mensagemErro("Ocorreu um erro sintatico na expressao. Linha " + str(numeroLinhas[posicao][0]) 
                + ". Lexema " + lexemas[posicao] + " invalido. Era esperada um valor, variavel ou chamada de funcao.")
    except IndexError:
        mensagemErro("Excecao na expressao. Ocorreu um erro sintatico na expressao. Linha " + str(numeroLinhas[posicao - 1][0]) 
            + ". Lexema " + lexemas[posicao - 1] + " nao esperado.")

def verificarReturn(posicao, tokens, lexemas, numeroLinhas, tipoFuncao):
    token = tokens[posicao]
    if (token != "idVariavel") and (token != "constante") and (token != "booleano"):
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
            + ". Token " + tokens[posicao] + " nao esperado. Era esperado um dado para retorno da funcao.")

    semantico.verificarTipoRetornadoPorFuncao(posicao, tokens, lexemas, numeroLinhas, tipoFuncao)
    posicao = lookAhead(posicao)

    if tokens[posicao]  != "pontoEVirgula":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao][0]) 
            + ". Token " + tokens[posicao] + " nao esperado. Era esperado um ;")

    return lookAhead(posicao)

# Valores/variaveis nas chamadas de procedimento e funcao
def verificarArgumentos(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "idVariavel":
        posicao = lookAhead(posicao)

        # Apenas um parametro eh obrigatorio, logo, pode ter virgula para verificar outros ou finaliza a assinatura do metodo
        if tokens[posicao]  == "virgula":
                # Como foi virgula, logo temos mais parametros para verificar
                return verificarArgumentos(lookAhead(posicao), tokens, lexemas, numeroLinhas)

        elif tokens[posicao]  == "fechaParentese":
            return lookAhead(posicao)

        else:
            mensagemErro("Ocorreu um erro sintatico nos argumentos do metodo, era esperado uma virgula ou fechamento de parentese na linha " 
            + str(numeroLinhas[posicao][0]) + ". Lexema " + lexemas[posicao] + " nao esperado.")
    
    elif tokens[posicao]  == "fechaParentese": # Nao recebe parametros
            return lookAhead(posicao)
    else:
        mensagemErro("Ocorreu um erro sintatico nos argumentos do metodo, era esperado o identificador da variavel na linha " 
            + str(numeroLinhas[posicao][0]) + ". Lexema " + lexemas[posicao] + " nao esperado.")
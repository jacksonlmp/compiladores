import sys

# Adianta o ponteiro para ler uma casa a frente
def lookAhead(posicao):
    return posicao + 1

def mensagemErro(mensagem):
    print(mensagem)
    sys.stderr.close()

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
        mensagemErro("Ocorreu um erro sintatico no balanceamento de chaves. Ha mais { do que }.")
    elif chavesAbertas < chavesFechadas:
        mensagemErro("Ocorreu um erro sintatico no balanceamento de chaves. Ha mais } do que {.")

    if parentesesAbertos > parentesesFechados:
        mensagemErro("Ocorreu um erro sintatico na balanceamento de parenteses. Ha mais ( do que ).")
    elif parentesesAbertos < parentesesFechados:
        mensagemErro("Ocorreu um erro sintatico no balanceamento de parenteses. Ha mais ) do que (.")

# Verifica se o codigo esta de acordo com a gramatica
def verificarBloco(posicao, tokens, lexemas, numeroLinhas):
    try:
        if tokens[posicao]  == "tipo":
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
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) + ". Lexema "+ lexemas[posicao]
                + " invalido. Linguagem nao reconhecida.")

    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) + ". Lexema " + lexemas[posicao - 1] 
            + " invalido. Linguagem nao reconhecida.")

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
                mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + tokens[posicao]  + " invalido. Verifique a separacao das linhas com ;")
        else:
            mensagemErro("Ocorreu um erro sintatico na atribuicao de variavel. Linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + tokens[posicao]  + " invalido.")
    else:
        mensagemErro("Ocorreu um erro sintatico na declaracao de variavel. Linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + tokens[posicao]  + " invalido.")

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
                    mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                        + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de chaves.")
            else:
                mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + lexemas[posicao] + " invalido. Era esperado um fechamento de parenteses.")
        else:
                mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de parenteses.")
    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) 
            + ". Lexema" + lexemas[posicao - 1] + " invalido.")

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
            mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                        + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de chaves.")
    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) 
            + ". Lexema" + lexemas[posicao - 1] + " invalido.") 

def verificarLaco(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  != "abreParentese":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Token " + tokens[posicao] + " invalido. Era esperado uma abertura de parentese.")

    posicao = lookAhead(posicao)
    posicao = verificarExpressao(posicao, tokens, lexemas, numeroLinhas)

    if tokens[posicao]  != "fechaParentese":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Token " + tokens[posicao] + " invalido. Era esperado um fechamento de parentese.")

    posicao = lookAhead(posicao)

    if tokens[posicao]  != "abreChave":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Token " + tokens[posicao] + " invalido. Era esperado uma abertura de chave.")

    posicao = lookAhead(posicao)

    while tokens[posicao]  != "fechaChave":
        posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
        posicao = lookAhead(posicao)

        if tokens[posicao]  != "auxLaco":
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Token " + tokens[posicao] + " invalido. Era esperado um break ou continue")

        posicao = lookAhead(posicao)

        if tokens[posicao]  != "pontoEVirgula":
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Token " + tokens[posicao] + " invalido. Era esperado um ;")

        posicao = lookAhead(posicao)

        if posicao > len(tokens)-1:
            mensagemErro("Ocorreu um erro sintatico. Faltou fechar chaves apos ultima linha")

    return posicao

def verificarDeclaracaoDeFuncao(posicao, tokens, lexemas, numeroLinhas):
    try:
        if tokens[posicao] != 'tipo':
            mensagemErro("ERRO SINTÁTICO - Linha" + str(numeroLinhas[posicao]) + ". Lexema " + lexemas[posicao] + " Invalido. Era esperado o tipo de dado de retorno da funcao." )

        posicao = lookAhead(posicao)

        if tokens[posicao] != 'IdFuncao':
            mensagemErro("ERRO SINTÁTICO - Linha" + str(numeroLinhas[posicao]) + ". Lexema " + lexemas[posicao] + " Invalido. Era esperado o identificador da funcao.")

        posicao = lookAhead(posicao)

        if tokens[posicao] != 'abreParentese':
            mensagemErro("ERRO SINTÁTICO - Linha" + str(numeroLinhas[posicao]) + ". Lexema" + lexemas[posicao] + " Invalido. Era esperado uma abertura de parentese.")

        posicao = lookAhead(posicao)
        posicao = verificarParametros(tokens, lexemas, numeroLinhas, posicao)

        if tokens[posicao] != 'abreChave':
            mensagemErro("ERRO SINTÁTICO - Linha" + str(numeroLinhas[posicao]) + ". Lexema" + lexemas[posicao] + " Invalido. Era esperado uma abertura de chave.")

        while not (tokens[posicao] == 'fechaChave' and tokens[posicao-3] == 'return'):
            if tokens[posicao] == 'return':
                posicao = lookAhead(posicao)
                posicao = verificarReturn(tokens, lexemas, numeroLinhas, posicao)
            elif tokens[posicao] != 'fechaChave':
                posicao = verificarBloco(tokens, lexemas, numeroLinhas, posicao)
            else:
                break

        return posicao
    
    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) 
            + ". Lexema" + lexemas[posicao - 1] + " invalido.")

def verificarDeclaracaoDeProcedimento(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "idProcedimento":
        posicao = lookAhead(posicao)

        if tokens[posicao]  == "abreParentese":
            posicao = lookAhead(posicao)
            
            posicao = verificarParametros(posicao, tokens, lexemas, numeroLinhas)
            
            if tokens[posicao]  == "abreChave":
                
                while(tokens[posicao]  != "fechaChave"):
                    posicao = lookAhead(posicao) 
                                  
                    if tokens[posicao]  != "fechaChave":
                        posicao = verificarBloco(posicao, tokens, lexemas, numeroLinhas)
                
                return posicao

            else:
                mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                    + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de chaves.")
        else:
            mensagemErro("Ocorreu um erro sintatico na estrutura condicional. Linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de parenteses.")
    else:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao ]) 
            + ". Lexema" + lexemas[posicao] + " invalido.")

def verificarChamadaDeProcedimento(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  != "abreParentese":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de parentese.")
    
    posicao = verificarParametros(lookAhead(posicao), tokens, lexemas, numeroLinhas)
    if tokens[posicao]  != "pontoEVirgula":
         mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Lexema " + lexemas[posicao] + " invalido. Era esperado um ;")
        
    return posicao

def verificarPrint(posicao, tokens, lexemas, numeroLinhas):
    if (tokens[posicao]  == "idVariavel") or (tokens[posicao]  == "constante"):
        posicao = lookAhead(posicao)
        if tokens[posicao]  == "pontoEVirgula":
            return posicao
        else:
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + lexemas[posicao] + " invalido. Verifique a separacao das linhas com ;")
    else:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + lexemas[posicao] + " invalido. Verifique o parametro informado na impressao")

def verificarParametros(posicao, tokens, lexemas, numeroLinhas):
    if tokens[posicao]  == "tipo":
        posicao = lookAhead(posicao)

        if tokens[posicao]  == "idVariavel":
            posicao = lookAhead(posicao) # Obtendo parametro

            # Apenas um parametro eh obrigatorio, logo, pode ter virgula para verificar outros ou finaliza a assinatura do metodo
            if tokens[posicao]  == "virgula":
                    #É virgula, então temos mais parametros para verificar
                    posicao = lookAhead(posicao)
                    posicao = verificarParametros(posicao, tokens, lexemas, numeroLinhas)
                    return posicao

            elif tokens[posicao]  == "fechaParentese":
                posicao = lookAhead(posicao)
                return posicao

            else:
                mensagemErro("Ocorreu um erro sintatico nos parametros do metodo, era esperado uma virgula ou fechamento de parentese na linha " 
                + str(numeroLinhas[posicao]) + ". Lexema " + lexemas[posicao] + " invalido.")
        else:
            mensagemErro("Ocorreu um erro sintatico nos parametros do metodo, era esperado o identificador da variavel na linha " 
                + str(numeroLinhas[posicao]) + ". Lexema " + lexemas[posicao] + " invalido.")

    else:
        mensagemErro("Ocorreu um erro sintatico nos parametros do metodo, era esperado o tipo do parametro na linha " 
            + str(numeroLinhas[posicao]) + ". Lexema " + lexemas[posicao] + " invalido.")

# Verifica expressoes para condicionais, lacos e expressoes aritmeticas
def verificarExpressao(posicao, tokens, lexemas, numeroLinhas):
    # Espera-se que seja encontrado um termo no look ahead
    try:    
        if tokens[posicao]  == "idFuncao":
            posicao = lookAhead(posicao)
                        
            if tokens[posicao]  == "abreParentese":
                posicao = lookAhead(posicao)
                posicao = verificarParametros(posicao, tokens, lexemas, numeroLinhas)
                return posicao
            else:
                mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma abertura de parentese.")

        elif tokens[posicao]  in ['idVariavel', 'booleano', 'constante']:
            if tokens[posicao]  == 'booleano':
                return lookAhead(posicao)

            elif tokens[posicao]  == "constante" and tokens[lookAhead(posicao)] == "pontoEVirgula":
                return lookAhead(posicao)
                
            else:
                posicao = lookAhead(posicao)
                
                if tokens[posicao]  in ['operadorLogico', 'operadorAritmetico']:
                    posicao = lookAhead(posicao)
                    
                    if tokens[posicao]  in ['constante', 'idVariavel']:
                        # Expressao correta
                        return lookAhead(posicao)
                        
                    else:
                        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                        + ". Lexema " + lexemas[posicao] + " invalido. Era esperado uma constante ou variavel.")

                else:
                    mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                        + ". Lexema " + lexemas[posicao] + " invalido. Era esperado um operador logico ou aritmetico.")
                        
        else:
            mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
                + ". Lexema " + lexemas[posicao] + " invalido.")
            
    except IndexError:
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao - 1]) 
            + ". Lexema " + lexemas[posicao - 1] + " invalido.")

def verificarReturn(posicao, tokens, numeroLinhas):
    if tokens[posicao]  != "idVariavel":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Token " + tokens[posicao] + " invalido. Era esperado um identificador de variavel.")

    posicao = lookAhead(posicao)

    if tokens[posicao]  != "pontoEVirgula":
        mensagemErro("Ocorreu um erro sintatico na linha " + str(numeroLinhas[posicao]) 
            + ". Token " + tokens[posicao] + " invalido. Era esperado um ;")

    return lookAhead(posicao)
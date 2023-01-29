import pandas as pd
import VerificadorCaractere as verificador
import ManipuladorTabelaToken as manipuladorTabela

def realizarAnaliseLexica(codigo):

    lexema = "" # Forma os tokens, a partir da leitura da linha
    numeroDaLinhaAtual = 0
    tabelaDeTokens = pd.DataFrame(columns=['Token', 'Lexema', 'Linha'])

    for linha in codigo:
        numeroDaLinhaAtual += 1

        i = 0
        qtdCaracteres = len(linha)
        while(i < qtdCaracteres):
            caractere = linha[i]

            if(verificador.ehCaractereValido(caractere) == False):
                print(f"Ocorreu um erro lexico na linha {numeroDaLinhaAtual}. Caractere '{caractere}' nao foi definido.")
                exit()

            elif verificador.ehEspacoOuQuebraDeLinha(caractere):
                manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual)
                i = i + 1
                lexema = ""
                continue

            elif verificador.ehParenteseChavePontoEVirgula(caractere):
                if lexema != "": # Possui token para salvar
                     manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual) # Guardou na tabela o token que estava lendo
                
                lexema = caractere 
                token = verificador.traduzParenteseChaveOuPontoEVirgula(lexema)
                manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token) # Guardou chave, ponto e virgula ou parentese
                i = i + 1
                lexema = ""
                continue
            
            #################### Verificar os operadores logicos ####################

            elif (i+1) < qtdCaracteres and verificador.identificarAritmeticoOuAtribuicao(caractere, linha[i+1], i) != -1:  
                novoIndice = verificador.identificarAritmeticoOuAtribuicao(caractere, linha[i+1], i)
                
                if lexema == "": # Nao tem token a ser salvo no momento
                    if(novoIndice != i): # 2 tokens juntos
                        lexema = caractere + linha[i+1]
                        token = verificador.identificarTipoOperadorLogico(lexema)
                        manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token)
                        i+=2 # Inserimos um operador logico com mais de um caractere ('>=' ou '<='), logo, foram lidos dois caracteres
                    else: # Apenas um token
                        lexema = caractere 
                        token = verificador.identificarTipoOperadorLogico(lexema)
                        manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token)
                        i+=1
                    lexema = ""
                    continue
                else: 
                    manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual) # Guarda o token que estava sendo lido no momento
                    lexema = caractere 
                    token = verificador.identificarTipoOperadorLogico(lexema)
                    manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token) # Salva o operador
                    lexema = ""
                    i+=1
                    continue

            #################### Verificar os operadores aritmeticos ####################

            elif verificador.ehAritmeticoAtribuicaoOuVirgula(caractere):
                if lexema != "":
                    manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual)
                
                lexema = caractere 
                token = verificador.identificarTipoAritmeticoAtribuicaoOuVirgula(lexema)
                manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token)
                lexema = ""
                i+=1
                continue

            else:
                lexema = lexema + caractere # O caractere nao formou token ainda, entao incrementa o lexema com o que foi lido

            i+=1

        # Verifica se chegou ao fim da linha (nao possui mais caracteres)
        if(len(lexema) != 0):
            manipuladorTabela.inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual)
            lexema = ""

    return tabelaDeTokens
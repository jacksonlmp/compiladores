import VerificadorCaractere as verificador
import pandas as pd

lexema = "" # Forma os tokens, a partir da leitura da linha
numeroDaLinhaAtual = 0
tabelaDeTokens = pd.DataFrame(columns=['Token', 'Lexema', 'Linha'])

def realizarAnaliseLexica(codigo):
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
                inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual)
                i = i + 1
                lexema = ""
                continue

            elif verificador.ehParenteseChavePontoEVirgula(caractere):
                if lexema != "": # Possui token para salvar
                     inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual) # Guardou na tabela o token que estava lendo
                
                lexema = caractere 
                token = verificador.traduzParenteseChaveOuPontoEVirgula(lexema)
                inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token) # Guardou chave, ponto e virgula ou parentese
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
                        inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token)
                        i+=2 # Inserimos um operador logico com mais de um caractere ('>=' ou '<='), logo, foram lidos dois caracteres
                    else: # Apenas um token
                        lexema = caractere 
                        token = verificador.identificarTipoOperadorLogico(lexema)
                        inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token)
                        i+=1
                    lexema = ""
                    continue
                else: 
                    inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual) # Guarda o token que estava sendo lido no momento
                    lexema = caractere 
                    token = verificador.identificarTipoOperadorLogico(lexema)
                    inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token) # Salva o operador
                    lexema = ""
                    i+=1
                    continue

            #################### Verificar os operadores aritmeticos ####################

            elif verificador.ehAritmeticoAtribuicaoOuVirgula(caractere):
                if lexema != "":
                    inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual)
                
                lexema = caractere 
                token = verificador.identificarTipoAritmeticoAtribuicaoOuVirgula(lexema)
                inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token)
                lexema = ""
                i+=1
                continue

            else:
                lexema = lexema + caractere # O caractere nao formou token ainda, entao incrementa o lexema com o que foi lido

            i+=1

        # Verifica se chegou ao fim da linha (nao possui mais caracteres)
        if(len(lexema) != 0):
            inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual)
            lexema = ""

    return tabelaDeTokens


#################### Funcoes da tabela de tokens ####################

def verificaToken(lexema, numeroDaLinhaAtual):
    tokens = {
        'laco': ['while'],
        'condicional': ['if', 'else'],
        'tipo': ['int', 'float', 'string'],
        'booleano': ['True', 'False'],
        'funcao': ['func'],
        'return': ['return'],
        'print': ['print'],
        'procedimento': ['proc'],
        'id_funcao': ['f'],
        'id_variavel': ['v'],
        'id_procedimento': ['p'],
        'aux_laco': ['break', 'continue'],
    }
    if(lexema == ''):
        return ''
    else:
        for tokens, lexemas in tokens.items():
            if lexema in lexemas:
                return tokens
        try:
            int(lexema)
            return "constante"
        except ValueError:
            print(f"Ocorreu um erro lexico na linha {numeroDaLinhaAtual}. Lexema '{lexema}' invalido.")
            exit()

# Salva o token na tabela
def inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token=None):
    if lexema:
        if not token:
            token = verificaToken(lexema, numeroDaLinhaAtual)
        tabelaDeTokens.loc[len(tabelaDeTokens)] = [token, lexema, numeroDaLinhaAtual]
    lexema = ""
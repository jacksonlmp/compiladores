import pandas as pd

palavrasReservadas = {
    "while": "laço",
    "if": "if",
    "else": "else",
    "int" : "tipo",
    "boolean": "tipo",
    "func": "funcao",
    "return": "return",
    "print": "print",
    "proc": "procedimento",
    "break": "auxLaco",
    "continue": "auxLaco"
}

def verificarToken(lexema, numero_linha):
    if(lexema == ''):
        return ''
    else:
        tokens = palavrasReservadas.get(lexema)
        if tokens:
            return tokens
        elif lexema[0] == 'v':
            return 'IdVariavel'
        elif lexema[0] == 'f':
            return 'IdFuncao'
        elif lexema[0] == 'p':
            return 'IdProcedimento'
        else:
            try:
                constante = int(lexema)
                return "constante"
            except:
                print("="*25)
                print("Erro lexico na linha "+ str(numero_linha))
                print("Lexema '"+ lexema +"' invalido.")
                print("="*25)
                exit()

# Salva o token na tabela
def inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token=None):
    if lexema:
        if not token:
            token = verificarToken(lexema, numeroDaLinhaAtual)
        tabelaDeTokens.loc[len(tabelaDeTokens)] = [token, lexema, numeroDaLinhaAtual]
    lexema = ""
import pandas as pd

def verificarToken(lexema, numeroDaLinhaAtual):
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
            print(f"Erro lexico na linha {numeroDaLinhaAtual}. Lexema '{lexema}' invalido.")
            exit()

# Salva o token na tabela
def inserirToken(lexema, tabelaDeTokens, numeroDaLinhaAtual, token=None):
    if lexema:
        if not token:
            token = verificarToken(lexema, numeroDaLinhaAtual)
        tabelaDeTokens.loc[len(tabelaDeTokens)] = [token, lexema, numeroDaLinhaAtual]
    lexema = ""
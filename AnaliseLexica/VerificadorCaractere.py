# Tipos de tokens
laco = ['while']
booleanos = ['true', 'false']
condicionais = ['if', 'else']
tipos = ['int', 'boolean']
constantes = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

caracteres = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
    ";", "(", ")", "{", "}", " ", "\n", ">", "<", 
    "=", "!", "+", "-", "*", "/", ","
]

def getOperadoresLogicos():
    return [">=", ">", "<", "<=", "!=", "=="]

def getOperadoresAritmeticos():
    return ["+", "-", "*", "/"]


#################### Funcoes de verificacao de caracteres ####################

# Indica se a linguagem aceita o caractere informado
def ehCaractereValido(caractere):
    return caractere in caracteres

# Identifica se o caractere encontrado eh um espaco ou uma quebra de linha
def ehEspacoOuQuebraDeLinha(caractere):
    return (caractere == " ") or (caractere == "\n")

# Identifica se o lexema e um operador aritmetico, uma atribuicao ou uma virgula
def identificarTipoAritmeticoAtribuicaoOuVirgula(lexema):
    if lexema == "=":
        return "atribuicao"
    elif lexema == ";":
        return "pontoEVirgula"
    elif lexema == ",":
        return "virgula"
    elif lexema in getOperadoresAritmeticos():
        return "operadorAritmetico"

# Identifica se o lexema e um operador logico    
def identificarTipoOperadorLogico(lexema):
    if lexema in getOperadoresLogicos():
        return "operadorLogico"

def ehAritmeticoAtribuicaoOuVirgula(caractere):
    if caractere == "=":
        return True
    elif caractere == ";" or caractere == ",":
        return True
    elif caractere in getOperadoresAritmeticos():
        return True

    return False

# Identifica se eh parentese, chave ou ponto e virgula
def ehParenteseChavePontoEVirgula(caractere):
    return caractere in set("(){};")

# Converte o caractere parentese, chave ou ponto em virgula em uma string
def traduzParenteseChaveOuPontoEVirgula(caractere):
    caracteres = {
        "(": "abreParentese",
        ")": "fechaParentese",
        "{": "abreChave",
        "}": "fechaChave",
        ";": "pontoEVirgula"
    }
    return caracteres.get(caractere)

# Identifica se eh uma atribuicao ou um operador logico aritmetico
def identificarAritmeticoOuAtribuicao(caractere, proximoCaractere, indice):
    if (caractere == ">") or (caractere == "<"):
        return (indice + 1 if proximoCaractere == '=' else indice)

    elif ((caractere == "=" or caractere == "!") and proximoCaractere == '='):
            return indice + 1
    
    else:
        return -1 # Nao reconheceu
import pandas as pd
import VerificadorRegras as verificador

def realizarAnaliseSintatica(tabelaDeTokens):
    listaDeTokens = (tabelaDeTokens[tabelaDeTokens.columns[0:1:]]).values
    listaDeLexemas = (tabelaDeTokens[tabelaDeTokens.columns[1:2:]]).values
    listaDeNumeroLinha = (tabelaDeTokens[tabelaDeTokens.columns[2:3:]]).values

    verificador.verificarBalanceamentoChaveEParentese(listaDeTokens)
    
    return "Tabela de simbolos"
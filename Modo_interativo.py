# Douglas Pereira Borges, 566889
# João Lucas Magalhães de Almeida, 581608
# Sarah Ingrid Fernandes Alves, 554703

import sys

#/////////modo interativo e suas funções////////////
#/////////modo interativo e suas funções////////////

def LerArqPistas(NomeArquivo):
    Grade = [[0 for _ in range(9)] for _ in range(9)]
    Pistas = [[False for _ in range(9)] for _ in range(9)]

    Letras = "ABCDEFGHI"
    ColunasDict = {}
    I = 0
    while I < 9:
        ColunasDict[Letras[I]] = I
        I = I + 1

    Arquivo = open(NomeArquivo, "r")
    Linhas = Arquivo.readlines()
    Arquivo.close()

    TotalPistas = 0
    Indice = 0
    while Indice < len(Linhas):
        LinhaOriginal = Linhas[Indice]
        LinhaLimpa = LinhaOriginal.strip()
        Indice = Indice + 1

        if len(LinhaLimpa) > 0:
            Partes = LinhaLimpa.split(":")
            if len(Partes) != 2:
                print("Formato inválido: " + LinhaLimpa)
                return "ERRO"

            Lado = Partes[0].strip()
            NumeroStr = Partes[1].strip()

            if NumeroStr.isdigit() == False:
                print("Número inválido: " + NumeroStr)
                return "ERRO"

            Numero = int(NumeroStr)
            if Numero < 1 or Numero > 9:
                print("O número: " + NumeroStr + "deveria ser de 1 a 9.")
                return "ERRO"

            LadoPartes = Lado.split(",")
            if len(LadoPartes) != 2:
                print("Formato inválido: " + LinhaLimpa)
                return "ERRO"

            ColLetra = LadoPartes[0].strip().upper()
            LinStr = LadoPartes[1].strip()

            if LinStr.isdigit() == False:
                print("Linha inválida: " + LinStr)
                return "ERRO"

            Linha = int(LinStr) - 1
            if ColLetra in ColunasDict:
                Coluna = ColunasDict[ColLetra]
            else:
                print("Coluna inválida: " + ColLetra)
                return "ERRO"

            if Linha < 0 or Linha >= 9:
                print("A linha: " + str(Linha + 1) + "deveria ser de 1 a 9.")
                return "ERRO"

            ValorExistente = Grade[Linha][Coluna]
            if ValorExistente == 0:
                Grade[Linha][Coluna] = Numero
                Pistas[Linha][Coluna] = True
                TotalPistas = TotalPistas + 1
            elif ValorExistente != Numero:
                print("Pista conflitante na célula (" + ColLetra + "," + str(Linha + 1) + ")")
                return "ERRO"

    if TotalPistas < 1 or TotalPistas > 80:
        print("Número de pistas inválido: " + str(TotalPistas) + "(Deve ser de 1 a 80 no máximo).")
        return "ERRO"

    I = 0
    while I < 9:
        J = 0
        while J < 9:
            Valor = Grade[I][J]
            if Valor != 0:
                Grade[I][J] = 0
                Resultado = ValidaJogada(Grade, I, J, Valor)
                if Resultado == False:
                    print("Pista inválida na posição (" + str(I+1) + "," + str(J+1) + ") fere as regras básicas do Sudoku.")
                    return "ERRO"
                Grade[I][J] = Valor
            J = J + 1
        I = I + 1

    return [Grade, Pistas]

#///////////divisão de função aqui/////////////
#///////////divisão de função aqui/////////////

def MostrarGrade(Grade, Pistas):
    Red = '\033[91m'
    Reset = '\033[0m'

    def LinhaHorizontal(Tipo):
        if Tipo == 'grossa':
            return " ++===+===+===++===+===+===++===+===+===++"
        return " ++---+---+---++---+---+---++---+---+---++"

    print("    A   B   C    D   E   F    G   H   I")

    Lin = 0
    while Lin < 9:
        if Lin % 3 == 0:
            print(LinhaHorizontal('grossa'))
        else:
            print(LinhaHorizontal('fina'))

        LinhaStr = str(Lin + 1) + "||"
        Col = 0
        while Col < 9:
            Valor = Grade[Lin][Col]
            if (Col + 1) % 3 != 0:
                Sep = "|"
            else:
                Sep = "||"
            if Valor == 0:
                LinhaStr = LinhaStr + "   " + Sep
            else:
                if Pistas[Lin][Col] == True:
                    LinhaStr = LinhaStr + Red + " " + str(Valor) + " " + Reset + Sep
                else:
                    LinhaStr = LinhaStr + " " + str(Valor) + " " + Sep
            Col = Col + 1
        print(LinhaStr + str(Lin + 1))
        Lin = Lin + 1

    print(LinhaHorizontal('grossa'))
    print("    A   B   C    D   E   F    G   H   I")

#///////////divisão de função aqui/////////////
#///////////divisão de função aqui/////////////

def EntradaJogada():
    Letras = "ABCDEFGHI"
    ColunasDict = {}
    I = 0
    while I < 9:
        ColunasDict[Letras[I]] = I
        I = I + 1

    Entrada = input("Digite a jogada: ").strip()
    if len(Entrada) == 0:
        return ["ERRO", "Você não deu uma entrada ainda"]

    Partes = Entrada.split(":")
    if len(Partes) != 2:
        return ["ERRO", "Formato inválido para jogada (esperado: C,3: 7)"]

    Lado = Partes[0].strip()
    NumeroStr = Partes[1].strip()

    PartesLado = Lado.split(",")
    if len(PartesLado) != 2:
        return ["ERRO", "Formato inválido da posição (esperado: C,3)"]

    ColLetra = PartesLado[0].strip().upper()
    LinStr = PartesLado[1].strip()

    if ColLetra in ColunasDict and LinStr.isdigit() and NumeroStr.isdigit():
        Coluna = ColunasDict[ColLetra]
        Linha = int(LinStr) - 1
        Numero = int(NumeroStr)
        if Linha >= 0 and Linha < 9 and Numero >= 1 and Numero <= 9:
            return ["JOGADA", Linha, Coluna, Numero]
        else:
            return ["ERRO", "Linha ou número fora do intervalo (1–9)"]
    else:
        return ["ERRO", "Coluna inválida ou dados não numéricos"]

#///////////divisão de função aqui/////////////
#///////////divisão de função aqui/////////////

def ValidaJogada(Grade, Linha, Coluna, Numero):
    I = 0
    while I < 9:
        if Grade[Linha][I] == Numero:
            return False
        if Grade[I][Coluna] == Numero:
            return False
        I = I + 1

    InicioLinha = (Linha // 3) * 3
    InicioColuna = (Coluna // 3) * 3

    I = 0
    while I < 3:
        J = 0
        while J < 3:
            if Grade[InicioLinha + I][InicioColuna + J] == Numero:
                return False
            J = J + 1
        I = I + 1

    return True

#///////////divisão de função aqui/////////////
#///////////divisão de função aqui/////////////

def ExecutarComandoInterativo(Grade, Pistas):
    print("Modo Interativo rodando.")
    JogoAtivo = True

    while JogoAtivo == True:
        MostrarGrade(Grade, Pistas)
        Entrada = EntradaJogada()

        if Entrada[0] == "ERRO":
            print("Erro: " + Entrada[1])
        else:
            Linha = Entrada[1]
            Coluna = Entrada[2]
            Numero = Entrada[3]

            if Pistas[Linha][Coluna] == True:
                print("Essa posição é uma pista e não pode ser modificada.")
            elif Grade[Linha][Coluna] != 0:
                Resposta = input("Essa célula já foi preenchida. Deseja sobrescrever? (s/n): ").strip().lower()
                if Resposta == "s":
                    if ValidaJogada(Grade, Linha, Coluna, Numero):
                        Grade[Linha][Coluna] = Numero
                    else:
                        print("Jogada inválida: viola as regras do Sudoku.")
                else:
                    print("Jogada cancelada.")
            else:
                if ValidaJogada(Grade, Linha, Coluna, Numero):
                    Grade[Linha][Coluna] = Numero
                else:
                    print("Jogada inválida: viola as regras do Sudoku.")

            I = 0
            Completo = True
            while I < 9:
                J = 0
                while J < 9:
                    if Grade[I][J] == 0:
                        Completo = False
                    J = J + 1
                I = I + 1

            if Completo == True:
                print("Verificando se a solução está correta...")
                Valido = True
                I = 0
                while I < 9:
                    J = 0
                    while J < 9:
                        Valor = Grade[I][J]
                        Grade[I][J] = 0
                        if ValidaJogada(Grade, I, J, Valor) == False:
                            Valido = False
                        Grade[I][J] = Valor
                        J = J + 1
                    I = I + 1

                if Valido == True:
                    MostrarGrade(Grade, Pistas)
                    print("Parabéns! Você completou o Sudoku corretamente.")
                    JogoAtivo = False
                else:
                    print("A grade está completa, mas contém erros. Continue corrigindo.")

#////////usando os subprogramas////////////
#////////usando os subprogramas////////////

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 jogoSudoku.py nome_arquivo.txt")
    else:
        NomeArquivo = sys.argv[1]
        Resultado = LerArqPistas(NomeArquivo)

        if Resultado == "ERRO":
            print("Erro ao processar o arquivo de pistas.")
        else:
            Grade = Resultado[0]
            Pistas = Resultado[1]
            Modo = input("Qual modo deseja jogar?(interativo/solucionador): ").strip().upper()
            if Modo == "INTERATIVO":
                ExecutarComandoInterativo(Grade, Pistas)
            else:
                if Modo == "SOLUCIONADOR":
                    print("Modo SOLUCIONADOR ainda não implementado.")

# Douglas Pereira Borges, 566889
# João Lucas Magalhães de Almeida, 581608
# Sarah Ingrid Fernandes Alves, 554703


def ler_arquivo_pistas(nome_arquivo):
    grade = []
    pistas = []
    i = 0
    while i < 9:
        linha = []
        pista = []
        j = 0
        while j < 9:
            linha.append(0)
            pista.append(False)
            j = j + 1
        grade.append(linha)
        pistas.append(pista)
        i = i + 1

    letras = "ABCDEFGHI"
    colunas_dict = {}
    i = 0
    while i < 9:
        colunas_dict[letras[i]] = i
        i = i + 1

    arquivo = open(nome_arquivo, "r")
    linhas = arquivo.readlines()
    arquivo.close()

    total_pistas = 0
    indice = 0

    while indice < len(linhas):
        linha_original = linhas[indice]
        indice = indice + 1

        linha_limpa = linha_original.strip()
        tamanho = len(linha_limpa)
        if tamanho > 0:
            partes = linha_limpa.split(":")
            if len(partes) == 2:
                lado = partes[0].strip()
                numero_str = partes[1].strip()

                if numero_str.isdigit():
                    numero = int(numero_str)

                    if numero >= 1 and numero <= 9:
                        lado_partes = lado.split(",")

                        if len(lado_partes) == 2:
                            col_letra = lado_partes[0].strip().upper()
                            lin_str = lado_partes[1].strip()

                            if lin_str.isdigit():
                                linha = int(lin_str) - 1

                                if col_letra in colunas_dict:
                                    coluna = colunas_dict[col_letra]

                                    if linha >= 0 and linha < 9:
                                        valor_existente = grade[linha][coluna]

                                        if valor_existente == 0:
                                            grade[linha][coluna] = numero
                                            pistas[linha][coluna] = True
                                            total_pistas = total_pistas + 1
                                        elif valor_existente != numero:
                                            print("Pista conflitante na célula (" + col_letra + "," + str(linha + 1) + ")")
                                            return "ERRO"
                                    else:
                                        print("Linha fora do intervalo (1-9): " + str(linha + 1))
                                        return "ERRO"
                                else:
                                    print("Coluna inválida: " + col_letra)
                                    return "ERRO"
                            else:
                                print("Linha inválida: " + lin_str)
                                return "ERRO"
                        else:
                            print("Formato inválido: " + linha_limpa)
                            return "ERRO"
                    else:
                        print("Número fora do intervalo (1-9): " + numero_str)
                        return "ERRO"
                else:
                    print("Número inválido: " + numero_str)
                    return "ERRO"
            else:
                print("Formato inválido: " + linha_limpa)
                return "ERRO"

    if total_pistas < 1 or total_pistas > 80:
        print("Número de pistas inválido: " + str(total_pistas))
        return "ERRO"

    i = 0
    while i < 9:
        j = 0
        while j < 9:
            valor = grade[i][j]
            if valor != 0:
                grade[i][j] = 0
                resultado = valida_jogada(grade, pistas, i, j, valor)
                if resultado == False:
                    print("Pista inválida na posição (" + str(i+1) + "," + str(j+1) + ") fere as regras do Sudoku.")
                    return "ERRO"
                grade[i][j] = valor
            j = j + 1
        i = i + 1

    return [grade, pistas]

#/////////////////////divisçao de funçoes aqui///////////////////////////
#/////////////////////divisçao de funçoes aqui///////////////////////////

def mostrar_grade(grade, pistas):
    RED = '\033[91m'
    RESET = '\033[0m'

    def linha_horizontal(tipo):
        if tipo == 'fina':
            return " ++---+---+---++---+---+---++---+---+---++"
        elif tipo == 'grossa':
            return " ++===+===+===++===+===+===++===+===+===++"

    print("    A   B   C    D   E   F    G   H   I")

    for lin in range(9):
        if lin % 3 == 0:
            print(linha_horizontal('grossa'))
        else:
            print(linha_horizontal('fina'))

        linha = f"{lin+1}||"
        for col in range(9):
            val = grade[lin][col]
            sep = "|" if (col + 1) % 3 != 0 else "||"

            if val == 0:
                linha += "   " + sep
            else:
                if pistas[lin][col]:
                    linha += RED + f" {val} " + RESET + sep
                else:
                    linha += f" {val} " + sep

        print(linha + f"{lin+1}")

    print(linha_horizontal('grossa'))
    print("    A   B   C    D   E   F    G   H   I")



#/////////////////////divisçao de funçoes aqui///////////////////////////
#/////////////////////divisçao de funçoes aqui///////////////////////////

def entrada_jogada():
    letras = "ABCDEFGHI"
    colunas_dict = {}
    i = 0
    while i < 9:
        colunas_dict[letras[i]] = i
        i = i + 1

    entrada = input("Digite a jogada:").strip()

    tamanho = len(entrada)
    if tamanho == 0:
        return ["ERRO", "Entrada vazia"]

    primeiro = entrada[0]
    if primeiro == "?":
        comando = "CONSULTA"
        resto = entrada[1:]
    elif primeiro == "!":
        comando = "APAGAR"
        resto = entrada[1:]
    else:
        comando = "JOGADA"
        resto = entrada

    partes = resto.split(":")
    if comando == "JOGADA":
        if len(partes) != 2:
            return ["ERRO", "Formato inválido para jogada"]

        lado = partes[0].strip()
        numero_str = partes[1].strip()

        partes_lado = lado.split(",")
        if len(partes_lado) != 2:
            return ["ERRO", "Formato inválido da posição"]

        col_letra = partes_lado[0].strip().upper()
        lin_str = partes_lado[1].strip()

        if col_letra in colunas_dict and lin_str.isdigit() and numero_str.isdigit():
            coluna = colunas_dict[col_letra]
            linha = int(lin_str) - 1
            numero = int(numero_str)
            if linha >= 0 and linha < 9 and numero >= 1 and numero <= 9:
                return ["JOGADA", linha, coluna, numero]
            else:
                return ["ERRO", "Linha ou número fora do intervalo"]
        else:
            return ["ERRO", "Coluna inválida ou dados não numéricos"]

    else:
        partes_lado = resto.split(",")
        if len(partes_lado) != 2:
            return ["ERRO", "Formato inválido da posição"]

        col_letra = partes_lado[0].strip().upper()
        lin_str = partes_lado[1].strip()

        if col_letra in colunas_dict and lin_str.isdigit():
            coluna = colunas_dict[col_letra]
            linha = int(lin_str) - 1
            if linha >= 0 and linha < 9:
                if comando == "CONSULTA":
                    return ["CONSULTA", linha, coluna]
                elif comando == "APAGAR":
                    return ["APAGAR", linha, coluna]
        return ["ERRO", "Coluna ou linha inválida"]


#/////////////////////divisçao de funçoes aqui///////////////////////////
#/////////////////////divisçao de funçoes aqui///////////////////////////

def valida_jogada(grade, pistas, linha, coluna, numero):
    i = 0
    while i < 9:
        if grade[linha][i] == numero:
            return False
        i = i + 1
    i = 0

    while i < 9:
        if grade[i][coluna] == numero:
            return False
        i = i + 1
    inicio_linha = (linha // 3) * 3
    inicio_coluna = (coluna // 3) * 3

    i = 0
    while i < 3:
        j = 0
        while j < 3:
            atual = grade[inicio_linha + i][inicio_coluna + j]
            if atual == numero:
                return False
            j = j + 1
        i = i + 1

    return True


#/////////////////////divisçao de funçoes aqui///////////////////////////
#/////////////////////divisçao de funçoes aqui///////////////////////////

def executar_comando_interativo(grade, pistas):
    print("Modo Interativo iniciado.")
    jogo_ativo = True

    while jogo_ativo:
        mostrar_grade(grade, pistas)
        entrada = entrada_jogada()

        if entrada[0] == "ERRO":
            print("Erro: " + entrada[1])
        
        elif entrada[0] == "JOGADA":
            linha = entrada[1]
            coluna = entrada[2]
            numero = entrada[3]

            if pistas[linha][coluna] == True:
                print("Essa posição é uma pista e não pode ser modificada.")
            elif grade[linha][coluna] != 0:
                print("Essa célula já foi preenchida.")
                resposta = input("Deseja sobrescrever? (s/n): ").strip().lower()
                if resposta == "s":
                    if valida_jogada(grade, pistas, linha, coluna, numero):
                        grade[linha][coluna] = numero
                    else:
                        print("Jogada inválida: viola as regras do Sudoku.")
                else:
                    print("Jogada cancelada.")
            else:
                if valida_jogada(grade, pistas, linha, coluna, numero):
                    grade[linha][coluna] = numero
                else:
                    print("Jogada inválida: viola as regras do Sudoku.")

        elif entrada[0] == "CONSULTA":
            linha = entrada[1]
            coluna = entrada[2]

            if grade[linha][coluna] != 0:
                print("Célula já preenchida.")
            elif pistas[linha][coluna] == True:
                print("Essa célula é uma pista e não pode ser alterada.")
            else:
                print("Possibilidades para a célula:")
                possibilidades = []
                numero = 1
                while numero <= 9:
                    if valida_jogada(grade, pistas, linha, coluna, numero):
                        possibilidades.append(str(numero))
                    numero = numero + 1
                print(", ".join(possibilidades))

        elif entrada[0] == "APAGAR":
            linha = entrada[1]
            coluna = entrada[2]

            if pistas[linha][coluna] == True:
                print("Você não pode apagar uma pista.")
            elif grade[linha][coluna] == 0:
                print("A célula já está vazia.")
            else:
                grade[linha][coluna] = 0
                print("Célula apagada.")

        completo = True
        i = 0
        while i < 9:
            j = 0
            while j < 9:
                if grade[i][j] == 0:
                    completo = False
                j = j + 1
            i = i + 1

        if completo == True:
            print("Verificando se a solução está correta...")
            valido = True
            i = 0
            while i < 9:
                j = 0
                while j < 9:
                    valor = grade[i][j]
                    grade[i][j] = 0
                    if valida_jogada(grade, pistas, i, j, valor) == False:
                        valido = False
                    grade[i][j] = valor
                    j = j + 1
                i = i + 1
            if valido == True:
                mostrar_grade(grade, pistas)
                print("Parabéns! Você completou o Sudoku corretamente.")
                jogo_ativo = False
            else:
                print("A grade está completa, mas contém erros. Continue corrigindo.")


#//////////////////////Usando as funções acima/////////////////////////////////////
#//////////////////////Usando as funções acima/////////////////////////////////////

if __name__ == "__main__":
    nome_arquivo = "arq_01_cfg.txt"
    resultado = ler_arquivo_pistas(nome_arquivo)

    if resultado == "ERRO":
        print("Erro ao processar o arquivo de pistas.")
    else:
        grade, pistas = resultado

        while True:
            mostrar_grade(grade, pistas)
            comando = entrada_jogada()

            if comando[0] == "ERRO":
                print("Erro na entrada:", comando[1])

            elif comando[0] == "JOGADA":
                linha, coluna, numero = comando[1], comando[2], comando[3]
                if pistas[linha][coluna]:
                    print("Não pode alterar uma pista fixa.")
                elif valida_jogada(grade, pistas, linha, coluna, numero):
                    grade[linha][coluna] = numero
                else:
                    print("Jogada inválida pelas regras do Sudoku.")

            elif comando[0] == "APAGAR":
                linha, coluna = comando[1], comando[2]
                if pistas[linha][coluna]:
                    print("Não pode apagar uma pista fixa.")
                else:
                    grade[linha][coluna] = 0

            elif comando[0] == "CONSULTA":
                linha, coluna = comando[1], comando[2]
                valor = grade[linha][coluna]
                if valor == 0:
                    print(f"Célula {chr(ord('A')+coluna)},{linha+1} está vazia.")
                else:
                    print(f"Célula {chr(ord('A')+coluna)},{linha+1} contém: {valor}")

            else:
                print("Comando não listado.")



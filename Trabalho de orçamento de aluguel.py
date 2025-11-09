import csv  

# Função para validar entradas numéricas de acordo com opções válidas
def entrada_inteiro(mensagem, opcoes_validas):
    while True:
        try:
            valor = int(input(mensagem))
            if valor in opcoes_validas:
                return valor  # Retorna o valor se estiver nas opções válidas
            else:
                print(f"Opção inválida! Escolha entre {opcoes_validas}.")
        except ValueError:
            print("Entrada inválida! Digite apenas números.")

# Função para validar respostas 's' ou 'n' (sim ou não)
def entrada_sn(mensagem):
    while True:
        resposta = input(mensagem).lower()
        if resposta in ['s', 'n']:
            return resposta
        else:
            print("Opção inválida! Digite 's' para sim ou 'n' para não.")


def calcular_aluguel():
    # Saudação inicial e solicitação do nome do cliente
    print("=== BEM-VINDO AO SISTEMA DE ORÇAMENTO R.M ===\n")
    nome_cliente = input("Por favor, digite seu nome: ").strip()
    if nome_cliente:
        print(f"\nOlá, {nome_cliente}! Vamos iniciar o seu orçamento.\n")
    else:
        nome_cliente = "Cliente"
        print("\nOlá! Vamos iniciar o seu orçamento.\n")

    # Loop principal do sistema, permitindo novos orçamentos
    while True:
        # Escolha do tipo de locação
        print("Selecione o tipo de locação:")
        print("1 - Apartamento (R$ 700,00 / 1 quarto)")
        print("2 - Casa (R$ 900,00 / 1 quarto)")
        print("3 - Estúdio (R$ 1.200,00)")
        tipo = entrada_inteiro("Digite o número correspondente: ", [1, 2, 3])

        valor_base = 0  
        tipo_imovel = ""  

        # Define valores e tipo do imóvel baseado na escolha
        if tipo == 1:
            valor_base = 700
            tipo_imovel = "Apartamento"
        elif tipo == 2:
            valor_base = 900
            tipo_imovel = "Casa"
        elif tipo == 3:
            valor_base = 1200
            tipo_imovel = "Estúdio"

        # Seleção de quartos (exceto estúdio)
        if tipo != 3:
            print("\nQuantos quartos deseja?")
            print("1 - Um quarto (sem acréscimo)")
            print("2 - Dois quartos (acréscimo de R$ 200 para apartamento e R$ 250 para casa)")
            quartos = entrada_inteiro("Digite o número correspondente: ", [1, 2])
            if tipo == 1 and quartos == 2:
                valor_base += 200
            elif tipo == 2 and quartos == 2:
                valor_base += 250
        else:
            quartos = 1 

        # Escolha de vagas de garagem ou estacionamento
        if tipo in [1, 2]:
            print("\nDeseja incluir vaga de garagem? (acréscimo de R$ 300,00)")
            print("1 - Sim")
            print("2 - Não")
            vaga = entrada_inteiro("Digite o número correspondente: ", [1, 2])
            if vaga == 1:
                valor_base += 300
        else:
            # Opções de vagas para estúdio
            print("\nDeseja incluir vagas de estacionamento?")
            print("1 - 2 vagas (R$ 250,00)")
            print("2 - Mais vagas adicionais (R$ 250 + R$ 60 por vaga extra)")
            print("3 - Não deseja vagas")
            opcao_vagas = entrada_inteiro("Digite o número correspondente: ", [1, 2, 3])

            if opcao_vagas == 1:
                valor_base += 250
            elif opcao_vagas == 2:
            
                while True:
                    try:
                        vagas_extras = int(input("Quantas vagas adicionais além das 2 iniciais? "))
                        if vagas_extras >= 0:
                            valor_base += 250 + (vagas_extras * 60)
                            break
                        else:
                            print("Digite um número positivo.")
                    except ValueError:
                        print("Entrada inválida! Digite apenas números.")

        # Desconto caso não haja crianças (aplicável apenas a apartamentos)
        possui_criancas = entrada_sn("\nPossui crianças? (s/n): ")
        if tipo == 1 and possui_criancas == 'n':
            desconto = valor_base * 0.05
            valor_base -= desconto

        # Valor do contrato fixo e parcelamento
        valor_contrato = 2000
        parcelas_contrato = entrada_inteiro("\nDeseja parcelar o contrato em quantas vezes? (1 a 5): ", [1, 2, 3, 4, 5])
        valor_parcela_contrato = valor_contrato / parcelas_contrato

        # Exibe o resumo do orçamento
        print(f"\n=== RESUMO DO ORÇAMENTO PARA {nome_cliente.upper()} ===")
        print(f"Tipo de imóvel: {tipo_imovel}")
        print(f"Quantidade de quartos: {quartos}")
        print(f"Valor mensal do aluguel: R$ {valor_base:.2f}")
        print(f"Valor total do contrato: R$ {valor_contrato:.2f}")
        print(f"Parcelamento do contrato: {parcelas_contrato}x de R$ {valor_parcela_contrato:.2f}")

        # Pergunta se deseja gerar CSV com as parcelas do aluguel
        opcao_csv = entrada_sn("\nDeseja gerar o arquivo CSV com as 12 parcelas do aluguel? (s/n): ")
        if opcao_csv == 's':
            with open('orcamento_rm.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.writer(arquivo_csv)
                escritor.writerow(['Mês', 'Valor da Parcela (R$)'])
                for mes in range(1, 13):
                    escritor.writerow([f"{mes}º mês", f"{valor_base:.2f}"])
            print("\nArquivo 'orcamento_rm.csv' gerado com sucesso!")

        # Pergunta se deseja fazer um novo orçamento
        repetir = entrada_sn("\nDeseja realizar um novo orçamento? (s/n): ")
        if repetir == 'n':
            print(f"\nObrigado por utilizar o sistema de orçamento da R.M, {nome_cliente}! Até logo!")
            break


if __name__ == "__main__":
    calcular_aluguel()

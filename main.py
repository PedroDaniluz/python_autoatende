from functions import *

while True:
    limpar()
    print(" ╔════════════════ MENU ══════════════════╗")
    print(" ║ 1 - Iniciar Atendimento                ║")
    print(" ║ 2 - Consultar Histórico                ║")
    print(" ║ 0 - Sair                               ║")
    print(" ╚════════════════════════════════════════╝")
    opc = input("Escolha uma opçao: ")
    while not opc.isnumeric() or not 0 <= int(opc) <= 2:
        opc = input("Escolha uma opçao válida: ")

    match int(opc):
        case 0:
            limpar()
            break
        case 1:
            limpar()
            input("Olá, Sou HapBot uma inteligencia artificial feita para te ajudar nesse momento dificil!\nSeja "
                  "bem-vindo ao nosso hospital.\nVou te atender de forma rápida e eficiente.\nBasta responder algumas "
                  "perguntas simples. Vamos começar?\nAperte enter para prosseguirmos... ")

            while True:
                limpar()
                cpf = input("Primeiro, digite o seu CPF: ")
                # Validar entrada: CPF
                while len(cpf) != 11:
                    cpf = input("CPF inválido, por favor, insira apenas os números: ")

                limpar()
                nascimento = input("Agora digite a data do seu nascimento: ")
                # Validar entrada: Nascimento
                while not validador_data(nascimento):
                    nascimento = input("Data inválida, insira sua data de nascimento no formato dd/mm/aaaa ou "
                                       "ddmmaaaa: ")
                nascimento = nascimento.replace('/', '')

                data_dict = consultar_cpf(cpf, nascimento)
                if data_dict['Situação'] == 'OK':
                    break
                else:
                    input("Os dados inseridos são inválidos! Tente novamente...")

            limpar()
            sintomas = input("Quais são os seus sintomas? ")
            while len(sintomas) < 5:
                sintomas = input("Descreva os seus sintomas: ")

            limpar()
            duracao = input("Quanto tempo faz que você está passando por isso? ")
            while len(duracao) < 5:
                duracao = input("Descreva os seus sintomas: ")

            limpar()
            alergico = input("Você é alérgico a alguma medicação? Se sim, qual? ")

            limpar()
            medicacao = input("Está fazendo o uso de alguma medicação nesse momento? Se sim, qual? ")

            limpar()
            input("Pronto! Vou te encaminhar para a próxima etapa com os nossos profissionais! "
                  "Pressione qualquer tecla...")

            userdata = (f"Idade: {data_dict['Idade']}\nSexo: {data_dict['Sexo']}\nSintomas: {sintomas}\n"
                        f"Duração: {duracao}\n Alergias: {alergico}\n Medicamento em uso: {medicacao}")

            create_pdf([data_dict['Nome'], data_dict['CPF'], data_dict['Idade'], data_dict['Sexo'], sintomas, duracao,
                        alergico, medicacao, gpt_ask(userdata)])

            adicionar_usuario(data_dict['Nome'], data_dict['CPF'], data_dict['Idade'], data_dict['Sexo'], sintomas,
                              duracao, alergico, medicacao, gpt_ask(userdata))
        case 2:
            limpar()
            opt = input("Essa é uma função exclusiva de administradores! Deseja prosseguir? (S)im ou (N)ão? ")
            while opt.upper() not in ["SIM", "NAO", "NÃO", "S", "N"]:
                opt = input("Opção inválida. Deseja prosseguir? (S)im ou (N)ão? ")
            if opt.upper() in ["SIM", "S"]:
                senha = input("Digite sua senha: ")
                if senha == 'admin':
                    while True:
                        with open("usuarios.json", "r", encoding='utf-8') as file:
                            usuarios = json.load(file)
                        pesquisa = input("Digite o nome do paciente: ")
                        aux = False
                        i = 0
                        for i in range(len(usuarios)):
                            if pesquisa.upper() == usuarios[i]['Nome'].upper():
                                aux = True
                                break
                        if aux:
                            limpar()
                            input(f'Nome: {usuarios[i]['Nome']}\nCPF: {usuarios[i]['CPF']}\n'
                                  f'Idade: {usuarios[i]['Idade']}\nSexo: {usuarios[i]['Sexo']}\n'
                                  f'Sintomas: {usuarios[i]['Sintomas']}\nDuração: {usuarios[i]['Duração']}\n'
                                  f'Alergias: {usuarios[i]['Alergias']}\nMedicações: {usuarios[i]['Medicação']}\n'
                                  f'Suspeitas: {usuarios[i]['Suspeitas']}\n'
                                  f'Data de atendimento: {usuarios[i]['Data de atendimento']}\n'
                                  f'Horário de atendimento: {usuarios[i]['Horário de atendimento']}\n'
                                  f'Aperte qualquer tecla para prosseguir...')
                        else:
                            limpar()
                            voltar = input("Usuário não encontrado, deseja tentar novamente? (S)im ou (N)ão? ")
                            while voltar.upper() not in ["SIM", "NAO", "NÃO", "S", "N"]:
                                voltar = input("Opção inválida. Deseja prosseguir? (S)im ou (N)ão? ")
                            if voltar.upper() in ["N", "NAO", "NÃO"]:
                                break
            else:
                print("Senha incorreta. Voltando ao menu inicial.")
                break

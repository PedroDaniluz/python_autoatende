from functions import *

while True:
    clear()
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
            clear()
            break
        case 1:
            clear()
            input("Olá, Sou HapBot uma inteligencia artificial feita para te ajudar nesse momento dificil!\nSeja "
                  "bem-vindo ao nosso hospital.\nVou te atender de forma rápida e eficiente.\nBasta responder algumas "
                  "perguntas simples. Vamos começar?\nAperte enter para prosseguirmos... ")

            while True:
                clear()
                cpf = input("Primeiro, digite o seu CPF: ")
                # Validar entrada: CPF
                while len(cpf) != 11:
                    cpf = input("CPF inválido, por favor, insira apenas os números: ")

                clear()
                bday = input("Agora digite a data do seu nascimento: ")
                # Validar entrada: Nascimento
                while not date_validator(bday):
                    bday = input("Data inválida, insira sua data de nascimento no formato dd/mm/aaaa ou "
                                 "ddmmaaaa: ")

                # Verificar se o CPF e a data de nascimento constam na Receita Federal
                query_dict = cpf_query(cpf, bday)
                if query_dict['Situação'] == 'OK':
                    # Cria o objeto 'paciente' da classe 'Patient'
                    paciente = Patient(cpf=query_dict["CPF"], name=query_dict["Nome"], age=query_dict["Idade"],
                                       gender=query_dict["Sexo"])
                    break
                else:
                    input("Os dados inseridos são inválidos! Tente novamente...")

            # Começa a atribuir valores aos atributos padrões da Classe:

            clear()
            paciente.symp = input("Quais são os seus sintomas? ")
            while len(paciente.symp) < 5:
                paciente.symp = input("Descreva os seus sintomas: ")

            clear()
            paciente.duration = input("Quanto tempo faz que você está passando por isso? ")
            while len(paciente.duration) < 4:
                paciente.duration = input("Descreva os seus sintomas: ")

            clear()
            paciente.allergies = input("Você é alérgico a alguma medicação? Se sim, qual? ")

            clear()
            paciente.medication = input("Está fazendo o uso de alguma medicação nesse momento? Se sim, qual? ")

            clear()
            input("Pronto! Vou te encaminhar para a próxima etapa com os nossos profissionais! "
                  "Pressione qualquer tecla...")

            print("\nSalvando...")

            # Pesquisa e atribui as suspeitas ao paciente
            paciente.get_suspicion()

            # Adiciona o usuário ao arquivo JSON
            paciente.add_user_db()

            # Cria a ficha de usuário em PDF
            paciente.create_pdf()

        case 2:
            clear()
            opt = input("Essa é uma função exclusiva de administradores! Deseja prosseguir? (S)im ou (N)ão? ")
            while opt.upper() not in ["SIM", "NAO", "NÃO", "S", "N"]:
                opt = input("Opção inválida. Deseja prosseguir? (S)im ou (N)ão? ")
            if opt.upper() in ["SIM", "S"]:
                password = input("Digite sua senha ('N' para sair): ")
                while password != "admin" and password.upper() not in ["N", "NAO", "NÃO"]:
                    password = input("Senha incorreta! Tente novamente ('N' para sair): ")
                if password == "admin":
                    serch_user_db("aux/usuarios.json")
                            
from functions import *

limpar()
input("Olá, Sou HapBot uma inteligencia artificial feita para te ajudar nesse momento dificil!\nSeja bem-vindo ao "
      "nosso hospital.\nVou te atender de forma rápida e eficiente.\nBasta responder algumas perguntas simples. "
      "Vamos começar?\nAperte enter para prosseguirmos... ")


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
        nascimento = input("Data inválida, insira sua data de nascimento no formato dd/mm/aaaa ou ddmmaaaa: ")
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
input("Certo, agora vou te encaminhar para a próxima etapa com os nossos profissionais! Pressione qualquer tecla...")

userdata = (f"Idade: {data_dict['Idade']}\nSexo: {data_dict['Sexo']}\nSintomas: {sintomas}\n"
            f"Duração: {duracao}\n Alergias: {alergico}\n Medicamento em uso: {medicacao}")

create_pdf([data_dict['Nome'], data_dict['CPF'], data_dict['Idade'], data_dict['Sexo'], sintomas, duracao, alergico,
            medicacao, gpt_ask(userdata)])

adicionar_usuario(data_dict['Nome'], data_dict['CPF'], data_dict['Idade'], data_dict['Sexo'], sintomas, duracao,
                  alergico, medicacao, gpt_ask(userdata))

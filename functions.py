import os
import dotenv
import requests
import json
from datetime import datetime, date
from openai import OpenAI
from reportlab.pdfgen import canvas
from pypdf import PdfWriter, PdfReader

dotenv.load_dotenv()


def limpar() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def formatar_sexo(sexo: str) -> str:
    if sexo.upper() == "M":
        return "Masculino"
    else:
        return "Feminino"


def formatar_nome(nome: str) -> str:
    # Captalizar as partes do nome
    nome_split = nome.split(" ")
    for i in range(len(nome_split)):
        nome_split[i] = nome_split[i].capitalize()
    return " ".join(nome_split)


def validador_data(data: str) -> bool:
    # Validar a data inserida
    if len(data) == 8 and len(data.split("/")) == 1:
        data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
    data_split = data.split("/")
    ano = datetime.now().year
    if len(data_split) != 3:
        return False
    else:
        if not data_split[0].isnumeric() or len(data_split[0]) != 2 or not 1 <= int(data_split[0]) <= 31:
            return False
        elif not data_split[1].isnumeric() or len(data_split[1]) != 2 or not 1 <= int(data_split[1]) <= 12:
            return False
        elif not data_split[2].isnumeric() or len(data_split[2]) != 4 or not ano - 150 <= int(data_split[2]) <= ano:
            return False
        else:
            aux = True
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                aux = False
            return aux


def calcular_idade(nasc: str):
    if len(nasc) == 8 and len(nasc.split("/")) == 1:
        nasc = f"{nasc[:2]}/{nasc[2:4]}/{nasc[4:]}"
    dia, mes, ano = nasc.split('/')[0], nasc.split('/')[1], nasc.split('/')[2]
    nasc = date(day=int(dia), month= int(mes), year=int(ano))
    data_atual = date.today()
    idade = data_atual.year - nasc.year - ((data_atual.month, data_atual.day) < (nasc.month, nasc.day))
 
    return idade


def consultar_cpf(cpf: str, nasc: str) -> dict:
    if len(nasc) == 8 and len(nasc.split("/")) == 1:
        nasc = f"{nasc[:2]}/{nasc[2:4]}/{nasc[4:]}"
    # Consultar CPF e data de nascimento com a API da receita federal
    print("\nBuscando...")
    token = os.getenv("CPF_API_KEY2")
    url = "http://ws.hubdodesenvolvedor.com.br/v2/cpf/"
    params = {
    "cpf": f"{cpf}",
    "data": f"{nasc}",
    "token": token
}

    response = requests.get(url, params=params)

    data = response.json()
    if data['return'] == 'OK':
        return {
            'Situação': 'OK',
            'Nome': formatar_nome(data['result']['nome_da_pf']),
            'CPF': f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
            'Idade': calcular_idade(data['result']['data_nascimento'])
        }
    else:
        print(f"Erro encontrado: {data['message']}")
        return {
            'Situação': 'ERRO',
        }


def gpt_ask(pergunta: str) -> str:
    # Mandar o request para o chatGPT
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    resposta = client.chat.completions.create(model="gpt-3.5-turbo",
                                              temperature=0.7,
                                              messages=[
                                                  {
                                                      "role": "system",
                                                      "content": "Você é um assistente virtual de um hospital, você "
                                                                 "receberá a idade, o sexo, os sintomas, a duração "
                                                                 "desses sintomas, as alergias e os medicamentos em uso"
                                                                 " do paciente. Com base nisso, deve retornar apenas "
                                                                 "uma string com as possiveis doenças separadas por "
                                                                 "espaço e vírgula, sem avisos, nem introdução. Nem "
                                                                 "titulo, apenas as três doenças captalizadas. Em PTBR"
                                                                 "Por exemplo:"
                                                                 "user: Dor de cabeça, dor nos olhos"
                                                                 "return: Enxaqueca, Sinusite, Cansaço"
                                                  },
                                                  {
                                                      "role": "user",
                                                      "content": pergunta
                                                  }
                                              ])
    return resposta.choices[0].message.content


def create_pdf(lista):
    informa = {
        "Nome Completo": lista[0],
        "CPF": lista[1],
        "Idade": lista[2],
        "Sexo": lista[3],
        "Sintomas": lista[4],
        "Duração": lista[5],
        "Alergia": lista[6],
        "Medicação em uso": lista[7],
        "Suspeitas": lista[8],
        "Data de atendimento": datetime.now().date(),
        "Horário de atendimento": f"{datetime.now().time()}".split(".")[0]
    }
    pdf = canvas.Canvas(f"Paciente - {lista[0]}.pdf")
    contlinhas = 0
    # Escrevendo primeiro pdf:
    for element in informa:
        pdf.drawString(100, 700 - contlinhas, f"{element}: {informa[element]}")
        contlinhas += 20
    pdf.save()
    # trabalhando com segundo pdf:
    stamp = PdfReader("template.pdf").pages[0]
    writer = PdfWriter(clone_from=f"Paciente - {lista[0]}.pdf")
    for page in writer.pages:
        page.merge_page(stamp, over=False)
    writer.write(f"Paciente - {lista[0]}.pdf")
    print("Ficha PDF gerada com sucesso.")


def adicionar_usuario(nome, cpf, idade, sexo, sintomas, duracao, alergias, medicacao, suspeitas):
    # Carregar dados existentes do arquivo JSON
    with open('usuarios.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    # Adicionar novo usuário
    novo_usuario = {
        'Nome': nome,
        'CPF': cpf,
        'Idade': idade,
        'Sexo': sexo,
        'Sintomas': sintomas,
        'Duração': duracao,
        'Alergias': alergias,
        'Medicação': medicacao,
        'Suspeitas': suspeitas,
        "Data de atendimento": f"{datetime.now().date()}",
        "Horário de atendimento": f"{datetime.now().time()}".split(".")[0]
    }

    dados.append(novo_usuario)

    # Salvar dados atualizados de volta ao arquivo JSON
    with open('usuarios.json', 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)


def buscar_usuario(doc: str) -> None:
    # Procura o usuário a partir do seu CPF no arquivo JSON
    while True:
        with open(doc, "r", encoding='utf-8') as file:
            usuarios = json.load(file)
        pesquisa = input("Digite o CPF do paciente: ")
        while len(pesquisa) != 11:
                    pesquisa = input("CPF inválido, por favor, insira apenas os números: ")
        aux = False
        ind = 0
        pesquisa = f"{pesquisa[:3]}.{pesquisa[3:6]}.{pesquisa[6:9]}-{pesquisa[9:]}"
        for i in range(len(usuarios)):
            if pesquisa == usuarios[i]["CPF"]:
                aux = True
                ind = i
        if aux:
            limpar()
            input(f'Nome: {usuarios[ind]["Nome"]}\nCPF: {usuarios[ind]["CPF"]}\n'
                    f'Idade: {usuarios[ind]["Idade"]}\nSexo: {usuarios[ind]["Sexo"]}\n'
                    f'Sintomas: {usuarios[ind]["Sintomas"]}\nDuração: {usuarios[ind]["Duração"]}\n'
                    f'Alergias: {usuarios[ind]["Alergias"]}\nMedicações: {usuarios[ind]["Medicação"]}\n'
                    f'Suspeitas: {usuarios[ind]["Suspeitas"]}\n'
                    f'Data de atendimento: {usuarios[ind]["Data de atendimento"]}\n'
                    f'Horário de atendimento: {usuarios[ind]["Horário de atendimento"]}\n'
                    f'Aperte qualquer tecla para prosseguir...')
            break
        else:
            limpar()
            voltar = input("Usuário não encontrado, deseja tentar novamente? (S)im ou (N)ão? ")
            while voltar.upper() not in ["SIM", "NAO", "NÃO", "S", "N"]:
                voltar = input("Opção inválida. Deseja prosseguir? (S)im ou (N)ão? ")
            if voltar.upper() in ["N", "NAO", "NÃO"]:
                break

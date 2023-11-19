import os
import dotenv
import requests
import json
from datetime import datetime
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
    nome_split = nome.split(" ")
    for i in range(len(nome_split)):
        nome_split[i] = nome_split[i].capitalize()
    return " ".join(nome_split)


def consultar_cpf(cpf: str, nasc: str) -> dict:
    print("\nBuscando...")
    token = os.getenv("CPF_API_KEY")
    url = "https://www.sintegraws.com.br/api/v1/execute-api.php"
    querystring = {"token": token, "cpf": f"{cpf}", "data-nascimento": f"{nasc}", "plugin": "CPF"}

    response = requests.request("GET", url, params=querystring)

    data = response.json()
    if data['code'] == '0':
        return {
            'Situação': 'OK',
            'Nome': formatar_nome(data['nome']),
            'Sexo': formatar_sexo(data['genero']),
            'CPF': data['cpf'],
            'Idade': data['idade']
        }
    else:
        return {
            'Situação': 'ERRO',
        }


def validador_data(data: str) -> bool:
    if len(data) == 8 and len(data.split("/")) == 1:
        data = f"{data[:2]}/{data[2:4]}/{data[4:]}"
    data_split = data.split("/")
    ano = datetime.now().year
    if len(data_split) != 3:
        print(data)
        print(data_split)
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


def gpt_ask(pergunta: str) -> str:
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
                                                                 "titulo, apenas as três doenças captalizadas"
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

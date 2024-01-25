import os
import dotenv
import requests
import json
from datetime import datetime
from openai import OpenAI
from reportlab.pdfgen import canvas
from pypdf import PdfWriter, PdfReader

dotenv.load_dotenv()


def clear() -> None:
    # Limpar script
    os.system('cls' if os.name == 'nt' else 'clear')


def name_format(name: str) -> str:
    # Captalizar as partes do nome
    nome_split = name.split(" ")
    for i in range(len(nome_split)):
        nome_split[i] = nome_split[i].capitalize()
    return " ".join(nome_split)


def gender_format(gender: str) -> str:
    # Formatar gênero
    if gender.upper() == "M":
        return "Masculino"
    else:
        return "Feminino"


def date_validator(date: str) -> bool:
    # Validar a data inserida, tentando evitar exceptions
    if len(date) == 8 and len(date.split("/")) == 1:
        date = f"{date[:2]}/{date[2:4]}/{date[4:]}"
    date_split = date.split("/")
    ano = datetime.now().year
    if len(date_split) != 3:
        return False
    else:
        if not date_split[0].isnumeric() or len(date_split[0]) != 2 or not 1 <= int(date_split[0]) <= 31:
            return False
        elif not date_split[1].isnumeric() or len(date_split[1]) != 2 or not 1 <= int(date_split[1]) <= 12:
            return False
        elif not date_split[2].isnumeric() or len(date_split[2]) != 4 or not ano - 150 <= int(date_split[2]) <= ano:
            return False
        else:
            aux = True
            try:
                datetime.strptime(date, "%d/%m/%Y")
            except ValueError:
                aux = False
            return aux


def cpf_query(cpf: str, bday: str) -> dict:
    if len(bday) != 8 and len(bday.split("/")) == 3:
        bday = f"{bday[:2]}{bday[3:5]}{bday[6:]}"
    # Consultar CPF e data de nascimento com a API da receita federal
    print("\nBuscando...")
    token = os.getenv("CPF_API_KEY")
    url = "https://www.sintegraws.com.br/api/v1/execute-api.php"
    querystring = {"token": f"{token}", "cpf": cpf, "data-nascimento": f"{bday}", "plugin": "CPF"}

    response = requests.request("GET", url, params=querystring)

    data = response.json()
    if data['code'] == '0':
        return {
            'Situação': 'OK',
            'Nome': name_format(data['nome']),
            'CPF': f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}",
            'Idade': data['idade'],
            'Sexo': gender_format(data['genero'])
        }
    else:
        print(f"Erro encontrado: {data['message']}")
        return {
            'Situação': 'ERRO',
        }


class Patient:
    # Paciente só é criado após confirmar validade do CPF
    # Criando um objeto Patient com valores padrões que são alterados ao longo do código
    def __init__(self, cpf, name, age, gender, symp="", duration="", allergies="", medication="", suspicion="") -> None:
        self.cpf: str = cpf
        self.name: str = name
        self.age: int = age
        self.gender: str = gender
        self.symp: str = symp
        self.duration: str = duration
        self.allergies: str = allergies
        self.medication: str = medication
        self.suspicion: str = suspicion
        self.date: str = f"{datetime.now().date()}"
        self.time: str = f"{datetime.now().time()}".split(".")[0]

    def get_suspicion(self):
        # Mandar o request para o chatGPT
        # Armazena as suspeitas no atributo 'suspicion' do objeto declarado da classe Patient
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        resposta = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  temperature=0.7,
                                                  messages=[
                                                      {
                                                          "role": "system",
                                                          "content": "Você é um assistente virtual de um hospital, "
                                                                     "você receberá a idade, o sexo, os sintomas, a "
                                                                     "duração desses sintomas, as alergias e os "
                                                                     "medicamentos em uso do paciente. Com base nisso, "
                                                                     "deve retornar apenas uma string com as possiveis "
                                                                     "doenças separadas por espaço e vírgula, sem "
                                                                     "avisos, nem introdução. Nem titulo, apenas as "
                                                                     "três doenças captalizadas. Em PTBR\n"
                                                                     "Por exemplo:\n"
                                                                     "user: Dor de cabeça, dor nos olhos\n"
                                                                     "return: Enxaqueca, Sinusite, Cansaço"
                                                      },
                                                      {
                                                          "role": "user",
                                                          "content": f"Idade: {self.age}\nSexo: {self.gender}\n"
                                                                     f"Sintomas: {self.symp}\nDuração: "
                                                                     f"{self.duration}\n Alergias: {self.allergies}\n "
                                                                     f"Medicamento em uso: {self.medication}"
                                                      }
                                                  ])
        self.suspicion = resposta.choices[0].message.content

    def add_user_db(self):
        # Carregar dados existentes do arquivo JSON
        with open('aux/usuarios.json', 'r', encoding='utf-8') as arquivo:
            data = json.load(arquivo)
        # Adicionar novo usuário
        new_user = {
            'Nome': self.name,
            'CPF': self.cpf,
            'Idade': self.age,
            'Sexo': self.gender,
            'Sintomas': self.symp,
            'Duração': self.duration,
            'Alergias': self.allergies,
            'Medicação': self.medication,
            'Suspeitas': self.suspicion,
            "Data de atendimento": self.date,
            "Horário de atendimento": self.time
        }

        data.append(new_user)

        # Salvar dados atualizados de volta ao arquivo JSON
        with open('aux/usuarios.json', 'w', encoding='utf-8') as arquivo:
            json.dump(data, arquivo, indent=4, ensure_ascii=False)

    def create_pdf(self):
        info = {
            "Nome Completo": self.name,
            "CPF": self.cpf,
            "Idade": self.age,
            "Sexo": self.gender,
            "Sintomas": self.symp,
            "Duração": self.duration,
            "Alergia": self.allergies,
            "Medicação em uso": self.medication,
            "Suspeitas": self.suspicion,
            "Data de atendimento": self.date,
            "Horário de atendimento": self.time
        }
        pdf = canvas.Canvas(f"Paciente - {self.name}.pdf")
        countlines = 0
        # Escrevendo primeiro pdf:
        for element in info:
            pdf.drawString(100, 700 - countlines, f"{element}: {info[element]}")
            countlines += 20
        pdf.save()
        # Trabalhando com segundo pdf:
        stamp = PdfReader("aux/template.pdf").pages[0]
        writer = PdfWriter(clone_from=f"Paciente - {self.name}.pdf")
        for page in writer.pages:
            page.merge_page(stamp, over=False)
        writer.write(f"Paciente - {self.name}.pdf")
        print("Ficha PDF gerada com sucesso.")


def serch_user_db(doc: str) -> None:
    # Procura o usuário a partir do seu CPF no arquivo JSON
    while True:
        with open(doc, "r", encoding='utf-8') as file:
            users_list = json.load(file)
        cpf_search = input("Digite o CPF do paciente: ")
        while len(cpf_search) != 11:
            cpf_search = input("CPF inválido, por favor, insira apenas os números: ")
        found = False
        index = 0
        cpf_search = f"{cpf_search[:3]}.{cpf_search[3:6]}.{cpf_search[6:9]}-{cpf_search[9:]}"
        for i in range(len(users_list)):
            if cpf_search == users_list[i]["CPF"]:
                found = True
                index = i
        if found:
            clear()
            input(f'Nome: {users_list[index]["Nome"]}\nCPF: {users_list[index]["CPF"]}\n'
                  f'Idade: {users_list[index]["Idade"]}\nSexo: {users_list[index]["Sexo"]}\n'
                  f'Sintomas: {users_list[index]["Sintomas"]}\nDuração: {users_list[index]["Duração"]}\n'
                  f'Alergias: {users_list[index]["Alergias"]}\nMedicações: {users_list[index]["Medicação"]}\n'
                  f'Suspeitas: {users_list[index]["Suspeitas"]}\n'
                  f'Data de atendimento: {users_list[index]["Data de atendimento"]}\n'
                  f'Horário de atendimento: {users_list[index]["Horário de atendimento"]}\n'
                  f'Aperte qualquer tecla para prosseguir...')
            break
        else:
            clear()
            go_back = input("Usuário não encontrado, deseja tentar novamente? (S)im ou (N)ão? ")
            while go_back.upper() not in ["SIM", "NAO", "NÃO", "S", "N"]:
                go_back = input("Opção inválida. Deseja prosseguir? (S)im ou (N)ão? ")
            if go_back.upper() in ["N", "NAO", "NÃO"]:
                break

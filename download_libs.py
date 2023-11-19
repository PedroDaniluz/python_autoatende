import os

'''
COMO RODAR O PROGRAMA?

*MacOS ou Linux:
-- Navegue até o diretório do programa
-- Digite no terminal os seguintes comandos:
    python3 -m venv venv
    source venv/bin/activate
    python3 download_libs.py
    python3 main.py
 
*Windows:
-- Navegue até o diretório do programa
-- digite no terminal os seguintes comandos:
    python -m venv venv
    venv\\Scripts\\activate
    python download_libs.py
    python main.py
'''
 
pacotes = ['requests', 'datetime', 'python-dotenv', 'openai', 'reportlab', 'pypdf']

for a in pacotes:
    os.system(f"pip install {a}")

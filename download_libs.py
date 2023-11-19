import os

pacotes = ['requests', 'datetime', 'python-dotenv', 'openai', 'reportlab', 'pypdf']

for a in pacotes:
    os.system(f"pip install {a}")

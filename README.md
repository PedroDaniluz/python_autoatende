<h1 style="color: orange">HapBot</h1>

<p>
    O HapBot é um modelo de autoatendimento responsável por realizar o cadastro inicial<br>
    dos pacientes nos hospitais da rede hapvida. Ele será responsável por gerar a ficha do<br>
    paciente, adiantando uma parte da triagem, e consequentemente, agilizandoo atendimento<br>
    médico.
</p>

<h3 style="color: darkgreen">Como configurar o script?</h3>

<p>
    Encontre o diretório do script e digite os seguintes comandos:<br>
    Digite os comandos em ordem ~apenas uma vez para configurar.<br>
</p>

<h4 style="color: purple">MacOS e Linux:</h4>

<p style="color: aquamarine">
    $ python3 -m venv venv<br>
    $ source venv/bin/activate<br>
    $ python3 download_libs.py<br>
</p>

<h4 style="color: purple">Windows:</h4>

<p style="color: aquamarine">
    $ python -m venv venv<br>
    $ venv\\Scripts\\activate<br>
    $ python download_libs.py<br>
</p>

<h3 style="color: darkgreen">Como rodar o script?</h3>

<p>
    Após realizar as configurações iniciais:<br>
    Encontre o diretório do script e digite os seguintes comandos:<br>
</p>

<h4 style="color: purple">MacOS e Linux:</h4>

<p style="color: aquamarine">
    $ source venv/bin/activate<br>
    $ python3 main.py
</p>

<h4 style="color: purple">Windows:</h4>

<p style="color: aquamarine">
    $ venv\\Scripts\\activate<br>
    $ python main.py
</p>

<h3 style="color: orange">Como usar o programa?</h3>

<p>
    No menu inicial, escolha uma dos opções:<br><br>
    1. Ao iniciar o atendimento você deve inserir um CPF e uma data de nascimento<br>
    válidas; e responder algumas perguntas no terminal. Com isso, o programa irá<br>
    gerar uma ficha PDF com os seus dados e salvá-los no arquivo json.<br><br>
    2. Ao consultar os usuários você deve inserir a senha <b>'admin'</b>, para poder<br>
    pesquisar os dados de usuários no sistema, a partir do nome.
</p>
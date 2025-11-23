Como contribuir para o projeto:
------------
__Agradecemos__ a vontade de contribuir para o nosso projeto, mas mantenha as coisas organizadas.
 
1. **Abra uma issue**

    Antes de começar a alterar o projeto:
    * Verifique se não existe uma issue relacionada
    * Caso não exista, crie uma issue explicando detalhadamente as funcionalidades implementadas

2. **Crie Uma Branch**

    Após definir oque sera alterado:
    * Não altere diretamente a main do projeto

3. **Mantenha Seu Codigo limpo**

    Lembre-se, o codigo será lido por outras pessoas:
    * Mantenha uma organização estrutural no codigo com base nos codigos ja feitos.
    * Evite deixar prints de debugs no codigos
    * Faça os testes das suas funcionalidades
    * Caso haja dependencias, explique-as.

4. **Atualize a Documentação**

    Mantenha seu codigo explicado:
    * Atualize comentarios.
    * Ajuste o `README` caso necessario.
    * Mantenha outros colaboradores informados    

Como rodar o projeto localmente:
------------
1. Clone o repositorio do GitHub:
````bash
git clone https://github.com/guilhermeblacerda/Connect.git
````
2. Crie e entre na sua branch:
````bash
git checkout -b "nome da sua branch"
````

3. crie um ambiente virtual
````bash
python -m venv "nome_do_seu_ambiente_virtual"
````

4. Ative o seu ambiente virtual: 
````bash 
"nome_do_seu_ambiente_virtual"\Scripts\activate 
````

5. Abra a pasta do repositorio e baixe as dependencias do projeto:
````bash
cd Connect
pip install -r requirements.txt 
````
6. Rode localmente o projeto: 
````bash
py manage.py runserver
````
------------




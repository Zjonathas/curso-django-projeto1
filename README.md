# Projeto de um sites de receitas
Este projeto foi desenvolvido em conjunto com o curso de Django do Luiz Otávio Miranda.
Um site completo com várias funcionalidades como usuários, receitas, mecanismo de busca, dashboard e etc.

## Como usar
- 1 - Clone o repositório `git clone "https://github.com/Zjonathas/curso-django-projeto1.git"`
- 2 - Crie um ambiente virtual com `python -m venv venv`
- 3 - Instale as dependências `pip install -r requirements.txt`
- 4 - Copie e cole o arquivo .env-example e renomeio para .env
- 5 - Substitua as informações necessárias dentro do .env
- 6 - Utilize `python manage.py makemigrations` e `python manage.py migrate`
- 7 - Crie um superuser com `python manage.py createsuperuser`
- 8 - Rode o servidor com `python manage.py runserver`

  ## API
  ### URLs da API
  - Substitua example.com pelo domínio local, ou do seu servidor.
  - Listar Receitas: `http://example.com/recipes/api/v2/`
  - Detalhar Receita: `http://example.com/recipes/api/v2/id -> Subistitua o id por o id da receita desejada`
  - Criar Receita: `http://example.com/recipes/api/v2/ -> Use Método POST (OBS: É possível usar mulitpart)`
  - Atualizar Receita: `http://example.com/recipes/api/v2/id -> Use método PATCH e subistitua o id por o id da receita desejada`
  - Deletar Receita: `http://example.com/recipes/api/v2/id -> Use Método DELETE e subistitua o id por o id da receita desejada`

    ### JWT
    - Create: `http://example.com/recipes/api/token/ -> Envie um JSON com username e password do Usuário`
    - Refresh: `http://example.com/recipes/api/token/refresh/ -> Envie o refresh`
    - Verify: `http://example.com/recipes/api/token/verify/ -> Envie um JSON com token: access (access obtido no refresh)`
   
    ### Authors
    - Me: `http://example.com/authors/api/me/`

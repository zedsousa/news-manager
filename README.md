# 📰 news-manager

Sistema de gerenciamento de notícias.

---

## 🚀 Tecnologias

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- Dev Containers (VSCode)
- SimpleJWT
- drf-spectacular (Swagger/OpenAPI)

---

## ⚙️ Como rodar o projeto

### Configure o arquivo `.env`

Copie o arquivo `.env-example` para `.env`:

```bash
cp .env-example .env
```

### Configure uma nova SECRET_KEY

Gere uma nova chave secreta e atualize no arquivo `.env`:

```bash
# Gere uma nova chave usando Python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copie a chave gerada e substitua no arquivo .env:
SECRET_KEY=sua-chave-gerada-aqui
```


### ▶️ Usando Dev Containers (VSCode)

1. Instale as extensões:
   - [Dev Containers (Remote - Containers)](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. No VSCode, clique no canto inferior esquerdo em `><` e selecione:
   ```
   "Reopen in Container"
   ```
---

### ▶️ Usando Docker Compose

1. Suba os containers:
   ```bash
   docker-compose up --build
   ```

2. Acesse a API:
   ```
   http://localhost:8000/api/
   ```
---

## 👤 Criar superusuário

Após os containers estarem rodando:

```bash
python manage.py createsuperuser
```

Acesse o painel administrativo em:

```
http://localhost:8000/admin/
```

---

## 📚 Documentação da API

A documentação interativa dos endpoints está disponível em:

```
http://localhost:8000/api/docs/swagger/
```

---

## 🧪 Rodando os testes

Para rodar os testes localmente:

```bash
pytest
```

No GitHub Actions, os testes são executados automaticamente nos branches `main` e `develop`.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
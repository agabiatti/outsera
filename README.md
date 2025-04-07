# Outsera Teste

API REST, desenvolvida com FastAPI, SQLAlchemy e Pydantic.

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic v2](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [Pytest](https://docs.pytest.org/)

---

## 🛠️ Requisitos

- Python 3.11
    * *Pydantic-core (engine em Rust) pode falhar na instalação em Python 3.13. Recomendado manter a versão 3.11 por compatibilidade.*
- pip + conda ou venv

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/agabiatti/outsera.git
cd outsera
```

### 2. Crie um ambiente virtual

Caso seja necessário, crie um ambiente virtual para rodar o projeto.

Utilizando conda:

```bash
conda create -n outsera_test python=3.11
conda activate outsera_test
```

Utilizando venv:

(O python precisa estar na versão desejada, 3.11)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Rodando o Projeto

```bash
pip install -r requirements.txt

uvicorn app.main:app --reload
```

### 4. Carregando dados para o Banco

Para preencher o banco de dados após a aplicação estar rodando, utilize a rota:

```
POST /services/load_data

{
    "csv_path": "./app/services/movielist.csv"
}
```

### 5. Rodando testes

```
pytest tests/test_movie_controller.py -v
pytest tests/test_producer_controller.py -v
pytest tests/test_studio_controller.py -v
```

### 6. Acessando as Docs

```
http://127.0.0.1:8000/docs
```
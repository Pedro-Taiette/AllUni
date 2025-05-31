# AllUni

![AllUni Logo](https://img.shields.io/badge/AllUni-Your%20Academic%20Companion-blue)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/alluni)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/yourusername/alluni)
[![Docker](https://img.shields.io/docker/pulls/taiettedev/alluni)](https://hub.docker.com/r/taiettedev/alluni)

## 📚 Sobre

AllUni é uma aplicação web moderna para gerenciamento de anotações acadêmicas, projetada para funcionar como um "wrapper" para plataformas Moodle. Inspirado no Notion, o AllUni permite que estudantes organizem suas matérias e anotações de forma intuitiva e eficiente.

![AllUni Screenshot](https://via.placeholder.com/800x400?text=AllUni+Screenshot)

## ✨ Funcionalidades

- **Organização por Matérias**: Crie e gerencie suas matérias acadêmicas  
- **Anotações com Markdown**: Escreva anotações ricas usando Markdown  
- **Sistema de Favoritos**: Marque suas anotações mais importantes  
- **Arquivamento**: Arquive matérias que não está mais cursando  
- **Pesquisa Avançada**: Encontre rapidamente suas anotações e matérias  

## 🚀 Começando

### Pré-requisitos

- Python 3.10+  
- Pipenv
### Instalação

1. Clone o repositório:

2. Crie o ambiente virtual:
```bash
pip install pipenv
cd ./AllUni
```

3. Instale as dependências:
```bash
pipenv install
```

4. Ative o ambiente e execute as migrações:
```bash
pipenv shell
python manage.py makemigrations
python manage.py migrate
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

Acesse a aplicação em: [http://localhost:8000](http://localhost:8000)

## 🧪 Testes

Para executar os testes:
```bash
coverage run manage.py test
coverage html  # Gera relatório HTML de cobertura
```

## 🐳 Docker

Para facilitar a implantação, disponibilizamos uma imagem Docker:

```bash
# Baixar a imagem
docker pull taiettedev/alluni:latest

# Executar o contêiner
docker run -p 8000:8000 taiettedev/alluni:latest

# Com persistência de dados
docker run -p 8000:8000 -v alluni_data:/app/data taiettedev/alluni:latest
```

Link para a imagem Docker: [taiettedev/alluni](https://hub.docker.com/r/taiettedev/alluni)

## 🔧 Tecnologias

- **Backend**: Django, Python  
- **Frontend**: HTML, CSS (Tailwind), JavaScript  
- **Banco de Dados**: SQLite (desenvolvimento), PostgreSQL (produção)  
- **Containerização**: Docker  
- **CI/CD**: GitHub Actions  

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

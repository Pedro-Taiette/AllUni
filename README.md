# 🎓 AllUni — *Your Academic Companion*

![AllUni Logo](https://img.shields.io/badge/AllUni-Your%20Academic%20Companion-blue)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/alluni)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/yourusername/alluni)
[![Docker Pulls](https://img.shields.io/docker/pulls/taiettedev/alluni)](https://hub.docker.com/r/taiettedev/alluni)

---

## 📚 Sobre o Projeto

> **AllUni**
O AllUni é uma plataforma web desenvolvida para ajudar estudantes universitários a centralizar, organizar e personalizar suas anotações acadêmicas em um único lugar.
> Inspirado por ferramentas modernas como o Notion, o AllUni vai além ao oferecer integração com o Moodle, possibilitando que os usuários acompanhem conteúdos das disciplinas diretamente pela plataforma. 
> A proposta é simples: diminuir a bagunça digital enfrentada por muitos estudantes, trazendo uma interface limpa, intuitiva e funcional para o dia a dia universitário. A ideia surgiu da experiência pessoal do desenvolvedor, que sentia a necessidade de uma ferramenta leve, focada no contexto acadêmico, mas com a flexibilidade de um caderno digital moderno.

>🧩 Explore o protótipo do AllUni no Figma e veja como estamos transformando a experiência acadêmica!
> 👉 [Acesse aqui o protótipo](https://www.figma.com/design/Xk6q1uKUOMR6USaXgwrdWO/Untitled?node-id=0-1&t=U4gamE1kLr5FLI7E-1)
---

## ✨ Funcionalidades Principais

🗂️ **Organização por Matérias** — Crie, edite e arquive suas matérias facilmente  
📝 **Editor Markdown** — Escreva anotações ricas com formatação moderna  
⭐ **Sistema de Favoritos** — Destaque conteúdos importantes com um clique  
📦 **Arquivamento Inteligente** — Mantenha seu ambiente limpo com matérias arquivadas  
🔍 **Pesquisa Avançada** — Encontre tudo rapidamente com filtros poderosos  

---

## 🚀 Começando

### 🔧 Pré-requisitos

- ✅ Python 3.10+  
- ✅ Pipenv  

### ⚙️ Instalação Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/yourusername/alluni.git
   cd AllUni
   ```

2. Instale o `pipenv` (se ainda não tiver):
   ```bash
   pip install pipenv
   ```

3. Instale as dependências do projeto:
   ```bash
   pipenv install
   ```

4. Ative o ambiente virtual e aplique as migrações:
   ```bash
   pipenv shell
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

🖥️ Acesse a aplicação: [http://localhost:8000](http://localhost:8000)

---

## 🧪 Testes Automatizados

AllUni tem cobertura de testes **100% garantida** ✅

Execute os testes com:

```bash
coverage run manage.py test
coverage html  # Gera o relatório HTML de cobertura
```

---

## 🐳 Docker

Também oferecemos suporte completo via Docker:

```bash
# Baixar a imagem
docker pull taiettedev/alluni:latest

# Rodar o contêiner
docker run -p 8000:8000 taiettedev/alluni:latest

# Com volume persistente de dados
docker run -p 8000:8000 -v alluni_data:/app/data taiettedev/alluni:latest
```

🔗 [Veja no Docker Hub](https://hub.docker.com/r/taiettedev/alluni)

---

## 🛠️ Tecnologias Utilizadas

| Camada        | Tecnologias                            |
|---------------|-----------------------------------------|
| 🔙 Backend     | Django, Python                          |
| 🎨 Frontend    | HTML, Tailwind CSS, JavaScript          |
| 💾 Banco de Dados | SQLite (dev), PostgreSQL (produção)   |
| 🐳 Containerização | Docker                                |
| 🚀 CI/CD       | GitHub Actions                          |

---

## 📄 Licença

Distribuído sob a licença MIT.  
Consulte o arquivo [`LICENSE`](./LICENSE) para mais detalhes.

---

## 🤝 Contribuindo

Quer contribuir? Toda ajuda é bem-vinda!  
Leia nosso guia de contribuição ou abra uma issue com sugestões, bugs ou ideias.

---

<p align="center">
Desenvolvido por estudantes, para estudantes.
</p>

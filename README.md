# 🔧 Oficina Mecânica

Sistema web de controle de serviços prestados em veículos.

## 👤 Informações do Desenvolvedor

| Campo | Valor |
|-------|-------|
| Nome | Lucca Niklaus |
| Matrícula | 202602271931 |
| Domínio | Opção B — Oficina Mecânica |

---

## 📋 Sobre o Projeto

Aplicação Flask que gerencia uma oficina mecânica, permitindo:

- Cadastro de veículos (placa, marca, modelo, ano, proprietário)
- Registro de serviços prestados em cada veículo
- Consulta de histórico de serviços
- Busca por placa ou proprietário
- Validação de dados com regras de negócio

---

## 🚀 Como Rodar a Aplicação (Do Zero)

### 1. **Clonar o repositório**
```bash
git clone <seu-repo>
cd oficina_mecanica
```

### 2. **Criar ambiente virtual**
```bash
python -m venv .venv
```

### 3. **Ativar o ambiente virtual**

**No Windows:**
```bash
.venv\Scripts\activate
```

**No macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. **Instalar dependências**
```bash
pip install flask
```

### 5. **Criar e popular o banco de dados**
```bash
python cadastro_sqlite.py
python dados_iniciais.py
```

### 6. **Executar a aplicação**
```bash
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

---

## 📍 Rotas da Aplicação

### Veículos (Entidade Principal)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Lista todos os veículos |
| GET | `/novo` | Exibe formulário de cadastro |
| POST | `/novo` | Grava um novo veículo |
| GET | `/veiculo/<id>` | Detalhes do veículo + seus serviços |
| GET | `/veiculo/<id>/editar` | Formulário de edição |
| POST | `/veiculo/<id>/editar` | Atualiza os dados |
| POST | `/veiculo/<id>/excluir` | Exclui o veículo e seus serviços |
| GET | `/buscar` | Busca por placa ou proprietário |

### Serviços (Entidade Relacionada)

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/veiculo/<id>/servico` | Formulário de novo serviço |
| POST | `/veiculo/<id>/servico` | Registra um novo serviço |
| POST | `/servico/<id>/concluir` | Marca serviço como concluído |
| POST | `/servico/<id>/excluir` | Exclui um serviço |

---

## ✅ Validações Implementadas

### Veículos

1. **Placa obrigatória e formato correto**
   - Aceita: `ABC-1234` ou `ABC1234`
   - Mensagem: "Placa inválida. Use formato ABC-1234 ou ABC1234."

2. **Placa única (consulta banco)**
   - Não permite dois veículos com a mesma placa
   - Mensagem: "Esta placa já está cadastrada."

3. **Ano dentro de intervalo razoável**
   - Intervalo: 1950 a 2026
   - Mensagem: "Ano deve estar entre 1950 e 2026."

4. **Marca, modelo e proprietário obrigatórios**
   - Campos não podem ficar vazios
   - Mensagens: "[Campo] é obrigatório."

### Serviços

1. **Descrição obrigatória e comprimento mínimo**
   - Mínimo 3 caracteres
   - Mensagem: "Descrição deve ter no mínimo 3 caracteres."

2. **Valor obrigatório e positivo**
   - Deve ser > 0
   - Mensagem: "Valor deve ser um número positivo."

3. **Data obrigatória**
   - Campo não pode ficar vazio
   - Mensagem: "Data é obrigatória."

---

## 🗄️ Estrutura do Banco de Dados

### Tabela `veiculos`
```sql
CREATE TABLE veiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    placa TEXT NOT NULL UNIQUE,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ano INTEGER NOT NULL,
    proprietario TEXT NOT NULL,
    data_cadastro TEXT NOT NULL
);
```

### Tabela `servicos`
```sql
CREATE TABLE servicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    veiculo_id INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    data_entrada TEXT NOT NULL,
    valor REAL NOT NULL,
    concluido INTEGER DEFAULT 0,
    FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE
);
```

**Relação:** 1 veículo → muitos serviços (1:N)

---

## 📁 Estrutura de Arquivos

```
oficina_mecanica/
├── app.py                          # Aplicação principal com rotas
├── cadastro_sqlite.py              # Conexão e criação de tabelas
├── validacoes.py                   # Regras de validação
├── dados_iniciais.py               # Script para popular o banco
├── oficina.db                      # Banco SQLite (gerado automaticamente)
├── README.md                       # Este arquivo
├── .venv/                          # Ambiente virtual
├── templates/                      # Templates HTML (Jinja2)
│   ├── base.html                   # Template base (cabeçalho, menu, rodapé)
│   ├── lista.html                  # Lista de veículos
│   ├── detalhe.html                # Detalhes do veículo + serviços
│   ├── form_veiculo.html           # Formulário de veículo
│   ├── form_servico.html           # Formulário de serviço
│   ├── busca.html                  # Página de busca
│   └── erro.html                   # Página de erro (404)
└── static/
    └── estilo.css                  # Estilos CSS
```

---

## 🎨 Recursos de Design

✅ Cores no cabeçalho (azul escuro #2c3e50)  
✅ Tabelas formatadas com estilos profissionais  
✅ Mensagens de erro destacadas em vermelho  
✅ Responsivo (funciona em dispositivos móveis)  
✅ Navegação intuitiva  

---

## 📝 Dados Iniciais

O script `dados_iniciais.py` insere:

- **4 veículos** com proprietários diferentes
- **10 serviços** distribuídos entre os veículos
- **1 veículo sem serviços** (testa página vazia) — Toyota Corolla (PQR-4321)

Serviços com status:
- ✓ Concluídos (5)
- ● Pendentes (5)

---

## 🔍 Recursos Adicionais

### POST-Redirect-GET
- Após gravar dados (novo, editar), a aplicação redireciona para GET
- Evita resubmissão acidental ao apertar F5

### Tratamento de Erros
- Erros 404 e 500 são tratados com página customizada
- Erros de validação são mostrados no formulário com dados preservados

### Busca
- Busca por placa (case-insensitive)
- Busca por proprietário
- Ambos os campos são pesquisados simultaneamente

---

## ⚠️ O Que Faltou

Nada! ✅

Toda a funcionalidade obrigatória foi implementada:
- [x] Duas tabelas relacionadas (1:N)
- [x] Todas as rotas CRUD
- [x] Validações (3+ regras)
- [x] Regra que depende do banco (placa única)
- [x] Templates sem HTML em Python
- [x] Dados iniciais
- [x] README completo

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Flask** (framework web)
- **SQLite3** (banco de dados)
- **Jinja2** (templates HTML)
- **CSS3** (estilização)

---

## 📞 Contato

Desenvolvido por: **Lucca Niklaus**  
Matrícula: **202602271931**  
Período: **3º semestre**  
Disciplina: **IBM4023 — Projeto em Ciência de Dados I**

---

**Última atualização:** 13 de setembro de 2026

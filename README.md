# Monitoramento de Impressoras - Agente 🖨️

Agente assíncrono desenvolvido em Python para coleta de dados de contadores e status de impressoras via protocolo SNMP. O agente é capaz de escanear a rede, identificar dispositivos online e extrair informações críticas como número de série, modelo e volume de impressões.

## 📚 Sobre este Projeto (Estudo e Prática) - Em desenvolvimento
Este repositório é parte de um ecossistema maior de monitoramento de ativos, desenvolvido com o objetivo de consolidar conhecimentos em programação assíncrona, protocolos de rede e arquitetura de sistemas distribuídos. 

## 🚀 Tecnologias Principais

* <b> Python 3.13 </b> (Cpython)
* <b> FastAPI: </b> Interface de comunicação e API.
* <b> PySNMP (Lextudio): </b> Comunicação assíncrona com os dispositivos.
* <b> Poetry: </b> Gerenciamento de dependências e ambiente virtual.
* <b> Taskipy: </b> Automação de tarefas de desenvolvimento.

## 🛠️ Como Executar
Se você já seguiu os passos no [SETUP.md](SETUP.md), basta rodar:

```
# Entrar no ambiente virtual
poetry shell

# Rodar o agente em modo de desenvolvimento
task run

# ou se não funcionar
poetry run task run
```

O servidor estará disponível em http://127.0.0.1:8000.

## 📡 Endpoints Principais
### 1. Escanear Impressora
Realiza um ping e coleta dados SNMP de um IP específico.

* <b> POST </b> /scan/printers/
* <b> Payload: </b>

```
{
  "ip": "192.168.50.57",
  "branch_id": 1,
  "network_id": 10
}
```

### 2. Documentação Automática
Acesse o Swagger UI para testar todos os endpoints:

* <b> Swagger UI: </b> http://127.0.0.1:8000/docs

* <b> ReDoc: </b> http://127.0.0.1:8000/redoc

## ⚙️ Configurações Técnicas (MIBs/OIDs)

O agente utiliza os seguintes OIDs padrão para coleta:

* <b> Serial: </b> 1.3.6.1.2.1.43.5.1.1.17.1

* <b> Modelo: </b> 1.3.6.1.2.1.25.3.2.1.3.1

* <b> Contador Total: </b> 1.3.6.1.2.1.43.10.2.1.4.1.1

## 🧪 Desenvolvimento
Para garantir a qualidade do código, utilizamos ferramentas de linting e testes automatizados:

```
# Rodar análise de código e corretor ortográfico
task lint

# Formatar o código automaticamente (PEP-8)
task format

# Executar suíte de testes com cobertura (em desenvolvimento)
task test
```

## 📝 Notas de Versão
* <b> v0.1.0: </b> Implementação inicial da coleta assíncrona e integração com impressoras Samsung e HP.

## 📂 Documentação Auxiliar
Para entender como configurar o ambiente do zero ou contribuir com o projeto, veja o nosso guia:

👉 [Guia de Instalação e Setup](SETUP.md)

## Tenha no seu PC

- Python 3.10+
- PostgreSQL instalado e rodando localmente


## Pra instalar

```bash
# Clone o repositório
git clone https://github.com/JulianoSobroza/RP3.git     
cd RP3                              # Entre no diretório

python3 -m venv .venv               # Crie o ambiente virtual

source .venv/bin/activate           # Ative venv se Linux/macOS
.venv\\Scripts\\activate            # Ative venv se Windows

pip install -r requirements.txt     # Instale as dependências

python iniciar_bd.py                # Configurar BD pela primeira vez

python run.py                       # Pra rodar

http://127.0.0.1:5000               # Pra acessar o sistema
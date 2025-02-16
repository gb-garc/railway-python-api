import os
from flask import Flask
from app.funcionarios import funcionarios_bp

def create_app():
    flask_app = Flask(__name__)
    # Registrar blueprint do módulo de funcionários
    flask_app.register_blueprint(funcionarios_bp)
    return flask_app

app = create_app()

if __name__ == "__main__":
    # Para rodar localmente, caso você teste,
    # mas no Railway, iremos setar via variáveis de ambiente.
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

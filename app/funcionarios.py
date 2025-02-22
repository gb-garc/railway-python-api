from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from datetime import date, datetime  # importar explicitamente

funcionarios_bp = Blueprint('funcionarios', __name__)

# Rota opcional para criar/verificar a tabela
@funcionarios_bp.route("/init", methods=["POST"])
def init_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS "testesfuncionarios" (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                cargo VARCHAR(50),
                secao VARCHAR(50),
                situacao VARCHAR(2),
                admissao DATE,
                salario REAL,
                cpf VARCHAR(15),
                tipo VARCHAR(2),
                esocial VARCHAR(15),
                obra INTEGER,
                nascimento DATE,
                id_interno INTEGER
            );
            """
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Tabela testesfuncionarios criada/verificada."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE - Inserir
@funcionarios_bp.route("/funcionarios", methods=["POST"])
def create_funcionario():
    data = request.get_json() or {}

    # Extrai campos do JSON
    id_interno = data.get("id_interno")
    nome = data.get("nome")
    cargo = data.get("cargo")
    secao = data.get("secao")
    situacao = data.get("situacao")
    admissao = data.get("admissao")
    salario = data.get("salario")
    cpf = data.get("cpf")
    tipo = data.get("tipo")
    esocial = data.get("esocial")
    obra = data.get("obra")
    nascimento = data.get("nascimento")

    # Verifica campos obrigatórios
    if not nome or not nascimento or not cargo:
        return jsonify({"error": "Campos obrigatórios: nome, nascimento, cargo."}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Monta a query com todas as colunas
        query = """
            INSERT INTO "testesfuncionarios" (
                id_interno, nome, cargo, secao, situacao, admissao,
                salario, cpf, tipo, esocial, obra, nascimento
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, nome, nascimento, cargo;
        """

        cur.execute(
            query,
            (
                id_interno, nome, cargo, secao, situacao, admissao,
                salario, cpf, tipo, esocial, obra, nascimento
            )
        )
        novo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": novo[0],
            "nome": novo[1],
            "nascimento": str(novo[2]),
            "cargo": novo[3]
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ - Listar todos
@funcionarios_bp.route("/funcionarios", methods=["GET"])
def get_funcionarios():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM "testesfuncionarios"')
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()

        funcionarios = []
        for row in rows:
            row_dict = {}
            for i, col_name in enumerate(columns):
                value = row[i]
                # Se a coluna for do tipo data/datetime, converte para string
                if isinstance(value, (date, datetime)):
                    row_dict[col_name] = value.isoformat()
                else:
                    row_dict[col_name] = value
            funcionarios.append(row_dict)

        return jsonify(funcionarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE - Atualizar
@funcionarios_bp.route("/funcionarios/<int:func_id>", methods=["PUT"])
def update_funcionario(func_id):
    data = request.get_json() or {}
    nome = data.get("nome")
    data_nasc = data.get("data_de_nascimento")
    cargo = data.get("cargo")

    if not nome or not data_nasc or not cargo:
        return jsonify({"error": "Campos obrigatórios: nome, data_de_nascimento, cargo."}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            UPDATE "tbl_funcionarios"
            SET nome = %s, data_de_nascimento = %s, cargo = %s
            WHERE id = %s
            RETURNING id, nome, data_de_nascimento, cargo;
        """
        cur.execute(query, (nome, data_nasc, cargo, func_id))
        updated = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if updated is None:
            return jsonify({"message": "Funcionário não encontrado."}), 404

        return jsonify({
            "id": updated[0],
            "nome": updated[1],
            "data_de_nascimento": str(updated[2]),
            "cargo": updated[3]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Remover
@funcionarios_bp.route("/funcionarios/<int:func_id>", methods=["DELETE"])
def delete_funcionario(func_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            DELETE FROM "tbl_funcionarios"
            WHERE id = %s
            RETURNING id;
        """
        cur.execute(query, (func_id,))
        deleted = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if deleted is None:
            return jsonify({"message": "Funcionário não encontrado."}), 404

        return jsonify({"message": f"Funcionário ID={func_id} removido com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

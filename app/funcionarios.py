from flask import Blueprint, request, jsonify
from app.db import get_db_connection

funcionarios_bp = Blueprint('funcionarios', __name__)

# Exemplo: Rota opcional para criar/verificar a tabela
@funcionarios_bp.route("/init", methods=["POST"])
def init_table():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
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
                nascimento DATE
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Tabela tbl_funcionarios criada/verificada."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE - Inserir
@funcionarios_bp.route("/funcionarios", methods=["POST"])
def create_funcionario():
    data = request.get_json() or {}
    nome = data.get("nome")
    data_nasc = data.get("data_de_nascimento")
    cargo = data.get("cargo")
    id_interno=data.get("id")

    if not nome or not data_nasc or not cargo:
        return jsonify({"error": "Campos obrigatórios: nome, data_de_nascimento, cargo."}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            INSERT INTO "testesfuncionarios" (nome, data_de_nascimento, cargo, id_interno)
            VALUES (%s, %s, %s, %s)
            RETURNING id, nome, data_de_nascimento, cargo;
        """
        cur.execute(query, (nome, data_nasc, cargo))
        novo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            "id": novo[0],
            "nome": novo[1],
            "data_de_nascimento": str(novo[2]),
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
        cur.execute('SELECT id, nome, data_de_nascimento, cargo FROM "tbl_funcionarios"')
        rows = cur.fetchall()
        cur.close()
        conn.close()

        funcionarios = []
        for r in rows:
            funcionarios.append({
                "id": r[0],
                "nome": r[1],
                "data_de_nascimento": str(r[2]),
                "cargo": r[3]
            })
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

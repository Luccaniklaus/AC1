from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from cadastro_sqlite import conectar_banco, criar_tabelas
from validacoes import validar_veiculo, validar_servico

app = Flask(__name__)


@app.route("/")
def listar():
    """Página inicial: lista todos os veículos."""
    conn = conectar_banco()
    veiculos = conn.execute(
        'SELECT * FROM veiculos ORDER BY proprietario'
    ).fetchall()
    conn.close()

    return render_template("lista.html", veiculos=veiculos)


@app.route("/veiculo/<int:id_veiculo>")
def detalhe(id_veiculo):
    """Detalhes de um veículo e seus serviços."""
    conn = conectar_banco()
    veiculo = conn.execute(
        'SELECT * FROM veiculos WHERE id = ?',
        (id_veiculo,)
    ).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                             mensagem=f"Veículo com id {id_veiculo} não encontrado."), 404

    servicos = conn.execute(
        'SELECT * FROM servicos WHERE veiculo_id = ? ORDER BY data_entrada DESC',
        (id_veiculo,)
    ).fetchall()
    conn.close()

    return render_template("detalhe.html", veiculo=veiculo, servicos=servicos)


@app.route("/novo", methods=["GET", "POST"])
def novo():
    """Cadastra um novo veículo."""
    if request.method == "GET":
        return render_template("form_veiculo.html", titulo="Cadastrar veículo",
                             dados={}, erros={}, acao=url_for("novo"))

    dados = {
        "placa": request.form.get("placa", "").strip().upper(),
        "marca": request.form.get("marca", "").strip(),
        "modelo": request.form.get("modelo", "").strip(),
        "ano": request.form.get("ano", "").strip(),
        "proprietario": request.form.get("proprietario", "").strip(),
    }

    erros = validar_veiculo(dados)

    if erros:
        return render_template("form_veiculo.html", titulo="Cadastrar veículo",
                             dados=dados, erros=erros,
                             acao=url_for("novo")), 400

    conn = conectar_banco()
    conn.execute(
        'INSERT INTO veiculos (placa, marca, modelo, ano, proprietario, data_cadastro)'
        ' VALUES (?, ?, ?, ?, ?, ?)',
        (dados["placa"], dados["marca"], dados["modelo"], 
         int(dados["ano"]), dados["proprietario"],
         datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    )
    conn.commit()
    conn.close()

    return redirect(url_for("listar"))


@app.route("/veiculo/<int:id_veiculo>/editar", methods=["GET", "POST"])
def editar(id_veiculo):
    """Edita um veículo existente."""
    conn = conectar_banco()
    veiculo = conn.execute(
        'SELECT * FROM veiculos WHERE id = ?',
        (id_veiculo,)
    ).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                             mensagem=f"Veículo com id {id_veiculo} não encontrado."), 404

    if request.method == "GET":
        conn.close()
        return render_template("form_veiculo.html", 
                             titulo=f"Editar {veiculo['placa']}",
                             dados=dict(veiculo), erros={},
                             acao=url_for("editar", id_veiculo=id_veiculo))

    dados = {
        "placa": request.form.get("placa", "").strip().upper(),
        "marca": request.form.get("marca", "").strip(),
        "modelo": request.form.get("modelo", "").strip(),
        "ano": request.form.get("ano", "").strip(),
        "proprietario": request.form.get("proprietario", "").strip(),
    }

    erros = validar_veiculo(dados, id_atual=id_veiculo)

    if erros:
        conn.close()
        return render_template("form_veiculo.html",
                             titulo=f"Editar {veiculo['placa']}",
                             dados=dados, erros=erros,
                             acao=url_for("editar", id_veiculo=id_veiculo)), 400

    conn.execute(
        'UPDATE veiculos SET placa = ?, marca = ?, modelo = ?, ano = ?, proprietario = ?'
        ' WHERE id = ?',
        (dados["placa"], dados["marca"], dados["modelo"],
         int(dados["ano"]), dados["proprietario"], id_veiculo)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("detalhe", id_veiculo=id_veiculo))


@app.route("/veiculo/<int:id_veiculo>/excluir", methods=["POST"])
def excluir(id_veiculo):
    """Exclui um veículo e seus serviços."""
    conn = conectar_banco()
    veiculo = conn.execute(
        'SELECT * FROM veiculos WHERE id = ?',
        (id_veiculo,)
    ).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                             mensagem=f"Veículo com id {id_veiculo} não encontrado."), 404

    placa = veiculo['placa']
    conn.execute('DELETE FROM veiculos WHERE id = ?', (id_veiculo,))
    conn.commit()
    conn.close()

    return redirect(url_for("listar"))


@app.route("/buscar")
def buscar():
    """Busca por placa ou proprietário."""
    termo = request.args.get("termo", "").strip().lower()

    encontrados = []
    if termo:
        conn = conectar_banco()
        encontrados = conn.execute(
            'SELECT * FROM veiculos WHERE LOWER(placa) LIKE ? OR LOWER(proprietario) LIKE ? ORDER BY proprietario',
            (f'%{termo}%', f'%{termo}%')
        ).fetchall()
        conn.close()

    return render_template("busca.html", termo=termo, veiculos=encontrados)


@app.route("/veiculo/<int:id_veiculo>/servico", methods=["GET", "POST"])
def novo_servico(id_veiculo):
    """Cria um novo serviço para um veículo."""
    conn = conectar_banco()
    veiculo = conn.execute(
        'SELECT * FROM veiculos WHERE id = ?',
        (id_veiculo,)
    ).fetchone()

    if veiculo is None:
        conn.close()
        return render_template("erro.html",
                             mensagem=f"Veículo não encontrado."), 404

    if request.method == "GET":
        conn.close()
        return render_template("form_servico.html", titulo="Novo serviço",
                             veiculo=veiculo, dados={}, erros={},
                             acao=url_for("novo_servico", id_veiculo=id_veiculo))

    dados = {
        "descricao": request.form.get("descricao", "").strip(),
        "data_entrada": request.form.get("data_entrada", "").strip(),
        "valor": request.form.get("valor", "").strip(),
    }

    erros = validar_servico(dados)

    if erros:
        conn.close()
        return render_template("form_servico.html", titulo="Novo serviço",
                             veiculo=veiculo, dados=dados, erros=erros,
                             acao=url_for("novo_servico", id_veiculo=id_veiculo)), 400

    conn.execute(
        'INSERT INTO servicos (veiculo_id, descricao, data_entrada, valor, concluido)'
        ' VALUES (?, ?, ?, ?, 0)',
        (id_veiculo, dados["descricao"], dados["data_entrada"], float(dados["valor"]))
    )
    conn.commit()
    conn.close()

    return redirect(url_for("detalhe", id_veiculo=id_veiculo))


@app.route("/servico/<int:id_servico>/concluir", methods=["POST"])
def concluir_servico(id_servico):
    """Marca um serviço como concluído."""
    conn = conectar_banco()
    servico = conn.execute(
        'SELECT veiculo_id FROM servicos WHERE id = ?',
        (id_servico,)
    ).fetchone()

    if servico is None:
        conn.close()
        return render_template("erro.html",
                             mensagem="Serviço não encontrado."), 404

    id_veiculo = servico['veiculo_id']
    conn.execute(
        'UPDATE servicos SET concluido = 1 WHERE id = ?',
        (id_servico,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("detalhe", id_veiculo=id_veiculo))


@app.route("/servico/<int:id_servico>/excluir", methods=["POST"])
def excluir_servico(id_servico):
    """Exclui um serviço."""
    conn = conectar_banco()
    servico = conn.execute(
        'SELECT veiculo_id FROM servicos WHERE id = ?',
        (id_servico,)
    ).fetchone()

    if servico is None:
        conn.close()
        return render_template("erro.html",
                             mensagem="Serviço não encontrado."), 404

    id_veiculo = servico['veiculo_id']
    conn.execute('DELETE FROM servicos WHERE id = ?', (id_servico,))
    conn.commit()
    conn.close()

    return redirect(url_for("detalhe", id_veiculo=id_veiculo))


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    """Trata erros 404."""
    return render_template("erro.html",
                         mensagem="Página não encontrada."), 404


@app.errorhandler(500)
def erro_interno(erro):
    """Trata erros 500."""
    return render_template("erro.html",
                         mensagem="Erro interno do servidor."), 500


if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True, port=8000) 

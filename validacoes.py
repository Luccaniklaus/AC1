import re
from cadastro_sqlite import conectar_banco


def validar_placa(placa):
    """Valida o formato da placa (ABC-1234 ou ABCD1234)."""
    placa = placa.strip().upper()
    # Aceita: ABC-1234 ou ABC1234
    if re.match(r'^[A-Z]{3}-?\d{4}$', placa):
        return True
    return False


def validar_ano(ano_str):
    """Valida se o ano está entre 1950 e 2026."""
    try:
        ano = int(ano_str)
        return 1950 <= ano <= 2026
    except ValueError:
        return False


def validar_valor(valor_str):
    """Valida se o valor é positivo."""
    try:
        valor = float(valor_str)
        return valor > 0
    except ValueError:
        return False


def placa_existe(placa, id_atual=None):
    """Verifica se a placa já existe (para outro veículo)."""
    conn = conectar_banco()
    placa = placa.strip().upper()
    
    if id_atual:
        # Editando: ignora o veículo atual
        resultado = conn.execute(
            'SELECT id FROM veiculos WHERE UPPER(placa) = ? AND id != ?',
            (placa, id_atual)
        ).fetchone()
    else:
        # Criando: qualquer ocorrência é erro
        resultado = conn.execute(
            'SELECT id FROM veiculos WHERE UPPER(placa) = ?',
            (placa,)
        ).fetchone()
    
    conn.close()
    return resultado is not None


def validar_veiculo(dados, id_atual=None):
    """Valida todos os dados de um veículo. Retorna dict de erros."""
    erros = {}

    # Placa obrigatória
    if not dados.get("placa"):
        erros["placa"] = "Placa é obrigatória."
    elif not validar_placa(dados["placa"]):
        erros["placa"] = "Placa inválida. Use formato ABC-1234 ou ABC1234."
    elif placa_existe(dados["placa"], id_atual):
        erros["placa"] = "Esta placa já está cadastrada."

    # Marca obrigatória
    if not dados.get("marca"):
        erros["marca"] = "Marca é obrigatória."

    # Modelo obrigatório
    if not dados.get("modelo"):
        erros["modelo"] = "Modelo é obrigatório."

    # Ano válido
    if not dados.get("ano"):
        erros["ano"] = "Ano é obrigatório."
    elif not validar_ano(dados["ano"]):
        erros["ano"] = "Ano deve estar entre 1950 e 2026."

    # Proprietário obrigatório
    if not dados.get("proprietario"):
        erros["proprietario"] = "Nome do proprietário é obrigatório."

    return erros


def validar_servico(dados):
    """Valida dados de um serviço. Retorna dict de erros."""
    erros = {}

    # Descrição obrigatória
    if not dados.get("descricao"):
        erros["descricao"] = "Descrição é obrigatória."
    elif len(dados["descricao"]) < 3:
        erros["descricao"] = "Descrição deve ter no mínimo 3 caracteres."

    # Data obrigatória
    if not dados.get("data_entrada"):
        erros["data_entrada"] = "Data é obrigatória."

    # Valor obrigatório e positivo
    if not dados.get("valor"):
        erros["valor"] = "Valor é obrigatório."
    elif not validar_valor(dados["valor"]):
        erros["valor"] = "Valor deve ser um número positivo."

    return erros

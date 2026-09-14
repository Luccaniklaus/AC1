#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados iniciais.
Execute: python dados_iniciais.py
"""

from cadastro_sqlite import conectar_banco, criar_tabelas
from datetime import datetime, timedelta

def popular_banco():
    """Insere dados iniciais no banco."""
    
    # Criar tabelas
    criar_tabelas()
    
    conn = conectar_banco()
    cursor = conn.cursor()

    # Limpar dados existentes (opcional)
    print("Limpando dados anteriores...")
    cursor.execute("DELETE FROM servicos")
    cursor.execute("DELETE FROM veiculos")

    # Inserir 3 veículos
    print("Inserindo veículos...")
    veiculos = [
        ("ABC-1234", "Volkswagen", "Gol", 2018, "João Silva", datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        ("XYZ-5678", "Fiat", "Uno", 2015, "Maria Santos", (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y %H:%M:%S")),
        ("MNO-9999", "Chevrolet", "Celta", 2010, "Pedro Oliveira", (datetime.now() - timedelta(days=60)).strftime("%d/%m/%Y %H:%M:%S")),
        ("PQR-4321", "Toyota", "Corolla", 2020, "Ana Costa", (datetime.now() - timedelta(days=90)).strftime("%d/%m/%Y %H:%M:%S")),
    ]

    cursor.executemany(
        "INSERT INTO veiculos (placa, marca, modelo, ano, proprietario, data_cadastro) VALUES (?, ?, ?, ?, ?, ?)",
        veiculos
    )

    # Inserir 5+ serviços para os primeiros 3 veículos
    print("Inserindo serviços...")
    servicos = [
        # Serviços do Gol (ABC-1234)
        (1, "Troca de óleo e filtro", "15/08/2026", 150.00, 1),
        (1, "Revisão geral", "20/08/2026", 450.00, 1),
        (1, "Troca de pneus", "25/08/2026", 800.00, 0),
        
        # Serviços do Uno (XYZ-5678)
        (2, "Alinhamento e balanceamento", "10/08/2026", 200.00, 1),
        (2, "Troca de pastilhas de freio", "12/08/2026", 280.00, 1),
        (2, "Limpeza do motor", "18/08/2026", 120.00, 0),
        (2, "Troca de bateria", "22/08/2026", 350.00, 0),
        
        # Serviços do Celta (MNO-9999)
        (3, "Reparo do sistema de ar condicionado", "05/08/2026", 600.00, 1),
        (3, "Troca de amortecedores", "08/08/2026", 950.00, 0),
        
        # Serviços do Corolla (PQR-4321)
        (4, "Manutenção preventiva", "01/09/2026", 500.00, 0),
    ]

    cursor.executemany(
        "INSERT INTO servicos (veiculo_id, descricao, data_entrada, valor, concluido) VALUES (?, ?, ?, ?, ?)",
        servicos
    )

    conn.commit()
    conn.close()

    print("✅ Banco de dados populado com sucesso!")
    print("\n📊 Resumo:")
    print("  • 4 veículos inseridos")
    print("  • 10 serviços inseridos")
    print("  • Veículo PQR-4321 tem apenas 1 serviço (teste de lista vazia)")


if __name__ == "__main__":
    popular_banco()

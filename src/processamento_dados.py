import pandas as pd
import os
from pathlib import Path

def carregar_dados():
    try:
        # Caminho mais robusto usando pathlib
        caminho = Path('data') / 'clientes.csv'
        
        if not caminho.exists():
            # Fallback para desenvolvimento - criar dados de exemplo
            print("⚠️ Arquivo não encontrado, usando dados de exemplo")
            return pd.DataFrame({
                'sexo': ['M', 'F', 'M', 'F'],
                'bairro': ['Centro', 'Vila Olímpia', 'Centro', 'Moema'],
                'itens_higienizados': ['Sofá', 'Cadeira', 'Sofá', 'Poltrona'],
                'valor_servico': [350.50, 420.0, 380.25, 500.75]
            })
        
        # Leitura com tratamento robusto
        dados = pd.read_csv(
            caminho,
            encoding='utf-8',
            dtype={'valor_servico': str},
            na_values=['', 'NA', 'N/A']
        )
        
        # Processamento seguro
        if 'valor_servico' in dados.columns:
            dados['valor_servico'] = (
                dados['valor_servico']
                .str.replace(r'[^\d.]', '', regex=True)
                .replace('', '0')
                .astype(float) )
        
        return dados
    
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        # Retorna DataFrame vazio para não quebrar o dashboard
        return pd.DataFrame()
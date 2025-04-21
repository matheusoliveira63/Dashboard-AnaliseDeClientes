import pandas as pd
import os
from pathlib import Path

def carregar_dados():
    try:
        caminho = Path('data') / 'clientes.csv'
        
        if not caminho.exists():
            # Dados de exemplo se o arquivo não existir
            return pd.DataFrame({
                'sexo': ['M', 'F', 'M', 'F'],
                'bairro': ['Centro', 'Vila Olímpia', 'Centro', 'Moema'],
                'itens_higienizados': ['Sofá', 'Cadeira', 'Sofá', 'Poltrona'],
                'valor_servico': [350.50, 420.0, 380.25, 500.75]
            })
        
        return pd.read_csv(caminho, encoding='utf-8')
    
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()
import pandas as pd
import os

def carregar_dados():
    try:
        caminho = os.path.join('data', 'clientes.csv')
        
        # Leitura com tratamento explícito de decimais
        dados = pd.read_csv(
            caminho,
            encoding='utf-8',
            dtype={'valor_servico': str}  # Força leitura como string
        )
        
        # Conversão segura para valores monetários
        dados['valor_servico'] = (
            dados['valor_servico']
            .str.replace('R\$', '', regex=True)  # Remove R$
            .str.replace(',', '', regex=True)  # Remove vírgulas (se houver)
            .str.strip()  # Remove espaços
            .replace('', '0')  # Substitui vazios por 0
            .astype(float)  # Converte para float
            .round(2)  # Arredonda para 2 decimais
        )
        
        return dados
    
    except Exception as e:
        print(f"\nERRO CRÍTICO: {str(e)}")
        return pd.DataFrame()
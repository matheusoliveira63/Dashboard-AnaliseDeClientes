# -*- coding: utf-8 -*-
from collections import Counter
import pandas as pd

def gerar_insights(dados):
    """
    Gera insights estratégicos a partir dos dados dos clientes.
    Retorna uma lista de strings formatadas para exibição no dashboard.
    """
    insights = []
    
    # Verifica se há dados válidos
    if dados.empty or not isinstance(dados, pd.DataFrame):
        return ["⚠️ Nenhum dado válido encontrado"]
    
    try:
        # --- ANÁLISE DEMOGRÁFICA ---
        if 'sexo' in dados.columns:
            contagem_sexo = dados['sexo'].value_counts(normalize=True) * 100
            for sexo, percentual in contagem_sexo.items():
                insights.append(f"👥 {sexo}: {percentual:.1f}%")
        
        # --- TOP BAIRROS ---
        if 'bairro' in dados.columns:
            top_bairros = dados['bairro'].value_counts().head(3)
            insights.append("\n🏘️ **Top Bairros:**")
            for bairro, quantidade in top_bairros.items():
                insights.append(f"• {bairro}: {quantidade} clientes")
        
        # --- ITENS MAIS POPULARES ---
        if 'itens_higienizados' in dados.columns:
            itens = dados['itens_higienizados'].value_counts().head(3)
            if not itens.empty:
                insights.append("\n🧼 **Itens Mais Higienizados:**")
                for item, quantidade in itens.items():
                    insights.append(f"• {item}: {quantidade}x")
        
        if 'itens_impermeabilizados' in dados.columns:
            itens = dados['itens_impermeabilizados'].value_counts().head(3)
            if not itens.empty:
                insights.append("\n🛡️ **Itens Mais Impermeabilizados:**")
                for item, quantidade in itens.items():
                    insights.append(f"• {item}: {quantidade}x")
        
        # --- ANÁLISE FINANCEIRA ---
        if 'valor_servico' in dados.columns:
            media = dados['valor_servico'].mean()
            maximo = dados['valor_servico'].max()
            minimo = dados['valor_servico'].min()
            
            # Formatação profissional para BRL (Real Brasileiro)
            def formatar_moeda(valor):
                return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            
            insights.append("\n💰 **Análise Financeira:**")
            insights.append(f"• Valor médio: {formatar_moeda(media)}")
            insights.append(f"• Ticket máximo: {formatar_moeda(maximo)}")
            insights.append(f"• Ticket mínimo: {formatar_moeda(minimo)}")
        
        # --- SUGESTÕES DE CAMPANHA ---
        insights.append("\n📈 **Sugestões para Tráfego Pago:**")
        
        if 'sexo' in dados.columns and len(dados['sexo'].unique()) > 1:
            sexo_maioria = dados['sexo'].mode()[0]
            insights.append(f"• Segmentar anúncios para público {sexo_maioria}")
        
        if 'bairro' in dados.columns:
            bairro_top = dados['bairro'].mode()[0]
            insights.append(f"• Geotargeting em {bairro_top} e arredores")
        
        if 'itens_higienizados' in dados.columns:
            item_top = dados['itens_higienizados'].mode()[0]
            insights.append(f"• Destaque promoções para {item_top}")
    
    except Exception as e:
        insights.append(f"\n⚠️ Erro na análise: {str(e)}")
    
    return insights


# Teste local (execute com `python insights.py`)
if __name__ == "__main__":
    # Dados de exemplo para teste
    dados_teste = pd.DataFrame({
        'sexo': ['M', 'F', 'M', 'M'],
        'bairro': ['Centro', 'Vila Olímpia', 'Centro', 'Moema'],
        'itens_higienizados': ['Sofá', 'Cadeira', 'Sofá', 'Poltrona'],
        'itens_impermeabilizados': ['Sofá', '', 'Sofá', 'Cadeira'],
        'valor_servico': [350.50, 420.0, 380.25, 500.75]
    })
    
    print("=== TESTE DE INSIGHTS ===")
    for insight in gerar_insights(dados_teste):
        print(insight)
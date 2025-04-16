import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
from processamento_dados import carregar_dados
from insights import gerar_insights

# =============================================
# CONFIGURAÇÃO INICIAL
# =============================================
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap'
]

# Primeiro carregamos os dados
dados = carregar_dados()

# Depois inicializamos o app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# =============================================
# PALETA DE CORES - SOFÁ NOVO DE NOVO
# =============================================
CORES = {
    'primaria': '#1A3967',
    'secundaria': '#E6AF2E',
    'terciaria': '#FFFFFF',
    'texto': '#333333',
    'fundo': '#F7F7F7',
    'destaque': '#1A3967',
    'sucesso': '#4CAF50',
    'gradiente': 'linear-gradient(135deg, #1A3967 0%, #0D1F3D 100%)'
}

# =============================================
# ESTILOS CSS PERSONALIZADOS
# =============================================
app.layout = html.Div(style={
    'fontFamily': "'Poppins', sans-serif",
    'backgroundColor': CORES['fundo'],
    'minHeight': '100vh',
    'margin': '0',
    'padding': '0'
}, children=[
    # Barra de Navegação Superior Fixa
    html.Div(style={
        'background': CORES['gradiente'],
        'color': CORES['terciaria'],
        'padding': '15px 25px',
        'position': 'sticky',
        'top': '0',
        'zIndex': '100',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between'
    }, children=[
        html.Div([
            html.Img(
                src=app.get_asset_url('logo.png'),
                style={'height': '100px'}
            ),
        ]),
        html.Div([
            html.H1("Análise de Clientes", style={
                'margin': '0',
                'fontSize': '34px',
                'fontWeight': '600'
            }),
            html.P("Sofá Novo de Novo - Santo Amaro", style={
                'margin': '0',
                'fontSize': '20px',
                'opacity': '0.9'
            })
        ])
    ]),
    
    # Container Principal
    html.Div(style={
        'padding': '20px',
        'maxWidth': '1400px',
        'margin': '0 auto'
    }, children=[
        # Linha de Filtros (2 colunas)
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(2, 1fr)',
            'gap': '20px',
            'marginBottom': '25px'
        }, children=[
            # Filtro Sexo
            html.Div([
                html.Label("Filtrar por Sexo", style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'fontWeight': '600',
                    'color': CORES['texto']
                }),
                dcc.Dropdown(
                    id='filtro-sexo',
                    options=[{'label': 'Todos', 'value': 'all'}] + 
                           [{'label': sexo, 'value': sexo} for sexo in dados['sexo'].unique()],
                    value='all',
                    clearable=False,
                    style={
                        'width': '100%',
                        'border': f'1px solid {CORES["primaria"]}'
                    }
                )
            ]),
            
            # Filtro Bairro
            html.Div([
                html.Label("Filtrar por Bairro", style={
                    'display': 'block',
                    'marginBottom': '8px',
                    'fontWeight': '600',
                    'color': CORES['texto']
                }),
                dcc.Dropdown(
                    id='filtro-bairro',
                    options=[{'label': 'Todos', 'value': 'all'}] + 
                           [{'label': bairro, 'value': bairro} for bairro in dados['bairro'].unique()],
                    value='all',
                    clearable=False,
                    style={
                        'width': '100%',
                        'border': f'1px solid {CORES["primaria"]}'
                    }
                )
            ])
        ]),
        
        # Grade de Gráficos (3 colunas responsivas)
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(350px, 1fr))',
            'gap': '20px',
            'marginBottom': '25px'
        }, children=[
            # Gráfico de Sexo
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '8px',
                'padding': '15px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)',
                'minHeight': '400px'
            }, children=[
                dcc.Graph(
                    id='grafico-sexo',
                    config={'displayModeBar': False},
                    style={'height': '100%'}
                )
            ]),
            
            # Gráfico de Bairros
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '8px',
                'padding': '15px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)',
                'minHeight': '400px'
            }, children=[
                dcc.Graph(
                    id='grafico-bairros',
                    config={'displayModeBar': False},
                    style={'height': '100%'}
                )
            ]),
            
            # Gráfico de Itens
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '8px',
                'padding': '15px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)',
                'minHeight': '400px'
            }, children=[
                dcc.Graph(
                    id='grafico-itens',
                    config={'displayModeBar': False},
                    style={'height': '100%'}
                )
            ])
        ]),
        
        # Área Inferior (Tabela + Insights)
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'minmax(0, 2fr) minmax(0, 1fr)',
            'gap': '20px',
            'marginBottom': '25px'
        }, children=[
            # Tabela de Dados
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)'
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'marginBottom': '15px'
                }, children=[
                    html.H3("Dados dos Clientes", style={
                        'color': CORES['primaria'],
                        'margin': '0',
                        'fontSize': '20px'
                    }),
                    html.Div([
                        html.Span("Itens por página: ", style={'marginRight': '10px'}),
                        dcc.Dropdown(
                            id='page-size',
                            options=[{'label': str(i), 'value': i} for i in [5, 10, 20]],
                            value=10,
                            clearable=False,
                            style={
                                'width': '80px',
                                'display': 'inline-block'
                            }
                        )
                    ])
                ]),
                dash_table.DataTable(
                    id='tabela-clientes',
                    columns=[{"name": i, "id": i} for i in dados.columns],
                    page_size=10,
                    style_table={
                        'overflowX': 'auto',
                        'borderRadius': '8px'
                    },
                    style_header={
                        'backgroundColor': CORES['primaria'],
                        'color': CORES['terciaria'],
                        'fontWeight': 'bold',
                        'border': 'none'
                    },
                    style_cell={
                        'padding': '12px',
                        'textAlign': 'left',
                        'border': f'1px solid {CORES["fundo"]}',
                        'maxWidth': '150px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': CORES['fundo']
                        },
                        {
                            'if': {'column_id': 'valor_servico'},
                            'color': CORES['secundaria'],
                            'fontWeight': 'bold'
                        }
                    ],
                    tooltip_data=[
                        {
                            column: {'value': str(value), 'type': 'markdown'}
                            for column, value in row.items()
                        } for row in dados.to_dict('records')
                    ],
                    tooltip_duration=None
                )
            ]),
            
            # Card de Insights (com scroll)
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '8px',
                'padding': '20px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.05)',
                'height': '500px',
                'display': 'flex',
                'flexDirection': 'column'
            }, children=[
                html.H3("Insights Estratégicos", style={
                    'color': CORES['primaria'],
                    'marginTop': '0',
                    'marginBottom': '15px',
                    'fontSize': '20px',
                    'position': 'sticky',
                    'top': '0',
                    'backgroundColor': CORES['terciaria'],
                    'zIndex': '1',
                    'paddingBottom': '10px',
                    'borderBottom': f'2px solid {CORES["secundaria"]}'
                }),
                html.Div(
                    id='div-insights',
                    style={
                        'flex': '1',
                        'overflowY': 'auto',
                        'paddingRight': '10px',
                        'scrollbarWidth': 'thin',
                        'scrollbarColor': f'{CORES["secundaria"]} {CORES["fundo"]}'
                    }
                )
            ])
        ])
    ]),
    
    # Rodapé
    html.Footer(style={
        'textAlign': 'center',
        'padding': '20px',
        'backgroundColor': CORES['primaria'],
        'color': CORES['terciaria'],
        'marginTop': '40px'
    }, children=[
        html.P("© 2023 Sofá Novo de Novo | Todos os direitos reservados"),
        html.P("Dashboard Analytics | v1.0", style={'opacity': '0.8', 'marginTop': '5px'})
    ])
])

# =============================================
# CALLBACKS PARA ATUALIZAÇÃO DINÂMICA
# =============================================
@app.callback(
    [Output('grafico-sexo', 'figure'),
     Output('grafico-bairros', 'figure'),
     Output('grafico-itens', 'figure'),
     Output('tabela-clientes', 'data'),
     Output('tabela-clientes', 'page_size')],
    [Input('filtro-sexo', 'value'),
     Input('filtro-bairro', 'value'),
     Input('page-size', 'value')]
)
def atualizar_conteudo(sexo, bairro, page_size):
    df_filtrado = dados.copy()
    
    # Aplicar filtros
    if sexo != 'all':
        df_filtrado = df_filtrado[df_filtrado['sexo'] == sexo]
    if bairro != 'all':
        df_filtrado = df_filtrado[df_filtrado['bairro'] == bairro]
    
    # Gráfico de Distribuição por Sexo
    contagem_sexo = df_filtrado['sexo'].value_counts().reset_index()
    contagem_sexo.columns = ['sexo', 'quantidade']
    
    fig_sexo = px.pie(
        contagem_sexo,
        values='quantidade',
        names='sexo',
        title='Distribuição por Sexo',
        color_discrete_sequence=[CORES['primaria'], CORES['secundaria']],
        hole=0.4
    )
    fig_sexo.update_layout(
        title_x=0.5,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=False,
        plot_bgcolor=CORES['terciaria'],
        paper_bgcolor=CORES['terciaria'],
        font=dict(color=CORES['texto'])
    )
    fig_sexo.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color=CORES['terciaria'], width=1))
    )
    
    # Gráfico de Top Bairros
    contagem_bairros = df_filtrado['bairro'].value_counts().reset_index()
    contagem_bairros.columns = ['bairro', 'quantidade']
    
    fig_bairros = px.bar(
        contagem_bairros.head(10),
        x='quantidade',
        y='bairro',
        title='Top 10 Bairros',
        orientation='h',
        color='quantidade',
        color_continuous_scale=[CORES['fundo'], CORES['primaria']]
    )
    fig_bairros.update_layout(
        title_x=0.5,
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False,
        margin=dict(l=100, r=20, t=60, b=20),
        plot_bgcolor=CORES['terciaria'],
        paper_bgcolor=CORES['terciaria'],
        font=dict(color=CORES['texto'])
    )
    
    # Gráfico de Itens Mais Higienizados
    contagem_itens = df_filtrado['itens_higienizados'].value_counts().reset_index()
    contagem_itens.columns = ['item', 'quantidade']
    
    fig_itens = px.bar(
        contagem_itens.head(10),
        x='item',
        y='quantidade',
        title='Top 10 Itens Higienizados',
        color='quantidade',
        color_continuous_scale=[CORES['fundo'], CORES['secundaria']]
    )
    fig_itens.update_layout(
        title_x=0.5,
        xaxis_tickangle=-45,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=80),
        plot_bgcolor=CORES['terciaria'],
        paper_bgcolor=CORES['terciaria'],
        font=dict(color=CORES['texto'])
    )
    
    return fig_sexo, fig_bairros, fig_itens, df_filtrado.to_dict('records'), page_size

@app.callback(
    Output('div-insights', 'children'),
    [Input('filtro-sexo', 'value'),
     Input('filtro-bairro', 'value')]
)
def atualizar_insights(sexo, bairro):
    df_filtrado = dados.copy()
    if sexo != 'all':
        df_filtrado = df_filtrado[df_filtrado['sexo'] == sexo]
    if bairro != 'all':
        df_filtrado = df_filtrado[df_filtrado['bairro'] == bairro]
    
    insights = gerar_insights(df_filtrado)
    
    return html.Ul([
        html.Li(
            dcc.Markdown(insight),
            style={
                'marginBottom': '12px',
                'padding': '12px',
                'backgroundColor': CORES['fundo'],
                'borderRadius': '6px',
                'borderLeft': f'4px solid {CORES["secundaria"]}',
                'listStyleType': 'none'
            }
        ) for insight in insights
    ])

# =============================================
# INICIALIZAÇÃO DO APLICATIVO
# =============================================
if __name__ == '__main__':
    app.run(debug=True)   
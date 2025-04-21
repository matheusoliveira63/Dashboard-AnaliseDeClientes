import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from src.processamento_dados import carregar_dados
from src.insights import gerar_insights

# =============================================
# CONFIGURAÇÃO INICIAL
# =============================================
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap'
]

dados = carregar_dados()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# =============================================
# PALETA DE CORES PROFISSIONAL (OPÇÃO 2)
# =============================================
CORES = {
    'primaria': '#2C3E50',       # Azul petróleo
    'secundaria': '#E74C3C',     # Vermelho terroso (destaque)
    'terciaria': '#ECF0F1',      # Branco gelo
    'fundo': '#FDFDFD',          # Branco neutro
    'destaque': '#3498DB',       # Azul médio
    'texto': '#34495E',          # Azul grafite
    'borda': '#BDC3C7',          # Cinza prateado
    'sucesso': '#2ECC71',        # Verde
    'gradiente': 'linear-gradient(135deg, #2C3E50 0%, #34495E 100%)'
}

# =============================================
# LAYOUT DO DASHBOARD
# =============================================
app.layout = html.Div(style={
    'fontFamily': "'Montserrat', sans-serif",
    'backgroundColor': CORES['fundo'],
    'minHeight': '100vh',
    'margin': '0',
    'padding': '0',
    'color': CORES['texto']
}, children=[
    # Barra de Navegação Superior (Premium)
    html.Div(style={
        'background': CORES['gradiente'],
        'color': CORES['terciaria'],
        'padding': '25px 40px',
        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between',
        'position': 'sticky',
        'top': '0',
        'zIndex': '1000',
        'borderBottom': f'3px solid {CORES["secundaria"]}'
    }, children=[
        html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[

            
            html.H1("SOFA NOVODENOVO", style={
                'margin': '0',
                'fontSize': '32px',
                'fontWeight': '700',
                'letterSpacing': '2px',
                'textTransform': 'uppercase'
            }),
            html.Div(style={
                'height': '40px',
                'width': '3px',
                'backgroundColor': CORES['secundaria'],
                'margin': '0 20px',
                'opacity': '0.8'
            }),
            html.P("DASHBOARD ANALÍTICO", style={
                'margin': '0',
                'fontSize': '18px',
                'fontWeight': '300',
                'letterSpacing': '1px',
                'opacity': '0.9'
                
            })
        ]),
    ]),
    
    # Container Principal
    html.Div(style={
        'padding': '30px 40px',
        'maxWidth': '1600px',
        'margin': '0 auto'
    }, children=[
        # Linha de Filtros (Premium)
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(300px, 1fr))',
            'gap': '25px',
            'marginBottom': '30px'
        }, children=[
            # Filtro Sexo
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '10px',
                'padding': '20px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["destaque"]}',
                'transition': 'all 0.3s ease'
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'marginBottom': '15px'
                }, children=[
                    html.I(className="fas fa-venus-mars", style={
                        'color': CORES['destaque'],
                        'fontSize': '20px',
                        'marginRight': '10px'
                    }),
                    html.Label("FILTRAR POR SEXO", style={
                        'fontWeight': '600',
                        'color': CORES['primaria'],
                        'fontSize': '14px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px'
                    })
                ]),
                dcc.Dropdown(
                    id='filtro-sexo',
                    options=[{'label': 'Todos', 'value': 'all'}] + 
                           [{'label': sexo, 'value': sexo} for sexo in dados['sexo'].unique()],
                    value='all',
                    clearable=False,
                    style={
                        'width': '100%',
                        'border': f'1px solid {CORES["borda"]}',
                        'borderRadius': '8px',
                        'fontFamily': "'Montserrat', sans-serif"
                    }
                )
            ]),
            
            # Filtro Bairro
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '10px',
                'padding': '20px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["sucesso"]}',
                'transition': 'all 0.3s ease'
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'marginBottom': '15px'
                }, children=[
                    html.I(className="fas fa-map-marker-alt", style={
                        'color': CORES['sucesso'],
                        'fontSize': '20px',
                        'marginRight': '10px'
                    }),
                    html.Label("FILTRAR POR BAIRRO", style={
                        'fontWeight': '600',
                        'color': CORES['primaria'],
                        'fontSize': '14px',
                        'textTransform': 'uppercase',
                        'letterSpacing': '1px'
                    })
                ]),
                dcc.Dropdown(
                    id='filtro-bairro',
                    options=[{'label': 'Todos', 'value': 'all'}] + 
                           [{'label': bairro, 'value': bairro} for bairro in dados['bairro'].unique()],
                    value='all',
                    clearable=False,
                    style={
                        'width': '100%',
                        'border': f'1px solid {CORES["borda"]}',
                        'borderRadius': '8px',
                        'fontFamily': "'Montserrat', sans-serif"
                    }
                )
            ])
        ]),
        
        # Grade de Gráficos (Premium)
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))',
            'gap': '25px',
            'marginBottom': '30px'
        }, children=[
            # Gráfico de Sexo
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '12px',
                'padding': '25px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["secundaria"]}',
                'minHeight': '450px',
                'display': 'flex',
                'flexDirection': 'column',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'transform': 'translateY(-5px)',
                    'boxShadow': '0 8px 25px rgba(0,0,0,0.12)'
                }
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'marginBottom': '20px',
                    'paddingBottom': '15px',
                    'borderBottom': f'1px solid {CORES["borda"]}'
                }, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                        html.I(className="fas fa-venus-mars", style={
                            'color': CORES['secundaria'],
                            'fontSize': '24px',
                            'marginRight': '12px'
                        }),
                        html.H3("Distribuição por Sexo", style={
                            'color': CORES['primaria'],
                            'margin': '0',
                            'fontSize': '20px',
                            'fontWeight': '600'
                        })
                    ]),
                    html.Div(style={
                        'backgroundColor': CORES['primaria'],
                        'color': CORES['terciaria'],
                        'padding': '5px 12px',
                        'borderRadius': '20px',
                        'fontSize': '12px',
                        'fontWeight': '500',
                        'letterSpacing': '0.5px'
                    }, children="DEMOGRAFIA")
                ]),
                dcc.Graph(
                    id='grafico-sexo',
                    config={'displayModeBar': False},
                    style={'flex': '1', 'height': '100%'}
                )
            ]),
            
            # Gráfico de Bairros
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '12px',
                'padding': '25px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["destaque"]}',
                'minHeight': '450px',
                'display': 'flex',
                'flexDirection': 'column',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'transform': 'translateY(-5px)',
                    'boxShadow': '0 8px 25px rgba(0,0,0,0.12)'
                }
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'marginBottom': '20px',
                    'paddingBottom': '15px',
                    'borderBottom': f'1px solid {CORES["borda"]}'
                }, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                        html.I(className="fas fa-map-marked-alt", style={
                            'color': CORES['destaque'],
                            'fontSize': '24px',
                            'marginRight': '12px'
                        }),
                        html.H3("Top Bairros", style={
                            'color': CORES['primaria'],
                            'margin': '0',
                            'fontSize': '20px',
                            'fontWeight': '600'
                        })
                    ]),
                    html.Div(style={
                        'backgroundColor': CORES['primaria'],
                        'color': CORES['terciaria'],
                        'padding': '5px 12px',
                        'borderRadius': '20px',
                        'fontSize': '12px',
                        'fontWeight': '500',
                        'letterSpacing': '0.5px'
                    }, children="GEOGRAFIA")
                ]),
                dcc.Graph(
                    id='grafico-bairros',
                    config={'displayModeBar': False},
                    style={'flex': '1', 'height': '100%'}
                )
            ]),
            
            # Gráfico de Itens
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '12px',
                'padding': '25px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["sucesso"]}',
                'minHeight': '450px',
                'display': 'flex',
                'flexDirection': 'column',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'transform': 'translateY(-5px)',
                    'boxShadow': '0 8px 25px rgba(0,0,0,0.12)'
                }
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'marginBottom': '20px',
                    'paddingBottom': '15px',
                    'borderBottom': f'1px solid {CORES["borda"]}'
                }, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                        html.I(className="fas fa-couch", style={
                            'color': CORES['sucesso'],
                            'fontSize': '24px',
                            'marginRight': '12px'
                        }),
                        html.H3("Itens Mais Higienizados", style={
                            'color': CORES['primaria'],
                            'margin': '0',
                            'fontSize': '20px',
                            'fontWeight': '600'
                        })
                    ]),
                    html.Div(style={
                        'backgroundColor': CORES['primaria'],
                        'color': CORES['terciaria'],
                        'padding': '5px 12px',
                        'borderRadius': '20px',
                        'fontSize': '12px',
                        'fontWeight': '500',
                        'letterSpacing': '0.5px'
                    }, children="PRODUTOS")
                ]),
                dcc.Graph(
                    id='grafico-itens',
                    config={'displayModeBar': False},
                    style={'flex': '1', 'height': '100%'}
                )
            ])
        ]),
        
        # Área Inferior (Tabela + Insights)
        html.Div(style={
            'display': 'grid',
            'gridTemplateColumns': 'minmax(0, 2fr) minmax(0, 1fr)',
            'gap': '25px',
            'marginBottom': '30px'
        }, children=[
            # Tabela de Dados (Premium)
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '12px',
                'padding': '25px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["primaria"]}'
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'justifyContent': 'space-between',
                    'alignItems': 'center',
                    'marginBottom': '20px',
                    'paddingBottom': '15px',
                    'borderBottom': f'1px solid {CORES["borda"]}'
                }, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center'}, children=[
                        html.I(className="fas fa-table", style={
                            'color': CORES['primaria'],
                            'fontSize': '24px',
                            'marginRight': '12px'
                        }),
                        html.H3("Dados dos Clientes", style={
                            'color': CORES['primaria'],
                            'margin': '0',
                            'fontSize': '20px',
                            'fontWeight': '600'
                        })
                    ]),
                    html.Div([
                        html.Span("Itens por página: ", style={
                            'marginRight': '10px',
                            'fontSize': '14px'
                        }),
                        dcc.Dropdown(
                            id='page-size',
                            options=[{'label': str(i), 'value': i} for i in [5, 10, 20]],
                            value=10,
                            clearable=False,
                            style={
                                'width': '80px',
                                'display': 'inline-block',
                                'fontFamily': "'Montserrat', sans-serif"
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
                        'borderRadius': '8px',
                        'border': f'1px solid {CORES["borda"]}'
                    },
                    style_header={
                        'backgroundColor': CORES['primaria'],
                        'color': CORES['terciaria'],
                        'fontWeight': 'bold',
                        'border': 'none',
                        'fontFamily': "'Montserrat', sans-serif"
                    },
                    style_cell={
                        'padding': '12px',
                        'textAlign': 'left',
                        'border': f'1px solid {CORES["borda"]}',
                        'maxWidth': '150px',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'fontFamily': "'Montserrat', sans-serif",
                        'fontSize': '14px'
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
            
            # Card de Insights (Premium)
            html.Div(style={
                'backgroundColor': CORES['terciaria'],
                'borderRadius': '12px',
                'padding': '25px',
                'boxShadow': '0 5px 15px rgba(0,0,0,0.08)',
                'borderTop': f'4px solid {CORES["secundaria"]}',
                'height': '500px',
                'display': 'flex',
                'flexDirection': 'column'
            }, children=[
                html.Div(style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'marginBottom': '20px',
                    'paddingBottom': '15px',
                    'borderBottom': f'1px solid {CORES["borda"]}'
                }, children=[
                    html.I(className="fas fa-lightbulb", style={
                        'color': CORES['secundaria'],
                        'fontSize': '24px',
                        'marginRight': '12px'
                    }),
                    html.H3("Insights Estratégicos", style={
                        'color': CORES['primaria'],
                        'margin': '0',
                        'fontSize': '20px',
                        'fontWeight': '600'
                    })
                ]),
                html.Div(
                    id='div-insights',
                    style={
                        'flex': '1',
                        'overflowY': 'auto',
                        'paddingRight': '10px'
                    }
                )
            ])
        ]),
        
        # Rodapé Profissional
        html.Footer(style={
            'textAlign': 'center',
            'padding': '20px',
            'backgroundColor': CORES['primaria'],
            'color': CORES['terciaria'],
            'marginTop': '40px',
            'fontSize': '14px'
        }, children=[
            html.Div(style={
                'maxWidth': '1200px',
                'margin': '0 auto',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center'
            }, children=[
                html.P("© 2025 Sofá Novo de Novo | Todos os direitos reservados"),
                html.Div(style={'display': 'flex'}, children=[
                    html.A("Termos de Uso", href="#", style={
                        'color': CORES['terciaria'],
                        'margin': '0 15px',
                        'textDecoration': 'none'
                    }),
                    html.A("Política de Privacidade", href="#", style={
                        'color': CORES['terciaria'],
                        'margin': '0 15px',
                        'textDecoration': 'none'
                    }),
                    
                ])
            ])
        ])
    ])
])

# =============================================
# CALLBACKS (mantidos iguais)
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
    
    if sexo != 'all':
        df_filtrado = df_filtrado[df_filtrado['sexo'] == sexo]
    if bairro != 'all':
        df_filtrado = df_filtrado[df_filtrado['bairro'] == bairro]
    
    # Gráfico de Sexo
    fig_sexo = px.pie(
        df_filtrado,
        names='sexo',
        color_discrete_sequence=[CORES['primaria'], CORES['secundaria']],
        hole=0.4
    )
    fig_sexo.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        plot_bgcolor=CORES['terciaria'],
        paper_bgcolor=CORES['terciaria'],
        font=dict(color=CORES['texto']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        )
    )
    
    # Gráfico de Bairros
    fig_bairros = px.bar(
        df_filtrado['bairro'].value_counts().reset_index(),
        x='count',
        y='bairro',
        orientation='h',
        color='count',
        color_continuous_scale=[CORES['fundo'], CORES['primaria']]
    )
    fig_bairros.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        coloraxis_showscale=False,
        margin=dict(l=100, r=20, t=20, b=20),
        plot_bgcolor=CORES['terciaria'],
        paper_bgcolor=CORES['terciaria'],
        font=dict(color=CORES['texto']),
        xaxis_title=None,
        yaxis_title=None
    )
    
    # Gráfico de Itens
    fig_itens = px.bar(
        df_filtrado['itens_higienizados'].value_counts().reset_index(),
        x='count',
        y='itens_higienizados',
        color='count',
        color_continuous_scale=[CORES['fundo'], CORES['secundaria']]
    )
    fig_itens.update_layout(
        xaxis_tickangle=-45,
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=20, b=80),
        plot_bgcolor=CORES['terciaria'],
        paper_bgcolor=CORES['terciaria'],
        font=dict(color=CORES['texto']),
        xaxis_title=None,
        yaxis_title=None
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
                'marginBottom': '15px',
                'padding': '15px',
                'backgroundColor': CORES['fundo'],
                'borderRadius': '8px',
                'borderLeft': f'4px solid {CORES["secundaria"]}',
                'listStyleType': 'none',
                'transition': 'all 0.3s ease',
                ':hover': {
                    'transform': 'translateX(5px)',
                    'boxShadow': '0 3px 10px rgba(0,0,0,0.05)'
                }
            }
        ) for insight in insights
    ])

# =============================================
# INICIALIZAÇÃO
# =============================================
if __name__ == '__main__':
    app.run(debug=True)
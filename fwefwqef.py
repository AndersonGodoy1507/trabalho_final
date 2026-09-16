
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestClassifier 
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

# ml

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


df=  pd.read_csv("diabetes2.csv")
if 'faixa_idade' not in df.columns:
        df['faixa_imc'] = pd.cut(
            df['imc'], 
            bins=[0, 18.5, 24.9, 29.9, 100], 
            labels=['Abaixo do Peso', 'Peso Normal', 'Sobrepeso', 'Obesidade']
        )
        df['faixa_idade'] = pd.cut(
            df['idade'], 
            bins=[0, 30, 50, 100], 
            labels=['Jovem (<30)', 'Adulto (30-50)', 'Idoso (>50)']
        )
# interface grafica

root = tk.Tk()
root.title('Risco de Diabetes')

root.state('zoomed') 
frame_controle = tk.Frame(root)
frame_controle.pack(side=tk.TOP, pady=10)

frame_resultados = tk.Frame(root)
frame_resultados.pack(side=tk.TOP, pady=10)
frame_grafico = tk.Frame(root)
frame_grafico.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


label_tendencia = tk.Label(frame_resultados, text='', justify=tk.CENTER, font=('Arial', 11, 'bold'))
label_tendencia.pack()

label_descricao = tk.Label(frame_resultados, text='', justify=tk.LEFT)
label_descricao.pack()

label_previsao = tk.Label(frame_resultados, text='', justify=tk.LEFT)
label_previsao.pack()





# limpando 
def limpar_frame():
    for widget in frame_grafico.winfo_children():
        widget.destroy()

    label_tendencia.config(text='')
    label_descricao.config(text='')
    label_previsao.config(text='')
    
    plt.close('all')

# funçoes de analise
def grafico_barra():
    limpar_frame()
    
    

    fig, ax = plt.subplots(figsize=(8, 5))
    risco_imc_idade = df.groupby(['faixa_idade', 'faixa_imc'], observed=False)['em_risco_diabetes'].mean() * 100
    risco_imc_idade.unstack().plot(kind='bar', ax=ax,grid=True)

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
        
    ax.set_title('Risco de Diabetes por Faixa Etária e IMC')
    ax.set_ylabel('Porcentagem em Risco (%)')
    ax.set_xlabel('Faixa Etária')
    ax.legend(title='Faixa de IMC')
    plt.xticks(rotation=0)
    insight = 'Conforme aumenta a idade, ser obeso aumenta significativamente a chance de diabetes.'
    label_tendencia.config(text=insight)



def mostrar_linhas1():
    limpar_frame()
    fig, ax =  plt.subplots(figsize = (8,5))
    media_risco_fumantes   =   df[df['fumante'] == 1].groupby('idade')['em_risco_diabetes'].mean() *100
    media_risco_naofumante = df[df['fumante'] == 0].groupby('idade')['em_risco_diabetes'].mean()* 100
    media_risco_fumantes.plot(kind  = 'line', color = 'red', ax=ax,label ='Fumante')
    media_risco_naofumante.plot(kind  = 'line', color = 'blue',ax=ax,label='Não Fumante')
    
    
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
    
    ax.set_title('Risco diabete idade + tabagismo')
    ax.set_ylabel('Taxa de risco %')
    ax.set_xlabel('Idade')
    ax.legend(labels = ['Tabagista', 'Não tabagista'])
    
    insight =  'Tabagistas tem maior risco de diabetes em todas as idades, e risco maior após os 50 anos'        
    label_tendencia.config(text= insight)      
    
    
def mostrar_linhas2():
    limpar_frame()
    fig, ax =  plt.subplots(figsize = (8,5))
    media_imc_atividade = df.groupby(['faixa_idade', 'nivel_atividade_fisica'], observed=False)['imc'].mean()
    media_risco_idade = df.groupby('faixa_idade')['em_risco_diabetes'].mean() * 100
    eixo2= ax.twinx()
    media_imc_atividade.unstack().plot(kind='line', ax=ax, grid=True, marker='o',
    color={'alto': 'green', 'moderado': 'yellow', 'baixo': 'red'})
    
   
    media_risco_idade.plot(kind='line', ax=eixo2, color='black', linestyle='--', marker='x', label='Risco (%)')
    
    
    
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
    
    ax.set_title('Atividade Fisica X IMC')
    ax.set_ylabel('IMC')
    ax.set_xlabel('Idade')
    eixo2.set_ylabel('Risco de Diabetes (%)')
    
    insight =  '''O nivel de imc por idade enquanto joven varia pouco mesmo com pouca atividade fisica moderada,
    passano a mudar após os 30 anos quando a atividade fisica se torna essencial e por fim mostrando que após os 50 anos
    o risco sobe mesmo mantendo uma atividade fisica boa.
    '''        
    label_tendencia.config(text= insight)   
    
def mostrar_pizza():
    limpar_frame()
    fig, ax = plt.subplots(figsize=(8, 5))
    historico_pizza = df['historico_familiar'].value_counts()
    historico_pizza.index = ['Com Histórico', 'Sem Histórico']
    historico_pizza.plot(
        kind='pie', 
        ax=ax, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#66b3ff', '#ff9999']
    )
    
    ax.set_aspect('equal')
    ax.set_title('Proporção de Histórico Familiar de Diabetes')
    ax.set_ylabel('')
    
    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
    
    insight = 'O gráfico mostra que pessoas com diabetes na família aumentam as chances de se ter diabetes.'
    label_tendencia.config(text=insight)
    
    


# botao

btn_barras = ttk.Button(frame_controle, text='Grafico de barras', command=grafico_barra)
btn_barras.grid(row=0, column=0, padx=5, pady=5)

btn_linhas1 = ttk.Button(frame_controle, text='Grafico de linhas 1', command=mostrar_linhas1)
btn_linhas1.grid(row=1, column=0, padx=5, pady=5)

btn_linhas2 = ttk.Button(frame_controle, text='Grafico de linhas 2', command=mostrar_linhas2)
btn_linhas2.grid(row=2, column=0, padx=5, pady=5)

btn_pizza = ttk.Button(frame_controle, text='Grafico de Pizza', command=mostrar_pizza)
btn_pizza.grid(row=3, column=0, padx=5, pady=5)

# btn_tendecia  = ttk.Button(frame_controle, text= 'Medida de tendência', command=mostrar_tendencia)
# btn_tendecia.grid(row = 3, padx= 5, pady=5)

# btn_descricao = ttk.Button(frame_controle, text= 'Descrição', command=descricao)
# btn_descricao.grid(row = 4, padx= 5, pady=5)

# btn_previsao  = ttk.Button(frame_controle, text= 'Previsão', command=previsao)
# btn_previsao.grid(row = 5, padx= 5, pady=5)










root.mainloop()

Conclusão 

Primeiro deixar que usai o gemini do google para ajeitar a interface grafica e tão somente para isso. De resto usei quando precisei entender a logica sem pedir a resposta diretamente. 

 

Sobre os gráficos: 

O primeiro gráfico mostra os índices de risco por faixa etária e imc. 

Para essa parte mudei as colunas com  a condicional a seguir: 

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

Tentei outros métodos, porém o gráfico pegava idade por idade deixando impossível a leitura. 

Esse gráfico mostra que conforme a idade aumenta o risco de diabetes aumenta se o paciente for obeso. 

 

O primeiro gráfico de linhas mostra o seguinte: 

Que o tabagismo é um fator de aumento de risco para o acometimento do diabetes, inclusive aumenta com a idade. 

O segundo gráfico de linhas mostra que: 

A linha verde que mostra muita atividade física, está dizendo que, o imc de quem faz atividade perto dos 30 anos diminui drasticamente e volta a subir quando se fica idoso, o amarelo está dizendo que o imc de quem se exercita de vez em quando cai próximo aos 30 e sobe também e o vermelho mostra que quem não faz atividade mantem a média a vida toda subindo quando se fica idoso aumentando drasticamente o risco de diabetes. 

E a linha pontilhada mostra que mesmo mantendo o imc baixo o risco de diabetes aumente conforme se fica mais idoso, aumentando assim a necessidade de cuidados para além do imc. 

 

O gráfico de pizza por sua vez mostra que o fator genético influi de forma grande, porém não definitiva para o risco de diabetes. 

 

Em resumo o que a análise mostra é que a diabetes é uma doença multifatorial e que ter uma boa relação entre alimentação, atividades físicas e cuidados de saúde preventiva reduzem as chances de se contrair tal doença. 

 
import streamlit as st
import numpy as np
import pandas as pd
import time
# necessario rodar o comando a baixo no terminal:
# streamlit run R:\EVANDRO\Python\Pietro\Streamlit\streamlit0.py

st.title('Aqui fica o título')
st.write('e aqui o subtítulo')
"""
# da pra fazer o titulo por aqui tb
e o sub por aqui:
"""

#para conseguir formatar minimamente o texto precisa da maracutaia do markdown, a sintaxe é do CSS
text1 = "string com o conteúdo do markdown abaixo. O ideal é ter um relatório pronto e só precisar editar o texto dessa string"

st.markdown("<h4 style='text-align: justify; color: goldenrod;'> título dourado </h4>", unsafe_allow_html=True) #texto em justificar
st.markdown("<p style='text-align: justify; color: black;'> " + str(text1) + " </p>", unsafe_allow_html=True) #precisa desse unsafe_allow_html=True

df = pd.DataFrame({
  'col1': [1, 2, 3, 4],
  'col2': [5, 6, 7, 8]
})


#muito facil exibir dataframes:
df

## plotar grafico (sem bokeh)
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

## mapa de dados (n sei se pode ser util)
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

## checkbox para esconder qualquer coisa

if st.checkbox('Mostrar'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    st.line_chart(chart_data)
    
    
    
    
option2 = st.selectbox(
    'Which number do you like best?',
      df['col2'])

'You selected: ', option2





#barra lateral
option = st.sidebar.selectbox( #isso aqui fica na lateral
    'Which number do you like best?',
     df['col1'])

'You selected (side):', option #isso aqui no corpo da página, pode ser util para fazer várias paginas, alternadas pela lateral




left_column, right_column = st.beta_columns(2)

#outra opçao de ocultar
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

#mais uma opçao de ocultar
expander = st.beta_expander("FAQ")
expander.write("essa eu acho a melhor opção para ocultar textos longos, mas tava tendo aquele bug dos gráficos que falei")


expander.markdown("<h1 style='text-align: justify; color: goldenrod;'> Da pra colocar qlqr coisa no expander </h1>", unsafe_allow_html=True)


st.title('Plotando com bokeh e funçao graph')
path_bokeh = "R:\\EVANDRO\\Python\\Pietro\\"
import sys
sys.path.append(path_bokeh)
from graph import graph

df = pd.read_excel ("R:/EVANDRO/Python/Pietro/" + "dados3.xlsx", sheet_name="Sheet1", header=0)
df = df.set_index("datas")
a = graph(df,par=True, style=["bb", "bb"])
a.plot()

st.bokeh_chart(a.pic, use_container_width=True)




## barra de progresso, me parece um pouco inútil

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'


#plotar com bokeh,sem chamar a função graph
from bokeh.plotting import figure, output_file, show

# output to static HTML file
output_file("line.html")
p = figure(plot_width=400, plot_height=400)

# add a circle renderer with a size, color, and alpha
p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

#essa é a funçao q integra o bokeh ao streamlit, basta colocar a figure como parametro
st.bokeh_chart(p, use_container_width=True)





#plotando uma img
from PIL import Image
st.image(Image.open('C:\\Users\\evandro.manso.TAVOLA\\Pictures\\logo.png'))
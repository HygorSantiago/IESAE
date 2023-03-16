#!streamlit run live_streamlit2.py

import streamlit as st
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

st.title('Diagnóstico de falha em torno mecânico')

df = pd.read_csv('predictive_maintenance.csv')
df = df.drop(columns=['UDI','Product ID','Type'])
df['Failure Type'] = df['Failure Type'].replace({'No Failure':'Sem falha',
                                                 'Heat Dissipation Failure':'Falha de dissipação de calor',
                                                 'Power Failure':'Falha de potência',
                                                 'Overstrain Failure':'Sobrecarga',
                                                 'Random Failures':'Falha aleatória',
                                                 'Tool Wear Failure':'Falha por desgaste'})
x = df.drop(columns=['Failure Type','Target'])
y = df['Failure Type']

modelo = DecisionTreeClassifier()
modelo.fit(x,y)

# Criar formulário para receber os dados de entrada
temp_ar = st.slider('Temperatura do ar [K]', min_value=290., max_value=320., step=0.1)
temp_pro = st.slider('Temperatura do processo [K]', min_value=290., max_value=320., step=0.1)
velocidade = st.slider('Velocidade de rotação [rpm]', min_value=1000.0, max_value=3000., step=0.1)
torque = st.slider('Torque [Nm]', min_value=1., max_value=80., step=0.1)
desgaste = st.slider('Desgaste [mm]', min_value=0., max_value=280., step=0.1)


if st.button('Prever'):
    # Fazer previsão com o modelo carregado
    input_data = [[temp_ar, temp_pro, velocidade, torque, desgaste]]
    prediction = modelo.predict(input_data)[0]
    
    # Exibir resultado da previsão
    st.write('O diagnóstico é: ', prediction)
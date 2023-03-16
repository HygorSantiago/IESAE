#!streamlit run live_streamlit.py

import streamlit as st
import pickle

st.title('Diagnóstico de falha em torno mecânico')

filename = 'modelo_treinado_live'

with open(filename, 'rb') as file:
    modelo = pickle.load(file)
    
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
    
    if prediction == 'No Failure':
        prediction = 'Sem falha'
    if prediction == 'Heat Dissipation Failure':
        prediction = 'Falha de dissipação de calor'
    if prediction == 'Power Failure':
        prediction = 'Falha de potência'
    if prediction == 'Overstrain Failure':
        prediction = 'Sobrecarga'
    if prediction == 'Random Failures':
        prediction = 'Falha aleatória'
    if prediction == 'Tool Wear Failure':
        prediction = 'Falha por desgaste'

    
    # Exibir resultado da previsão
    st.write('O diagnóstico é: ', prediction)
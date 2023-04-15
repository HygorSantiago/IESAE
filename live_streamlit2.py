#!streamlit run live_streamlit2.py

import streamlit as st

import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

from docxtpl import DocxTemplate

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

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

x_treino,x_teste,y_treino,y_teste = train_test_split(x,y,test_size=0.3)

modelo = DecisionTreeClassifier()
modelo.fit(x_treino,y_treino)

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
    
if st.button('Relatório'):
    
    nome = 'Hygor'

    acuracia = modelo.score(x_teste,y_teste)

    input_data = [[temp_ar, temp_pro, velocidade, torque, desgaste]]
    
    previsao = modelo.predict(input_data)
    previsao = previsao[0]
    
    context = {'nome':nome,
               'temperatura_ar':round(temp_ar-273.15,2),
               'temperatura_processo':round(temp_pro-273.15,2),
               'velocidade':velocidade,
               'torque':torque,
               'desgaste':desgaste,
               'acuracia':round(100*acuracia,2),
               'previsao':previsao}
    
    doc = DocxTemplate('texto_base.docx')
    doc.render(context)
    doc.save('relatorio.docx')
    
    texto = f'''
    {nome}, segue seu relatório.
    '''
    texto = MIMEText(texto, 'plain')
    
    msg = MIMEMultipart()

    msg['Subject'] = 'Relatório Trilha dos Dados'
    msg['From'] = 'hsantiagolara@gmail.com'
    msg['To'] = 'hsantiagolara@gmail.com'
    password = 'nghmccbclqdpzsro'

    msg.attach(texto)
    
    caminho_anexo = 'relatorio.docx'

    with open(caminho_anexo, 'rb') as f:
        anexo = MIMEBase('application', 'octet-stream')
        anexo.set_payload(f.read())
    
    encoders.encode_base64(anexo)
    
    anexo.add_header('Content-Disposition',f'attachment; filename={caminho_anexo}')

    msg.attach(anexo)
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()

    server.login(msg['From'],password)

    server.sendmail(msg['From'],msg['To'],msg.as_string().encode('utf-8'))

    server.quit()

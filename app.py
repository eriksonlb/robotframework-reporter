from flask import Flask, render_template
import json
import plotly.graph_objs as go
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    with open('data.json', 'r') as f:
        dados_teste = json.load(f)['testes']

    # Contar os sucessos e falhas
    sucesso = sum(teste['status'] == 'PASS' for teste in dados_teste)
    falha = sum(teste['status'] == 'FAILED' for teste in dados_teste)

    # Agrupar os testes pelo erro e contar a quantidade de ocorrências
    erros = {}
    for teste in dados_teste:
        erro = teste['error']
        if erro:
            if erro in erros:
                erros[erro] += 1
            else:
                erros[erro] = 1

    # Criar o gráfico de pizza
    labels = ['Pass', 'Failed']
    values = [sucesso, falha]
    pie_chart = go.Figure(data = go.Pie(labels=labels, values=values))

    # Transformar os erros em pares (erro, quantidade) para o gráfico de pizza
    erros_labels = list(erros.keys())
    erros_values = list(erros.values())
    erros_chart = go.Figure(data = go.Pie(labels=erros_labels, values=erros_values))

    # Converter o gráfico de pizza para JSON
    pie_chart_json = pie_chart.to_json()
    erros_chart_json = erros_chart.to_json()

    return render_template('index.html', pie_chart_json=pie_chart_json, erros_chart_json=erros_chart_json, erros=erros, sucesso=sucesso, falha=falha, dados_teste=dados_teste)

if __name__ == '__main__':
    app.run(debug=True)

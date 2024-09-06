from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from datetime import timedelta, datetime

app = Flask(__name__)
app.secret_key = 'secret_key'

# Simulação de banco de dados
usuarios = []
passagens_vendidas = 0
admin_password = "admin"
vendas = []  # Lista que armazenará todas as vendas

# Estrutura do Usuário
class Usuario:
    def __init__(self, nome, email, senha, cpf, cep, rua, cidade, bairro):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.endereco = {
            'cep': cep,
            'rua': rua,
            'cidade': cidade,
            'bairro': bairro
        }

# Simulação de viagens e horários
rotas = {
    "Vitória -> Linhares": {"preco": 78.05, "tempo_viagem": timedelta(hours=2, minutes=30), "atraso": timedelta(hours=4)},
    "Vitória -> Jaguaré": {"preco": 113.88, "tempo_viagem": timedelta(hours=3, minutes=45), "atraso": timedelta()},
    "Vitória -> São Mateus": {"preco": 123.49, "tempo_viagem": timedelta(hours=4, minutes=30), "atraso": timedelta()}
}

# Página inicial de login
@app.route('/')
def index():
    return render_template('index.html')

# Página de cadastro de novo usuário
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Página de recuperação de senha
@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

# Página de compra de passagem
@app.route('/menu-viagens')
def menu_viagens():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    # Exibe o nome e CPF do usuário logado
    usuario = next(u for u in usuarios if u.email == session['usuario'])
    
    return render_template('menu_viagens.html', usuario=usuario, rotas=rotas)

# Rota para realizar a compra de passagem
@app.route('/comprar', methods=['POST'])
def comprar_passagem():
    try:
        rota = request.form['rota']
        horario_embarque = request.form['horario_embarque']  # Recebe o horário no formato HH:MM
        data_viagem = request.form['data_viagem']  # Recebe a data da viagem no formato YYYY-MM-DD

        # Verifica se uma rota foi escolhida
        if rota == "":
            return jsonify(success=False, message="Por favor, selecione uma rota.")

        # Divide a string HH:MM em horas e minutos
        horas_embarque, minutos_embarque = map(int, horario_embarque.split(':'))

        global passagens_vendidas
        passagens_vendidas += 1

        # Calcula horários
        embarque = timedelta(hours=horas_embarque, minutes=minutos_embarque)
        tempo_viagem = rotas[rota]["tempo_viagem"]
        atraso = rotas[rota]["atraso"]
        
        # Se a rota for "Vitória -> Linhares", adiciona o atraso de 4 horas
        if rota == "Vitória -> Linhares":
            embarque += atraso  # Adiciona o atraso ao horário de embarque

        chegada = embarque + tempo_viagem

        # Recupera o nome e CPF do usuário logado
        usuario_logado = next(u for u in usuarios if u.email == session['usuario'])

        # Salvar detalhes da venda no relatório de vendas
        venda = {
            "nome": usuario_logado.nome,
            "cpf": usuario_logado.cpf,
            "rota": rota,
            "data_compra": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Data e hora da compra
            "data_viagem": data_viagem,  # Data da viagem
            "horario_embarque": f"{horas_embarque:02d}:{minutos_embarque:02d}",
            "horario_chegada": str(chegada),
            "preco": rotas[rota]["preco"]
        }
        vendas.append(venda)  # Armazena a venda

        # Simula a compra e gera o ticket
        return jsonify(
            success=True,
            message="Compra realizada com sucesso!",
            empresa="ABK Bus Lines",
            nome=usuario_logado.nome,
            cpf=usuario_logado.cpf,
            horario_embarque=f"{horas_embarque:02d}:{minutos_embarque:02d}",
            tempo_viagem=str(tempo_viagem),
            horario_chegada=str(chegada),
            preco=rotas[rota]["preco"],
            atraso=str(atraso)
        )
    except Exception as e:
        # Exibe erro detalhado no terminal Flask e retorna mensagem de erro ao cliente
        print(f"Erro ao processar a compra: {e}")
        return jsonify(success=False, message="Erro ao processar a compra.")

# Página principal do menu
@app.route('/menu-principal')
def menu_principal():
    if 'usuario' not in session:
        return redirect(url_for('index'))
    
    usuario = next(u for u in usuarios if u.email == session['usuario'])
    return render_template('menu_principal.html', usuario=usuario)

# Rota para registrar um novo usuário
@app.route('/register', methods=['POST'])
def register():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    confirmar_senha = request.form['confirmar_senha']
    cpf = request.form['cpf']
    cep = request.form['cep']
    rua = request.form['rua']
    cidade = request.form['cidade']
    bairro = request.form['bairro']

    if senha != confirmar_senha:
        return jsonify(success=False, message="As senhas não coincidem.")
    
    if len(cpf) != 11:
        return jsonify(success=False, message="CPF deve ter 11 dígitos.")
    
    novo_usuario = Usuario(nome, email, senha, cpf, cep, rua, cidade, bairro)
    usuarios.append(novo_usuario)
    
    # Após o cadastro, retornar o redirecionamento para o login
    return jsonify(success=True, message="Usuário registrado com sucesso!", redirect=url_for('index'))

# Página de login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    # Verifica se o administrador está logando
    if email == 'admin@admin.com' and senha == admin_password:
        session['admin'] = True
        return redirect(url_for('admin_dashboard'))

    # Verifica se o usuário está logado
    for usuario in usuarios:
        if usuario.email == email and usuario.senha == senha:
            session['usuario'] = usuario.email
            return redirect(url_for('menu_principal'))
    
    return jsonify(success=False, message="Usuário ou senha inválidos!")

# Rota para o painel do administrador
@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('index'))
    
    return render_template('admin.html', passagens_vendidas=passagens_vendidas)

# Rota para relatório de vendas do administrador
@app.route('/admin/relatorio-vendas')
def relatorio_vendas():
    if 'admin' not in session:
        return redirect(url_for('index'))
    
    return render_template('relatorio_vendas.html', vendas=vendas)

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

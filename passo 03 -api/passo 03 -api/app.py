
from flask import Flask, request, redirect, url_for, render_template_string, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "cadastro_usuarios_2026"

# Banco de dados
def conectar():
    conexao = sqlite3.connect("usuarios.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    banco = conectar()
    banco.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT
        )
    """)
    banco.commit()
    banco.close()


# Interface HTML integrada ao Python
HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Users | Gerenciamento</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', sans-serif;
}

body {
    background: #090e1a;
    color: #e8edf7;
    min-height: 100vh;
}

header {
    padding: 25px 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #202b40;
    background: #0d1424;
}

.logo {
    font-size: 23px;
    font-weight: bold;
    color: #60a5fa;
}

.logo span {
    color: white;
}

.status {
    color: #4ade80;
    font-size: 13px;
}

.container {
    max-width: 1150px;
    margin: 45px auto;
    padding: 0 20px;
}

.intro {
    margin-bottom: 35px;
}

.intro h1 {
    font-size: 32px;
    margin-bottom: 10px;
}

.intro p {
    color: #8493aa;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin-bottom: 30px;
}

.card {
    background: #111c30;
    border: 1px solid #24324a;
    padding: 23px;
    border-radius: 13px;
}

.card small {
    color: #91a1ba;
}

.card h2 {
    font-size: 29px;
    margin-top: 12px;
    color: #60a5fa;
}

.content {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 22px;
}

.panel {
    background: #111c30;
    border: 1px solid #24324a;
    padding: 25px;
    border-radius: 13px;
}

.panel h2 {
    font-size: 19px;
    margin-bottom: 23px;
}

label {
    display: block;
    color: #aab8ce;
    font-size: 13px;
    margin-bottom: 8px;
}

input {
    width: 100%;
    background: #0a1323;
    border: 1px solid #293b57;
    color: white;
    padding: 13px;
    border-radius: 8px;
    outline: none;
    margin-bottom: 18px;
}

input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px #3b82f622;
}

button {
    border: none;
    padding: 13px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: .2s;
}

.add {
    width: 100%;
    background: #2563eb;
    color: white;
}

.add:hover {
    background: #3b82f6;
}

.search {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
}

.search input {
    margin: 0;
}

.search button {
    background: #263b5c;
    color: white;
}

table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

th {
    color: #8294af;
    font-size: 12px;
    text-transform: uppercase;
}

th, td {
    padding: 15px 10px;
    border-bottom: 1px solid #26344b;
    font-size: 13px;
}

td {
    color: #d5deed;
}

.delete {
    color: #f87171;
    background: #451d2a;
    padding: 8px 11px;
}

.delete:hover {
    background: #702b3d;
}

.flash {
    background: #183b35;
    border: 1px solid #276b55;
    color: #86efac;
    padding: 13px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.empty {
    color: #8190a8;
    text-align: center;
    padding: 35px;
}

@media(max-width: 850px) {
    .content {
        grid-template-columns: 1fr;
    }

    .cards {
        grid-template-columns: 1fr;
    }

    .panel {
        overflow-x: auto;
    }

    header {
        padding: 20px;
    }

    .intro h1 {
        font-size: 26px;
    }
}
</style>
</head>

<body>

<header>
    <div class="logo">USER<span>MANAGER.</span></div>
    <div class="status">● Sistema online</div>
</header>

<div class="container">

    <div class="intro">
        <h1>Gerenciamento de usuários</h1>
        <p>Cadastre, consulte e gerencie seus usuários em um só lugar.</p>
    </div>

    {% for mensagem in get_flashed_messages() %}
        <div class="flash">{{ mensagem }}</div>
    {% endfor %}

    <div class="cards">
        <div class="card">
            <small>Total de usuários</small>
            <h2>{{ total }}</h2>
        </div>

        <div class="card">
            <small>Resultados encontrados</small>
            <h2>{{ usuarios|length }}</h2>
        </div>

        <div class="card">
            <small>Status do sistema</small>
            <h2 style="color:#4ade80">Ativo</h2>
        </div>
    </div>

    <div class="content">

        <div class="panel">
            <h2>+ Novo usuário</h2>

            <form action="/cadastrar" method="POST">

                <label>Nome completo</label>
                <input type="text" name="nome"
                       placeholder="Digite o nome"
                       maxlength="100" required>

                <label>E-mail</label>
                <input type="email" name="email"
                       placeholder="exemplo@email.com"
                       maxlength="150" required>

                <label>Telefone</label>
                <input type="tel" name="telefone"
                       placeholder="(00) 00000-0000"
                       maxlength="20">

                <button class="add" type="submit">
                    Cadastrar usuário
                </button>

            </form>
        </div>

        <div class="panel">
            <h2>Usuários cadastrados</h2>

            <form class="search" action="/" method="GET">
                <input type="text" name="busca"
                       placeholder="Pesquisar nome ou e-mail..."
                       value="{{ busca }}">
                <button type="submit">Buscar</button>
            </form>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>E-mail</th>
                        <th>Telefone</th>
                        <th>Ação</th>
                    </tr>
                </thead>

                <tbody>
                    {% for usuario in usuarios %}
                    <tr>
                        <td>#{{ usuario.id }}</td>
                        <td>{{ usuario.nome }}</td>
                        <td>{{ usuario.email }}</td>
                        <td>{{ usuario.telefone or '-' }}</td>
                        <td>
                            <form action="/excluir/{{ usuario.id }}"
                                  method="POST"
                                  onsubmit="return confirm('Deseja excluir este usuário?')">
                                <button class="delete" type="submit">
                                    Excluir
                                </button>
                            </form>
                        </td>
                    </tr>
                    {% else %}
                    <tr>
                        <td colspan="5" class="empty">
                            Nenhum usuário encontrado.
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>

        </div>
    </div>
</div>

</body>
</html>
"""


# Página principal e consulta
@app.route("/")
def inicio():
    busca = request.args.get("busca", "").strip()

    banco = conectar()

    if busca:
        usuarios = banco.execute("""
            SELECT * FROM usuarios
            WHERE nome LIKE ? OR email LIKE ?
            ORDER BY id DESC
        """, (f"%{busca}%", f"%{busca}%")).fetchall()
    else:
        usuarios = banco.execute("""
            SELECT * FROM usuarios ORDER BY id DESC
        """).fetchall()

    total = banco.execute(
        "SELECT COUNT(*) FROM usuarios"
    ).fetchone()[0]

    banco.close()

    return render_template_string(
        HTML,
        usuarios=usuarios,
        total=total,
        busca=busca
    )


# Cadastro
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip().lower()
    telefone = request.form.get("telefone", "").strip()

    if not nome or not email:
        flash("Preencha os campos obrigatórios.")
        return redirect(url_for("inicio"))

    banco = conectar()

    try:
        banco.execute("""
            INSERT INTO usuarios (nome, email, telefone)
            VALUES (?, ?, ?)
        """, (nome, email, telefone))

        banco.commit()
        flash("Usuário cadastrado com sucesso!")

    except sqlite3.IntegrityError:
        flash("Este e-mail já está cadastrado.")

    finally:
        banco.close()

    return redirect(url_for("inicio"))


# Exclusão
@app.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    banco = conectar()

    banco.execute(
        "DELETE FROM usuarios WHERE id = ?", (id,)
    )

    banco.commit()
    banco.close()

    flash("Usuário excluído com sucesso!")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    criar_tabela()
    app.run(debug=True)

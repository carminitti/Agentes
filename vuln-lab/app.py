"""
NexBank - Aplicação intencionalmente vulnerável para treinamento de pentest.
NÃO use em produção. Contém vulnerabilidades OWASP Top 10 propositais.
"""

from flask import Flask, request, session, render_template, redirect, jsonify, make_response
import sqlite3
import hashlib
import urllib.request
import os
import json
import re

app = Flask(__name__)
app.secret_key = 'secret'          # A02 — chave fraca
app.debug = True                   # A05 — debug mode ativo
DATABASE = 'nexbank.db'


# ─── Helpers ──────────────────────────────────────────────────────────────────

def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def current_user():
    if 'user_id' not in session:
        return None
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return user


# ─── Init DB ──────────────────────────────────────────────────────────────────

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email    TEXT,
        role     TEXT DEFAULT 'user',
        balance  REAL DEFAULT 1000.0,
        ssn      TEXT,
        sec_ans  TEXT,
        bio      TEXT DEFAULT ''
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id     INTEGER,
        recipient   TEXT,
        amount      REAL,
        description TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id    INTEGER,
        content    TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    seed_users = [
        ('admin',  md5('admin123'), 'admin@nexbank.com',  'admin', 99999.0, '000-00-0001', 'blue'),
        ('alice',  md5('password'), 'alice@email.com',    'user',   5420.5, '123-45-6789', 'red'),
        ('bob',    md5('123456'),   'bob@email.com',      'user',   2150.75,'987-65-4321', 'green'),
        ('carlos', md5('abc123'),   'carlos@email.com',   'user',    875.0, '555-12-3456', 'yellow'),
    ]
    for u in seed_users:
        try:
            c.execute(
                'INSERT INTO users (username,password,email,role,balance,ssn,sec_ans) VALUES (?,?,?,?,?,?,?)', u)
        except Exception:
            pass

    seed_tx = [
        (2, 'bob',    1500.0, 'Salário de março'),
        (2, 'carlos',  200.0, 'Aluguel'),
        (3, 'alice',   350.0, 'Freelance — design'),
        (3, 'admin',    50.0, 'Taxa de serviço'),
        (4, 'alice',   100.0, 'Pagamento parcial'),
        (1, 'alice',  5000.0, 'Bônus executivo'),
    ]
    for t in seed_tx:
        try:
            c.execute(
                'INSERT INTO transactions (user_id,recipient,amount,description) VALUES (?,?,?,?)', t)
        except Exception:
            pass

    conn.commit()
    conn.close()


# ─── Auth Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        conn = get_db()
        # ⚠ A03 — SQL Injection no campo username
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{md5(password)}'"
        try:
            user = conn.execute(query).fetchone()
        except Exception as e:
            conn.close()
            return render_template('login.html', error=f'DB error: {e}')   # A05 — erro verboso
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect('/dashboard')
        error = 'Usuário ou senha inválidos.'
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        email    = request.form.get('email', '')
        sec_ans  = request.form.get('sec_ans', '')
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (username,password,email,sec_ans) VALUES (?,?,?,?)',
                (username, md5(password), email, sec_ans))
            conn.commit()
            conn.close()
            return redirect('/login')
        except Exception:
            conn.close()
            error = 'Usuário já existe.'
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    user = current_user()
    if not user:
        return redirect('/login')
    conn = get_db()
    txs = conn.execute(
        'SELECT * FROM transactions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5',
        (user['id'],)).fetchall()
    msgs = conn.execute(
        'SELECT m.*, u.username FROM messages m JOIN users u ON m.user_id=u.id ORDER BY m.created_at DESC LIMIT 10'
    ).fetchall()
    conn.close()
    return render_template('dashboard.html', user=user, transactions=txs, messages=msgs)


# ─── Perfil ───────────────────────────────────────────────────────────────────

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    # ⚠ A01 — IDOR: qualquer usuário autenticado acessa qualquer perfil
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if not user:
        return 'Usuário não encontrado', 404
    return render_template('profile.html', user=user)


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')
    me = current_user()
    if request.method == 'POST':
        bio = request.form.get('bio', '')
        # ⚠ A03 — XSS Armazenado: bio salva sem sanitização
        conn = get_db()
        conn.execute('UPDATE users SET bio=? WHERE id=?', (bio, session['user_id']))
        conn.commit()
        conn.close()
        return redirect(f'/profile/{session["user_id"]}')
    return render_template('edit_profile.html', user=me)


# ─── Transações ───────────────────────────────────────────────────────────────

@app.route('/transactions')
def transactions():
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    txs = conn.execute(
        'SELECT * FROM transactions WHERE user_id=? ORDER BY created_at DESC',
        (session['user_id'],)).fetchall()
    conn.close()
    return render_template('transactions.html', transactions=txs)


@app.route('/transaction/<int:tx_id>')
def transaction_detail(tx_id):
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    # ⚠ A01 — IDOR: sem verificar se tx pertence ao usuário logado
    tx = conn.execute('SELECT * FROM transactions WHERE id=?', (tx_id,)).fetchone()
    conn.close()
    if not tx:
        return 'Transação não encontrada', 404
    return render_template('transaction_detail.html', tx=tx)


@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect('/login')
    q = request.args.get('q', '')
    results = []
    if q:
        conn = get_db()
        # ⚠ A03 — SQL Injection na busca
        query = f"SELECT * FROM transactions WHERE description LIKE '%{q}%'"
        try:
            results = conn.execute(query).fetchall()
        except Exception as e:
            conn.close()
            return render_template('search.html', q=q, results=[], error=str(e))
        conn.close()
    # ⚠ A03 — XSS Refletido: q renderizado sem escape no template
    return render_template('search.html', q=q, results=results)


# ─── Transferência ────────────────────────────────────────────────────────────

@app.route('/transfer', methods=['GET', 'POST'])
def transfer_page():
    if 'user_id' not in session:
        return redirect('/login')
    me = current_user()
    msg = None
    if request.method == 'POST':
        recipient = request.form.get('recipient', '')
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            amount = 0
        desc = request.form.get('description', 'Transferência')

        conn = get_db()
        dest = conn.execute('SELECT * FROM users WHERE username=?', (recipient,)).fetchone()
        if not dest:
            msg = ('error', 'Destinatário não encontrado.')
        elif amount <= 0:
            msg = ('error', 'Valor inválido.')
        elif me['balance'] < amount:
            msg = ('error', 'Saldo insuficiente.')
        else:
            # ⚠ A01/A04 — sem CSRF token
            conn.execute('UPDATE users SET balance=balance-? WHERE id=?', (amount, session['user_id']))
            conn.execute('UPDATE users SET balance=balance+? WHERE id=?', (amount, dest['id']))
            conn.execute(
                'INSERT INTO transactions (user_id,recipient,amount,description) VALUES (?,?,?,?)',
                (session['user_id'], recipient, amount, desc))
            conn.commit()
            msg = ('success', f'R$ {amount:.2f} transferido para {recipient}.')
            me = current_user()
        conn.close()
    return render_template('transfer.html', user=me, msg=msg)


# ─── Mural de mensagens (XSS armazenado público) ──────────────────────────────

@app.route('/board', methods=['GET', 'POST'])
def board():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        content = request.form.get('content', '')
        # ⚠ A03 — XSS Armazenado no mural público
        conn = get_db()
        conn.execute('INSERT INTO messages (user_id,content) VALUES (?,?)', (session['user_id'], content))
        conn.commit()
        conn.close()
        return redirect('/board')
    conn = get_db()
    msgs = conn.execute(
        'SELECT m.*, u.username FROM messages m JOIN users u ON m.user_id=u.id ORDER BY m.created_at DESC'
    ).fetchall()
    conn.close()
    return render_template('board.html', messages=msgs)


# ─── Admin ────────────────────────────────────────────────────────────────────

@app.route('/admin')
def admin():
    # ⚠ A01 — sem verificar role; qualquer usuário logado acessa
    if 'user_id' not in session:
        return redirect('/login')
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    txs   = conn.execute('SELECT * FROM transactions ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', users=users, transactions=txs)


# ─── API Endpoints ────────────────────────────────────────────────────────────

@app.route('/api/users/<int:uid>')
def api_user(uid):
    # ⚠ A01 — IDOR na API: sem autenticação nem autorização
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'not found'}), 404
    # ⚠ A02 — retorna dados sensíveis (ssn, password hash, balance)
    return jsonify(dict(user))


@app.route('/api/transactions')
def api_transactions():
    # ⚠ A01 — sem autenticação; retorna todas as transações
    conn = get_db()
    txs = conn.execute('SELECT * FROM transactions').fetchall()
    conn.close()
    return jsonify([dict(t) for t in txs])


@app.route('/api/debug')
def api_debug():
    # ⚠ A05 — endpoint de debug expõe configuração interna
    return jsonify({
        'secret_key': app.secret_key,
        'database':   DATABASE,
        'debug_mode': app.debug,
        'session_data': dict(session),
        'env_vars':   {k: v for k, v in os.environ.items() if 'PATH' not in k},
    })


@app.route('/api/fetch')
def api_fetch():
    url = request.args.get('url', '')
    if not url:
        return jsonify({'error': 'url param required'}), 400
    # ⚠ A10 — SSRF: busca qualquer URL sem validação
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NexBank/1.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        return jsonify({'url': url, 'content': content[:8000]})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/reset-password', methods=['POST'])
def api_reset_password():
    data = request.get_json(force=True) or {}
    username    = data.get('username', '')
    answer      = data.get('answer', '')
    new_password= data.get('new_password', '')
    # ⚠ A04 — sem rate limiting; pergunta de segurança é "sua cor favorita"
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    if user and user['sec_ans'].strip().lower() == answer.strip().lower():
        conn.execute('UPDATE users SET password=? WHERE username=?', (md5(new_password), username))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Senha redefinida.'})
    conn.close()
    return jsonify({'success': False, 'message': 'Resposta incorreta.'})


@app.route('/api/transfer', methods=['POST'])
def api_transfer():
    if 'user_id' not in session:
        return jsonify({'error': 'unauthenticated'}), 401
    # ⚠ A04 — sem CSRF token na API
    data      = request.get_json(force=True) or {}
    recipient = data.get('recipient', '')
    amount    = float(data.get('amount', 0))
    desc      = data.get('description', 'API transfer')
    conn      = get_db()
    me        = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    dest      = conn.execute('SELECT * FROM users WHERE username=?', (recipient,)).fetchone()
    if not dest:
        conn.close()
        return jsonify({'error': 'recipient not found'}), 404
    if me['balance'] < amount:
        conn.close()
        return jsonify({'error': 'insufficient funds'}), 400
    conn.execute('UPDATE users SET balance=balance-? WHERE id=?', (amount, session['user_id']))
    conn.execute('UPDATE users SET balance=balance+? WHERE id=?', (amount, dest['id']))
    conn.execute('INSERT INTO transactions (user_id,recipient,amount,description) VALUES (?,?,?,?)',
                 (session['user_id'], recipient, amount, desc))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'new_balance': me['balance'] - amount})


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print('\n' + '='*60)
    print('  NexBank — Lab de Pentest')
    print('  http://127.0.0.1:5000')
    print('='*60 + '\n')
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

def get_db():
    conn = sqlite3.connect('complaints.db')
    conn.row_factory = sqlite3.Row
    return conn

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('home.html')

# إرسال الشكوى
@app.route('/submit', methods=['POST'])
def submit():
    title = request.form['title']
    description = request.form['description']
    name = request.form.get('name', '').strip()
    anonymous = request.form.get('anonymous')

    if anonymous == 'yes':
        name = 'Anonymous'

    category = classify_complaint(description)

    conn = get_db()
    conn.execute('INSERT INTO complaints (name, title, description, category) VALUES (?, ?, ?, ?)',
                (name, title, description, category))
    conn.commit()
    conn.close()
    return render_template('success.html', category=category)

# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin123':
            session['admin'] = True
            return redirect('/admin')
        return render_template('admin_login.html', error='Wrong password!')
    if not session.get('admin'):
        return render_template('admin_login.html')
    conn = get_db()
    complaints = conn.execute('SELECT * FROM complaints').fetchall()
    conn.close()
    return render_template('admin.html', complaints=complaints)

# تغيير status الشكوى
@app.route('/admin/update/<int:id>', methods=['POST'])
def update_status(id):
    status = request.form['status']
    conn = get_db()
    conn.execute('UPDATE complaints SET status=? WHERE id=?', (status, id))
    conn.commit()
    conn.close()
    return redirect('/admin')

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect('/admin')

# تصنيف الشكوى بالـ AI
def classify_complaint(text):
    text = text.lower()
    if any(word in text for word in ['wifi', 'internet', 'network', 'computer', 'laptop', 'system', 'password', 'login']):
        return 'IT'
    elif any(word in text for word in ['grade', 'exam', 'course', 'professor', 'lecture', 'assignment']):
        return 'Academic'
    elif any(word in text for word in ['fee', 'payment', 'money', 'scholarship', 'finance', 'tuition']):
        return 'Finance'
    else:
        return 'General'

if __name__ == '__main__':
    app.run(debug=True)
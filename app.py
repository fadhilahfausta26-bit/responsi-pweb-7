from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_responsi'

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_responsi_pweb'
    )
    return conn

@app.route('/')
def index():
    if 'mahasiswa_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nim = request.form['nim']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM mahasiswa WHERE nim = %s AND password = %s", (nim, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['mahasiswa_id'] = user['id']
            session['nama'] = user['nama']
            session['nim'] = user['nim']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="NIM atau Password salah!")
            
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'mahasiswa_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM matakuliah")
    semua_matkul = cursor.fetchall()
    
    cursor.execute("""
        SELECT mk.id, mk.kode_mk, mk.nama_mk, mk.sks 
        FROM matakuliah_diambil md
        JOIN matakuliah mk ON md.matakuliah_id = mk.id
        WHERE md.mahasiswa_id = %s
    """, (session['mahasiswa_id'],))
    matkul_diambil = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', nama=session['nama'], nim=session['nim'], semua_matkul=semua_matkul, matkul_diambil=matkul_diambil)

@app.route('/ambil/<int:id_matkul>')
def ambil_matkul(id_matkul):
    if 'mahasiswa_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM matakuliah_diambil WHERE mahasiswa_id = %s AND matakuliah_id = %s", 
                   (session['mahasiswa_id'], id_matkul))
    sudah_ambil = cursor.fetchone()
    
    if not sudah_ambil:
        cursor.execute("INSERT INTO matakuliah_diambil (mahasiswa_id, matakuliah_id) VALUES (%s, %s)", 
                       (session['mahasiswa_id'], id_matkul))
        conn.commit()
        
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/hapus/<int:id_matkul>')
def hapus_matkul(id_matkul):
    if 'mahasiswa_id' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM matakuliah_diambil WHERE mahasiswa_id = %s AND matakuliah_id = %s", 
                   (session['mahasiswa_id'], id_matkul))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
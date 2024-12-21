from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from functools import wraps
import os
import mysql.connector
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'rahasia123'

# Konfigurasi Database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sistem_penyakit'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Konfigurasi upload
UPLOAD_FOLDER = 'static/images/penyakit'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Tambahkan timestamp untuk menghindari nama file yang sama
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{int(datetime.now().timestamp())}{ext}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    return None

# Route untuk halaman utama
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Mengambil 3 penyakit terbaru
    cursor.execute('''
        SELECT p.*, a.nama_admin,
        GROUP_CONCAT(DISTINCT g.nama_gejala) as gejala_list,
        GROUP_CONCAT(DISTINCT pb.nama_penyebab) as penyebab_list
        FROM penyakit p 
        JOIN admin a ON p.id_admin = a.id_admin
        LEFT JOIN ciri_ciri c ON p.id_penyakit = c.id_penyakit
        LEFT JOIN gejala g ON c.id_gejala = g.id_gejala
        LEFT JOIN detail_penyebab dp ON p.id_penyakit = dp.id_penyakit
        LEFT JOIN penyebab pb ON dp.id_penyebab = pb.id_penyebab
        GROUP BY p.id_penyakit
        ORDER BY p.id_penyakit DESC
        LIMIT 3
    ''')
    penyakit_list = cursor.fetchall()
    
    # Mengubah string gejala dan penyebab menjadi list
    for penyakit in penyakit_list:
        if penyakit['gejala_list']:
            penyakit['gejala'] = [{'nama_gejala': g} for g in penyakit['gejala_list'].split(',')]
        else:
            penyakit['gejala'] = []
            
        if penyakit['penyebab_list']:
            penyakit['penyebab'] = [{'nama_penyebab': p} for p in penyakit['penyebab_list'].split(',')]
        else:
            penyakit['penyebab'] = []
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', penyakit_list=penyakit_list)

# Route untuk halaman penyakit
@app.route('/penyakit')
def penyakit():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Mengambil data penyakit dengan join ke admin
    cursor.execute('''
        SELECT p.*, a.nama_admin,
        GROUP_CONCAT(DISTINCT g.nama_gejala) as gejala_list,
        GROUP_CONCAT(DISTINCT pb.nama_penyebab) as penyebab_list
        FROM penyakit p 
        JOIN admin a ON p.id_admin = a.id_admin
        LEFT JOIN ciri_ciri c ON p.id_penyakit = c.id_penyakit
        LEFT JOIN gejala g ON c.id_gejala = g.id_gejala
        LEFT JOIN detail_penyebab dp ON p.id_penyakit = dp.id_penyakit
        LEFT JOIN penyebab pb ON dp.id_penyebab = pb.id_penyebab
        GROUP BY p.id_penyakit
    ''')
    penyakit_list = cursor.fetchall()
    
    # Mengubah string gejala dan penyebab menjadi list
    for penyakit in penyakit_list:
        if penyakit['gejala_list']:
            penyakit['gejala'] = [{'nama_gejala': g} for g in penyakit['gejala_list'].split(',')]
        else:
            penyakit['gejala'] = []
            
        if penyakit['penyebab_list']:
            penyakit['penyebab'] = [{'nama_penyebab': p} for p in penyakit['penyebab_list'].split(',')]
        else:
            penyakit['penyebab'] = []
    
    cursor.close()
    conn.close()
    
    return render_template('penyakit.html', penyakit_list=penyakit_list)

# Route untuk halaman gejala
@app.route('/gejala')
def gejala():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil semua gejala untuk dropdown
    cursor.execute('SELECT * FROM gejala ORDER BY nama_gejala')
    gejala_list = cursor.fetchall()
    
    selected_gejala_ids = request.args.getlist('gejala[]')
    selected_gejala = []
    penyakit_list = []
    
    if selected_gejala_ids:
        # Ambil detail gejala yang dipilih
        placeholders = ','.join(['%s'] * len(selected_gejala_ids))
        cursor.execute(f'SELECT * FROM gejala WHERE id_gejala IN ({placeholders})', tuple(selected_gejala_ids))
        selected_gejala = cursor.fetchall()
        
        # Ambil penyakit yang memiliki gejala yang dipilih
        cursor.execute(f'''
            SELECT p.*, a.nama_admin,
            GROUP_CONCAT(DISTINCT g.nama_gejala) as gejala_list,
            GROUP_CONCAT(DISTINCT pb.nama_penyebab) as penyebab_list,
            COUNT(DISTINCT cc.id_gejala) as matched_symptoms
            FROM penyakit p 
            JOIN admin a ON p.id_admin = a.id_admin
            JOIN ciri_ciri cc ON p.id_penyakit = cc.id_penyakit
            LEFT JOIN ciri_ciri c ON p.id_penyakit = c.id_penyakit
            LEFT JOIN gejala g ON c.id_gejala = g.id_gejala
            LEFT JOIN detail_penyebab dp ON p.id_penyakit = dp.id_penyakit
            LEFT JOIN penyebab pb ON dp.id_penyebab = pb.id_penyebab
            WHERE cc.id_gejala IN ({placeholders})
            GROUP BY p.id_penyakit
            ORDER BY matched_symptoms DESC
        ''', tuple(selected_gejala_ids))
        penyakit_list = cursor.fetchall()
        
        # Convert string lists to array
        for penyakit in penyakit_list:
            if penyakit['gejala_list']:
                penyakit['gejala'] = [{'nama_gejala': g} for g in penyakit['gejala_list'].split(',')]
            else:
                penyakit['gejala'] = []
                
            if penyakit['penyebab_list']:
                penyakit['penyebab'] = [{'nama_penyebab': p} for p in penyakit['penyebab_list'].split(',')]
            else:
                penyakit['penyebab'] = []
    
    cursor.close()
    conn.close()
    
    return render_template('gejala.html',
                         gejala_list=gejala_list,
                         selected_gejala=selected_gejala,
                         penyakit_list=penyakit_list)

# Route untuk halaman konsultasi
@app.route('/konsultasi')
def konsultasi():
    return render_template('konsultasi.html')

# Route untuk login admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['admin_username'] = admin['username']
            session['admin_id'] = admin['id_admin']
            session['admin_level'] = admin['level']
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin/login.html', error='Username atau password salah')
    
    return render_template('admin/login.html')

# Route untuk dashboard admin
@app.route('/admin')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Mengambil total data
    cursor.execute('SELECT COUNT(*) as total FROM penyakit')
    total_penyakit = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM gejala')
    total_gejala = cursor.fetchone()['total']
    
    cursor.execute('SELECT COUNT(*) as total FROM penyebab')
    total_penyebab = cursor.fetchone()['total']
    
    # Data untuk aktivitas terbaru (contoh: 5 penyakit terakhir)
    cursor.execute('''
        SELECT p.nama_penyakit, a.nama_admin, p.id_penyakit 
        FROM penyakit p 
        JOIN admin a ON p.id_admin = a.id_admin 
        ORDER BY p.id_penyakit DESC LIMIT 5
    ''')
    recent_activities = []
    for row in cursor.fetchall():
        recent_activities.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'description': f'Menambah penyakit: {row["nama_penyakit"]}',
            'admin': row['nama_admin']
        })
    
    cursor.close()
    conn.close()
    
    data = {
        'total_penyakit': total_penyakit,
        'total_gejala': total_gejala,
        'total_penyebab': total_penyebab,
        'recent_activities': recent_activities
    }
    return render_template('admin/dashboard.html', **data)

# Route untuk kelola penyakit
@app.route('/admin/penyakit')
@login_required
def kelola_penyakit():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Ambil data penyakit
    cursor.execute('''
        SELECT p.*, a.nama_admin,
        GROUP_CONCAT(DISTINCT g.id_gejala) as gejala_ids,
        GROUP_CONCAT(DISTINCT pb.id_penyebab) as penyebab_ids
        FROM penyakit p 
        JOIN admin a ON p.id_admin = a.id_admin
        LEFT JOIN ciri_ciri c ON p.id_penyakit = c.id_penyakit
        LEFT JOIN gejala g ON c.id_gejala = g.id_gejala
        LEFT JOIN detail_penyebab dp ON p.id_penyakit = dp.id_penyakit
        LEFT JOIN penyebab pb ON dp.id_penyebab = pb.id_penyebab
        GROUP BY p.id_penyakit
    ''')
    penyakit_list = cursor.fetchall()
    
    # Convert string ids to list
    for penyakit in penyakit_list:
        penyakit['gejala_ids'] = [int(id) for id in penyakit['gejala_ids'].split(',')] if penyakit['gejala_ids'] else []
        penyakit['penyebab_ids'] = [int(id) for id in penyakit['penyebab_ids'].split(',')] if penyakit['penyebab_ids'] else []
    
    # Ambil data gejala dan penyebab untuk dropdown
    cursor.execute('SELECT * FROM gejala ORDER BY nama_gejala')
    gejala_list = cursor.fetchall()
    
    cursor.execute('SELECT * FROM penyebab ORDER BY nama_penyebab')
    penyebab_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/penyakit.html', 
                         penyakit_list=penyakit_list,
                         gejala_list=gejala_list,
                         penyebab_list=penyebab_list)

# Route untuk tambah penyakit
@app.route('/admin/penyakit/tambah', methods=['POST'])
@login_required
def tambah_penyakit():
    if request.method == 'POST':
        nama = request.form['nama_penyakit']
        deskripsi = request.form['desk_penyakit']
        saran = request.form.get('saran', '')
        admin_id = session['admin_id']
        gejala_ids = request.form.getlist('gejala[]')
        penyebab_ids = request.form.getlist('penyebab[]')
        
        # Handle file upload
        image_filename = None
        if 'gambar' in request.files:
            file = request.files['gambar']
            image_filename = save_image(file)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert penyakit
            cursor.execute('''
                INSERT INTO penyakit (nama_penyakit, desk_penyakit, saran, id_admin, images)
                VALUES (%s, %s, %s, %s, %s)
            ''', (nama, deskripsi, saran, admin_id, image_filename))
            
            # Get the id of inserted penyakit
            penyakit_id = cursor.lastrowid
            
            # Insert gejala relations
            for gejala_id in gejala_ids:
                cursor.execute('INSERT INTO ciri_ciri (id_penyakit, id_gejala) VALUES (%s, %s)',
                             (penyakit_id, gejala_id))
            
            # Insert penyebab relations
            for penyebab_id in penyebab_ids:
                cursor.execute('INSERT INTO detail_penyebab (id_penyakit, id_penyebab) VALUES (%s, %s)',
                             (penyakit_id, penyebab_id))
            
            conn.commit()
            flash('Penyakit berhasil ditambahkan', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('kelola_penyakit'))

# Route untuk edit penyakit
@app.route('/admin/penyakit/edit/<int:id_penyakit>', methods=['POST'])
@login_required
def edit_penyakit(id_penyakit):
    if request.method == 'POST':
        nama = request.form['nama_penyakit']
        deskripsi = request.form['desk_penyakit']
        saran = request.form.get('saran', '')
        gejala_ids = request.form.getlist('gejala[]')
        penyebab_ids = request.form.getlist('penyebab[]')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Cek gambar lama
            cursor.execute('SELECT images FROM penyakit WHERE id_penyakit = %s', (id_penyakit,))
            old_image = cursor.fetchone()['images']
            
            # Handle file upload
            image_filename = old_image
            if 'gambar' in request.files:
                file = request.files['gambar']
                if file.filename != '':
                    # Hapus gambar lama jika ada
                    if old_image and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], old_image)):
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_image))
                    image_filename = save_image(file)
            
            # Update penyakit
            cursor.execute('''
                UPDATE penyakit 
                SET nama_penyakit = %s, desk_penyakit = %s, saran = %s, images = %s
                WHERE id_penyakit = %s
            ''', (nama, deskripsi, saran, image_filename, id_penyakit))
            
            # Update gejala relations
            cursor.execute('DELETE FROM ciri_ciri WHERE id_penyakit = %s', (id_penyakit,))
            for gejala_id in gejala_ids:
                cursor.execute('INSERT INTO ciri_ciri (id_penyakit, id_gejala) VALUES (%s, %s)',
                             (id_penyakit, gejala_id))
            
            # Update penyebab relations
            cursor.execute('DELETE FROM detail_penyebab WHERE id_penyakit = %s', (id_penyakit,))
            for penyebab_id in penyebab_ids:
                cursor.execute('INSERT INTO detail_penyebab (id_penyakit, id_penyebab) VALUES (%s, %s)',
                             (id_penyakit, penyebab_id))
            
            conn.commit()
            flash('Penyakit berhasil diupdate', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('kelola_penyakit'))

# Route untuk hapus penyakit
@app.route('/admin/penyakit/hapus/<int:id_penyakit>', methods=['POST'])
@login_required
def hapus_penyakit(id_penyakit):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Ambil nama file gambar
        cursor.execute('SELECT images FROM penyakit WHERE id_penyakit = %s', (id_penyakit,))
        image = cursor.fetchone()['images']
        
        # Hapus gambar jika ada
        if image and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image))
        
        # Hapus data terkait di tabel ciri_ciri
        cursor.execute('DELETE FROM ciri_ciri WHERE id_penyakit = %s', (id_penyakit,))
        # Hapus data terkait di tabel detail_penyebab
        cursor.execute('DELETE FROM detail_penyebab WHERE id_penyakit = %s', (id_penyakit,))
        # Hapus penyakit
        cursor.execute('DELETE FROM penyakit WHERE id_penyakit = %s', (id_penyakit,))
        conn.commit()
        flash('Penyakit berhasil dihapus', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('kelola_penyakit'))

# Route untuk kelola gejala
@app.route('/admin/gejala')
@login_required
def kelola_gejala():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT g.*, a.nama_admin FROM gejala g JOIN admin a ON g.id_admin = a.id_admin')
    gejala_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/gejala.html', gejala_list=gejala_list)

# Route untuk tambah gejala
@app.route('/admin/gejala/tambah', methods=['POST'])
@login_required
def tambah_gejala():
    if request.method == 'POST':
        nama = request.form['nama_gejala']
        admin_id = session['admin_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO gejala (nama_gejala, id_admin) VALUES (%s, %s)', (nama, admin_id))
            conn.commit()
            flash('Gejala berhasil ditambahkan', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('kelola_gejala'))

# Route untuk edit gejala
@app.route('/admin/gejala/edit/<int:id_gejala>', methods=['POST'])
@login_required
def edit_gejala(id_gejala):
    if request.method == 'POST':
        nama = request.form['nama_gejala']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE gejala SET nama_gejala = %s WHERE id_gejala = %s', (nama, id_gejala))
            conn.commit()
            flash('Gejala berhasil diupdate', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('kelola_gejala'))

# Route untuk hapus gejala
@app.route('/admin/gejala/hapus/<int:id_gejala>', methods=['POST'])
@login_required
def hapus_gejala(id_gejala):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Hapus data terkait di tabel ciri_ciri
        cursor.execute('DELETE FROM ciri_ciri WHERE id_gejala = %s', (id_gejala,))
        # Hapus gejala
        cursor.execute('DELETE FROM gejala WHERE id_gejala = %s', (id_gejala,))
        conn.commit()
        flash('Gejala berhasil dihapus', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('kelola_gejala'))

# Route untuk kelola penyebab
@app.route('/admin/penyebab')
@login_required
def kelola_penyebab():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute('SELECT p.*, a.nama_admin FROM penyebab p JOIN admin a ON p.id_admin = a.id_admin')
    penyebab_list = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin/penyebab.html', penyebab_list=penyebab_list)

# Route untuk tambah penyebab
@app.route('/admin/penyebab/tambah', methods=['POST'])
@login_required
def tambah_penyebab():
    if request.method == 'POST':
        nama = request.form['nama_penyebab']
        admin_id = session['admin_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO penyebab (nama_penyebab, id_admin) VALUES (%s, %s)', (nama, admin_id))
            conn.commit()
            flash('Penyebab berhasil ditambahkan', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('kelola_penyebab'))

# Route untuk edit penyebab
@app.route('/admin/penyebab/edit/<int:id_penyebab>', methods=['POST'])
@login_required
def edit_penyebab(id_penyebab):
    if request.method == 'POST':
        nama = request.form['nama_penyebab']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE penyebab SET nama_penyebab = %s WHERE id_penyebab = %s', (nama, id_penyebab))
            conn.commit()
            flash('Penyebab berhasil diupdate', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
        finally:
            cursor.close()
            conn.close()
            
        return redirect(url_for('kelola_penyebab'))

# Route untuk hapus penyebab
@app.route('/admin/penyebab/hapus/<int:id_penyebab>', methods=['POST'])
@login_required
def hapus_penyebab(id_penyebab):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Hapus data terkait di tabel detail_penyebab
        cursor.execute('DELETE FROM detail_penyebab WHERE id_penyebab = %s', (id_penyebab,))
        # Hapus penyebab
        cursor.execute('DELETE FROM penyebab WHERE id_penyebab = %s', (id_penyebab,))
        conn.commit()
        flash('Penyebab berhasil dihapus', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Terjadi kesalahan: {str(e)}', 'error')
    finally:
        cursor.close()
        conn.close()
        
    return redirect(url_for('kelola_penyebab'))

# Route untuk logout
@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True, port=5501) 
from flask import jsonify, request
from app import app, db
from app.models import Admin, Penyakit, Gejala, Penyebab, CiriCiri, DetailPenyebab
from app.schemas import (admin_schema, admins_schema, penyakit_schema, 
                        penyakits_schema, gejala_schema, gejalas_schema,
                        penyebab_schema, penyebabs_schema)
from werkzeug.security import generate_password_hash, check_password_hash

# Routes untuk Admin
@app.route('/admin', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify(admins_schema.dump(admins))

@app.route('/admin', methods=['POST'])
def add_admin():
    nama_admin = request.json['nama_admin']
    username = request.json['username']
    password = generate_password_hash(request.json['password'])
    level = request.json['level']
    
    new_admin = Admin(nama_admin=nama_admin, username=username, 
                     password=password, level=level)
    
    db.session.add(new_admin)
    db.session.commit()
    
    return admin_schema.jsonify(new_admin)

# Routes untuk Penyakit
@app.route('/penyakit', methods=['GET'])
def get_penyakits():
    penyakits = Penyakit.query.all()
    return jsonify(penyakits_schema.dump(penyakits))

@app.route('/penyakit', methods=['POST'])
def add_penyakit():
    data = request.json
    new_penyakit = Penyakit(
        nama_penyakit=data['nama_penyakit'],
        images=data['images'],
        desk_penyakit=data['desk_penyakit'],
        saran=data['saran'],
        id_admin=data['id_admin']
    )
    
    db.session.add(new_penyakit)
    db.session.commit()
    
    # Tambahkan gejala
    if 'gejala_ids' in data:
        for gejala_id in data['gejala_ids']:
            ciri = CiriCiri(id_penyakit=new_penyakit.id_penyakit, 
                           id_gejala=gejala_id)
            db.session.add(ciri)
    
    # Tambahkan penyebab
    if 'penyebab_ids' in data:
        for penyebab_id in data['penyebab_ids']:
            detail = DetailPenyebab(id_penyakit=new_penyakit.id_penyakit, 
                                  id_penyebab=penyebab_id)
            db.session.add(detail)
    
    db.session.commit()
    return penyakit_schema.jsonify(new_penyakit)

# Routes untuk Gejala
@app.route('/gejala', methods=['GET'])
def get_gejalas():
    gejalas = Gejala.query.all()
    return jsonify(gejalas_schema.dump(gejalas))

@app.route('/gejala', methods=['POST'])
def add_gejala():
    nama_gejala = request.json['nama_gejala']
    id_admin = request.json['id_admin']
    
    new_gejala = Gejala(nama_gejala=nama_gejala, id_admin=id_admin)
    db.session.add(new_gejala)
    db.session.commit()
    
    return gejala_schema.jsonify(new_gejala)

# Routes untuk Penyebab
@app.route('/penyebab', methods=['GET'])
def get_penyebabs():
    penyebabs = Penyebab.query.all()
    return jsonify(penyebabs_schema.dump(penyebabs))

@app.route('/penyebab', methods=['POST'])
def add_penyebab():
    nama_penyebab = request.json['nama_penyebab']
    id_admin = request.json['id_admin']
    
    new_penyebab = Penyebab(nama_penyebab=nama_penyebab, id_admin=id_admin)
    db.session.add(new_penyebab)
    db.session.commit()
    
    return penyebab_schema.jsonify(new_penyebab) 
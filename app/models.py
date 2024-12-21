from app import db
from datetime import datetime

class Admin(db.Model):
    id_admin = db.Column(db.Integer, primary_key=True)
    nama_admin = db.Column(db.String(30))
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text)
    level = db.Column(db.String(20))

class Penyakit(db.Model):
    id_penyakit = db.Column(db.Integer, primary_key=True)
    nama_penyakit = db.Column(db.String(30))
    images = db.Column(db.String(200))
    desk_penyakit = db.Column(db.Text)
    saran = db.Column(db.Text)
    id_admin = db.Column(db.Integer, db.ForeignKey('admin.id_admin'))
    
    gejala = db.relationship('Gejala', secondary='ciri_ciri')
    penyebab = db.relationship('Penyebab', secondary='detail_penyebab')

class Gejala(db.Model):
    id_gejala = db.Column(db.Integer, primary_key=True)
    nama_gejala = db.Column(db.Text)
    id_admin = db.Column(db.Integer, db.ForeignKey('admin.id_admin'))

class Penyebab(db.Model):
    id_penyebab = db.Column(db.Integer, primary_key=True)
    nama_penyebab = db.Column(db.Text)
    id_admin = db.Column(db.Integer, db.ForeignKey('admin.id_admin'))

class CiriCiri(db.Model):
    id_ciri_ciri = db.Column(db.Integer, primary_key=True)
    id_penyakit = db.Column(db.Integer, db.ForeignKey('penyakit.id_penyakit'))
    id_gejala = db.Column(db.Integer, db.ForeignKey('gejala.id_gejala'))

class DetailPenyebab(db.Model):
    id_detail_penyebab = db.Column(db.Integer, primary_key=True)
    id_penyakit = db.Column(db.Integer, db.ForeignKey('penyakit.id_penyakit'))
    id_penyebab = db.Column(db.Integer, db.ForeignKey('penyebab.id_penyebab')) 
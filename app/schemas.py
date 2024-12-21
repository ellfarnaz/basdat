from app import ma

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id_admin', 'nama_admin', 'username', 'level')

class GejalaSchema(ma.Schema):
    class Meta:
        fields = ('id_gejala', 'nama_gejala')

class PenyebabSchema(ma.Schema):
    class Meta:
        fields = ('id_penyebab', 'nama_penyebab')

class PenyakitSchema(ma.Schema):
    gejala = ma.Nested(GejalaSchema, many=True)
    penyebab = ma.Nested(PenyebabSchema, many=True)
    
    class Meta:
        fields = ('id_penyakit', 'nama_penyakit', 'images', 'desk_penyakit', 
                 'saran', 'gejala', 'penyebab')

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)
penyakit_schema = PenyakitSchema()
penyakits_schema = PenyakitSchema(many=True)
gejala_schema = GejalaSchema()
gejalas_schema = GejalaSchema(many=True)
penyebab_schema = PenyebabSchema()
penyebabs_schema = PenyebabSchema(many=True) 
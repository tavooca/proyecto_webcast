# coding: utf8
# intente algo como
def index(): return dict(message="hello from configuracion.py")

@auth.requires_login()
def grupos():
    formulario=SQLFORM.grid(db.grupos,deletable=False,create=False,editable=False)
    return locals()

@auth.requires_login()
def estados():
    formulario=SQLFORM.grid(db.estados,deletable=False,create=False,editable=False)
    return locals()

@auth.requires_login()
def tipos():
    formulario=SQLFORM.grid(db.tipos,deletable=False,create=False,editable=False)
    return locals()

@auth.requires_login()
def clientes():
    formulario=SQLFORM.grid(db.clientes)
    return locals()

@auth.requires_login()
def proyectos():
    formulario=SQLFORM.smartgrid(db.proyecto)
    return locals()

@auth.requires_login()
def tareas():
    formulario=SQLFORM.grid(db.tareas)
    return locals()
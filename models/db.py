# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)


## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)



db.define_table("grupos",
    Field("grupo", length=100, notnull=True, default=None))

db.define_table("clientes",
    Field("nombres", notnull=True, default=None),
    Field("apellidos", notnull=True, default=None),
    Field("empresa", default=None),
    Field("telefono", default=None),
    Field("email", default=None),
    Field("observacion", "text", default=None),
    Field("foto", "upload", default=None))

db.define_table("estados",
    Field("grupo", db.grupos),
    Field("estado", notnull=True, default=None))

db.define_table("tipos",
    Field("grupo", db.grupos),
    Field("tipo", notnull=True, default=None))

db.define_table("proyecto",
    Field("nombre", default=None),
    Field("cliente", db.clientes),
    Field("tipo", db.tipos),
    Field("estado", db.estados),
    Field("fecha_inicio", "date", notnull=True, default=None),
    Field("fecha_fin", "date", notnull=True, default=None),
    Field("valor", "integer", notnull=True, default=None),
    Field("observacion", "text", default=None),
    Field("usuario", db.auth_user, default=None))

db.define_table("tareas",
    Field("nombre", notnull=True, default=None),
    Field("tarea", "text", notnull=True, default=None),
    Field("proyecto", db.proyecto),
    Field("estado", db.estados),
    Field("fecha_inicio", "date", notnull=True, default=None),
    Field("fecha_fin", "date", notnull=True, default=None))

""" Relations between tables (remove fields you don't need from requires) """
db.estados.grupo.requires=IS_IN_DB( db, 'grupos.id', ' %(grupo)s')
db.tipos.grupo.requires=IS_IN_DB( db, 'grupos.id', ' %(grupo)s')
db.proyecto.cliente.requires=IS_IN_DB( db, 'clientes.id', ' %(nombres)s %(apellidos)s %(empresa)s %(telefono)s %(email)s %(onservacion)s %(foto)s')
db.proyecto.tipo.requires=IS_IN_DB( db, 'tipos.id', ' %(grupo)s %(tipo)s')
db.proyecto.estado.requires=IS_IN_DB( db, 'estados.id', ' %(grupo)s %(estado)s')
db.tareas.proyecto.requires=IS_IN_DB( db, 'proyecto.id', ' %(nombre)s %(cliente)s %(tipo)s %(estado)s %(fecha_inicio)s %(fecha_fin)s %(valor)s %(observacion)s %(usuario)s')
db.tareas.estado.requires=IS_IN_DB( db, 'estados.id', ' %(grupo)s %(estado)s')

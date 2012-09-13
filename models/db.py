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
auth.settings.actions_disabled = ['change_password','request_reset_password','retrieve_username']

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
    Field("grupo",requires = IS_NOT_EMPTY(error_message=T('El campo grupo es obligatorio'))),
    format = '%(grupo)s'
    )
db.grupos.grupo.requires = IS_NOT_IN_DB(db, 'grupos.grupo')

db.define_table("estados",
    Field("grupo", db.grupos),
    Field("estado",requires = IS_NOT_EMPTY(error_message=T('El campo estado es obligatorio'))),
    format = '%(estado)s'
    )
db.estados.estado.requires = IS_NOT_IN_DB(db, 'estados.estado')

db.define_table("tipos",
    Field("grupo", db.grupos),
    Field("tipo",requires = IS_NOT_EMPTY(error_message=T('El campo tipo es obligatorio'))),
    format = '%(tipo)s'
    )
db.tipos.tipo.requires = IS_NOT_IN_DB(db, 'tipos.tipo')

db.define_table("clientes",
    Field("nombres",requires = IS_NOT_EMPTY(error_message=T('El campo nombre es obligatorio'))),
    Field("apellidos",requires = IS_NOT_EMPTY(error_message=T('El campo apellido es obligatorio'))),
    Field("empresa",requires = IS_NOT_EMPTY(error_message=T('El campo empresa es obligatorio'))),
    Field("telefono"),
    Field("email",requires = IS_EMAIL(error_message=T('Email Invalido !'))),
    Field("observacion", "text"),
    Field("foto", "upload"),
    format = '%(apellidos)s %(nombres)s'
    )

#IS_DATE
#requires = IS_EMAIL(error_message=T('invalid email!'))

db.define_table("proyecto",
    Field("nombre",requires = IS_NOT_EMPTY(error_message=T('El campo nombre es obligatorio'))),
    Field("cliente", db.clientes),
    Field("tipo", db.tipos),
    Field("estado", db.estados),
    Field("fecha_inicio", "date", requires = IS_DATE(error_message=T('El campo debe ser una Fecha'))),
    Field("fecha_fin", "date", requires = IS_DATE(error_message=T('El campo debe ser una Fecha'))),
    Field("valor", "integer",requires = IS_NOT_EMPTY(error_message=T('El campo valor es obligatorio'))),
    Field("observacion", "text"),
    Field("usuario", db.auth_user),
    format = '%(nombre)s'
    )

db.define_table("tareas",
    Field("nombre",requires = IS_NOT_EMPTY(error_message=T('El campo nombre es obligatorio'))),
    Field("tarea", "text", requires = IS_NOT_EMPTY(error_message=T('El campo tarea es obligatorio'))),
    Field("proyecto", db.proyecto),
    Field("estado", db.estados),
    Field("fecha_inicio", "date", requires = IS_DATE(error_message=T('El campo debe ser una Fecha'))),
    Field("fecha_fin", "date", requires = IS_DATE(error_message=T('El campo debe ser una Fecha'))),
    format = '%(nombre)s (%(proyecto)s)'
    )
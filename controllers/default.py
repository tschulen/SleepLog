# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

def index():
    q = db.entry
    title = db().select(db.entry.title)
    entries = db().select(db.entry.body)
    url = URL('download')
    # LOL I'm bad for copying and pasting similar things
    def generate_view_button(row):
        b = '' 
        b = A('View', _class = 'btn', _href=URL('default','view',args=[row.id]))
        return b

    def generate_edit_button(row):
        #If the record is ours, we can edit it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class = 'btn', _href=URL('default','edit',args=[row.id]))
        return b
     # creates extra buttons
    links = []
    links.append(dict(header= '',body = generate_edit_button))
    links.append(dict(header= '', body = generate_view_button))

    form = SQLFORM.grid(q,
        fields=[db.entry.user_id, db.entry.date_posted,
                db.entry.category, db.entry.title,
                db.entry.body],
        editable=False, deletable=False,
        details = False,
        links = links,
        csv= False,
        upload= url,
        paginate=10,
        )  
    return dict(form=form, title=title)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)

def manage():
    grid = SQLFORM.smartgrid(db.entry, linked_tables=['entry'])
    return dict(grid=grid)



@auth.requires_login()
def edit():
    """edit post"""
    p = db.entry(request.args(0)) or redirect(URL('default', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not Authorized')
        redirect(URL('default','index'))

   # USER AUTHENTICATION NOT YET IMPLEMENTED
    form = SQLFORM(db.entry, record=p)
    if form.process().accepted:
        session.flash = T('Updated')
        redirect(URL('default', 'index'))
        # redirect(URL('default', 'view', args=[p.id]))
    return dict(form=form)
    
def view():
    """view a post"""
    # p = db(db.bboard.id == request.args(0)).select().first()
    p = db.entry(request.args(0)) or redirect(URL('default','index'))
    url = URL('download')
    dreamCategory = p.category
    form = SQLFORM(db.entry, record = p, readonly = True, upload=url)
    # p.name would contain the name of the poster.
    return dict(form=form, dreamCategory=dreamCategory)

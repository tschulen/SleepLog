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
    q = db.entry.private == False
    title = db().select(db.entry.title)
    entries = db().select(db.entry.body)
    url = URL('download')

    def generate_view_button(row):
        b = '' 
        # Cloud button for 'Normal' category
        if row.category == "Normal":
            b = A(IMG(_src=URL('static/images','cloud.png'), _name = "cloudbutton",
                         _alt="cloudbutton",_width = "30", _height = "30", 
                         _id = "cloudpic", _border = "0",
                         _onMouseOver = "this.src='/SleepLog/static/images/cloud3.png'",
                         _onMouseOut = "this.src='/SleepLog/static/images/cloud.png'" ),
                         _class = 'btn', _href=URL('default','view',args=[row.id]))
        # Ghost button for 'Normal' category
        elif row.category == "Nightmare":
            b = A(IMG(_src=URL('static/images','ghost.png'), _name = "ghostbutton", 
                        _alt="ghostbutton",_width = "30", _height = "30",
                        _id = "ghostpic", _border = "0",
                        _onMouseOver = "this.src='/SleepLog/static/images/ghost2.png'",
                        _onMouseOut = "this.src='/SleepLog/static/images/ghost.png'" ),
                        _class = 'btn', _href=URL('default','view',args=[row.id]))
        # Star button for 'Normal' category
        # TODO May want to have star glow when hovering over with mouse
        elif row.category == "Lucid":
            b = A(IMG(_src=URL('static/images', 'star.png'), _name="starbutton",
                        _alt = "starbutton", _width="30", _height="30", 
                        _id = "starpic", _border="0", 
                        _onMouseOver = "this.src='/SleepLog/static/images/star2.png'",
                        _onMouseOut = "this.src='/SleepLog/static/images/star.png'"),
                        _class = 'btn', _href=URL('default','view',args=[row.id]))
        return b


    def generate_edit_button(row):
        #If the record is ours, we can edit it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Edit', _class = 'btn', _href=URL('default','edit',args=[row.id]))
        return b

    def generate_delete_item_button(row):
        # If the record is ours, we can confirm to delete it.
        b = ''
        if auth.user_id == row.user_id:
            b = A('Delete', _class='btn', _href=URL('default', 'delete_item', args=[row.id]))
        return b

    # creates extra buttons
    links = []
    links.append(dict(header= '', body = generate_edit_button))
    links.append(dict(header= '', body = generate_delete_item_button))
    links.append(dict(header= '', body = generate_view_button))

    # Generate grid from database
    grid = SQLFORM.grid(q,
        fields=[db.entry.user_id, 
                db.entry.category, db.entry.title,
                db.entry.body, db.entry.date_posted],
                csv= False,
                editable=False,
                deletable=False,
                details = False,
                links = links,
                paginate=10,
                upload= url,
                )  

    return dict(title=title, grid=grid)

def about():
    return dict()

def statistics():
    normal_count = db(db.entry.category == 'Normal').count()    
    nightmare_count = db(db.entry.category == 'Nightmare').count()    
    lucid_count = db(db.entry.category == 'Lucid').count()    
    return dict(normal_count=normal_count, nightmare_count=nightmare_count,
                lucid_count=lucid_count)

def chat():
    return dict()
    
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


@auth.requires_login()
def delete_item():
     item = db.entry(request.args(0)) or redirect(URL('default', 'index'))
     form = FORM.confirm('Confirm Delete',{'Back':URL('default', 'index')})
     if form.accepted:
         db(db.entry.id == item.id).delete()
         redirect(URL('default', 'index'))
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


#New default register screen controller
def register():
    """Register Screen"""
    #
    return dict(form=auth.register())

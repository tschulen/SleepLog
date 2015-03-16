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
    new_entry_btn = A('New Entry', _class='btn', _href=URL('default', 'new_entry'))


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
                create=False,
                csv = False,
                editable =False,
                deletable = False,
                details = False,
                links = links,
                paginate = 10,
                upload = url,
                orderby=~db.entry.date_posted,
    )  

    return dict(title=title, grid=grid, new_entry_btn=new_entry_btn)

@auth.requires_login()
def new_entry():
    form = SQLFORM.factory(
        Field('title', requires=IS_NOT_EMPTY()),
        Field('body', 'text'),
        Field('private', 'boolean'),
        Field('category', requires=IS_IN_SET(['Normal', 'Nightmare', 'Lucid'])),
        Field('tags', 'list:string'),  
    )
    if form.process().accepted:
        entry = db.entry.insert(title=form.vars.title, body=form.vars.body,
                        private=form.vars.private, category=form.vars.category)
        for tag in form.vars.tags:
            db.tag.insert(name=tag)
            
        redirect(URL('index'))
        response.flash = 'Success!'

    return dict(form=form)

@auth.requires_login() 
def suggestions():
        s=db.suggestions
        formsuggestions = SQLFORM.grid(s,
                       fields=[db.suggestions.category,
                               db.suggestions.msg,]
                       )
  
        return dict(formsuggestions=formsuggestions)

def chat():
    return dict()

def about():
    return dict()

def faq():
    return dict()

def statistics():
    normal_count = db(db.entry.category == 'Normal').count()    
    nightmare_count = db(db.entry.category == 'Nightmare').count()    
    lucid_count = db(db.entry.category == 'Lucid').count()    
    tag_list = []
    count_dict = dict()
    for row in db().select(db.tag.ALL):
        row_name = str(row.name)
        if row.name is not '':
            if not row.name in count_dict:
                count_dict[row.name] = 1
            else:
                count_dict[row.name] += 1
    top_five_tags = sorted(count_dict, key=count_dict.get, reverse=True)[:5]
    tag1 = None
    tag2 = None
    tag3 = None
    tag4 = None
    tag5 = None
    for i in range(0, len(top_five_tags)): 
        if i == 0:
            tag1 = top_five_tags[i]
        elif i == 1:
            tag2 = top_five_tags[i]
        elif i == 2:
            tag3 = top_five_tags[i]
        elif i == 3:
            tag4 = top_five_tags[i]
        elif i == 4:
            tag5 = top_five_tags[i]
    return dict(normal_count=normal_count, nightmare_count=nightmare_count,
                lucid_count=lucid_count, top_five_tags=top_five_tags,
                tag1=tag1, tag2=tag2, tag3=tag3, tag4=tag4, tag5=tag5)


def chat():
    return dict()
    
def emailexample():
    form = SQLFORM.factory(
    Field('name', requires=IS_NOT_EMPTY(), default= get_author()),
    Field('email', requires =[ IS_EMAIL(error_message='invalid email!'), IS_NOT_EMPTY() ]),
    Field('subject', requires=IS_NOT_EMPTY()),
    Field('message', requires=IS_NOT_EMPTY(), type='text')
    )
    if form.process().accepted:
        session.name = form.vars.name
        session.email = form.vars.email
        session.subject = form.vars.subject
        session.message = form.vars.message

        # Note that this sends out a dummy mail to your web2py e-mail, emails to yahoo might be slow to arrive
        if mail:
            # you can possibly just change it to session.email instead of auth.user.email
            if mail.send(to=[session.email],
                # same goes for everything here too using session stuffs
                subject=session.subject,
                # I included the users email as well to be sent.
                message= "Message from" + get_email() +"\n"+ session.message
            ):
                response.flash = 'email sent sucessfully.'
            else:
                response.flash = 'fail to send email sorry!'
        else:
            response.flash = 'Unable to send the email : email parameters not defined'
    elif form.errors:
            response.flash='form has errors.'

    return dict(form=form)

def get_author():
    # This shouldn't be called when a user isn't logged in,
    # but just in case we have a placeholder name.
    a = request.client
    # If we're logged in pull our first and last names into a name
    if auth.user:
        a = auth.user.first_name + " " + auth.user.last_name
    return a
def get_email():
    # This shouldn't be called when a user isn't logged in,
    # but just in case we have a placeholder name.
    a = "example@blah.com"
    # If we're logged in pull our first and last names into a name
    if auth.user:
        a = auth.user.email
    return a

def new_post():
    form = SQLFORM(db.comments)
    if form.accepts(request, formname=None):
        # q2 = db(db.comments.commentpost!=None).select().last() #This grabs last element in db
        q2 = db(db.comments.commentpost!=None).select() #grabs the db section
        # return DIV(q2.commentpost) #This just returns the post
        return DIV(q2) #This returns the database
    elif form.errors:
        return TABLE(*[TR(k, v) for k, v in form.errors.items()])

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

def view_tag():
    grid = SQLFORM.grid(q,
        fields=[db.entry.user_id, 
                db.entry.category, db.entry.title,
                db.entry.body, db.entry.date_posted],
                create=False,
                csv = False,
                editable =False,
                deletable = False,
                details = False,
                links = links,
                paginate = 10, 
                upload = url,
                orderby=~db.entry.date_posted,
    ) 
    return dict(grid=grid)


#New default register screen controller
def register():
    """Register Screen"""
    #
    return dict(form=auth.register())

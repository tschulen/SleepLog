from datetime import datetime

db.define_table('entry',
        Field('date_posted', 'datetime'),
        Field('title'),
        Field('body', 'text'), 
        Field('private', 'boolean'),
        Field('category'),
        Field('user_id', db.auth_user),
        Field('picture', 'upload'), #User profile picture. TODO: Set Size Const. to 100x100px
        Field('tags', 'list:reference tag'),
)

db.define_table('tag',
    Field('name'),
    format='%(name)s'
)
db.define_table('comments',
    Field('commentpost', 'text')
)

db.comments.commentpost.requires = IS_NOT_EMPTY()
db.entry.category.readable = True
db.entry.id.readable = False
db.entry.date_posted.default = datetime.utcnow()
db.entry.date_posted.writable = False 
db.entry.private.default = False
db.entry.tags.readable = False
db.entry.tags.writable = False
db.entry.user_id.default = auth.user_id
db.entry.user_id.writable = db.entry.user_id.readable = False

db.entry.category.requires = IS_IN_SET(['Normal', 'Nightmare', 'Lucid'])

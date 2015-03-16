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

#Restrictions/Settings for entry table
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

#Defines table for tag
db.define_table('tag',
    Field('name'),
    format='%(name)s'
)

#Defines table for comments
db.define_table('comments',
    Field('commentpost', 'text')
)
#Restriction/Setting for comments table
db.comments.commentpost.requires = IS_NOT_EMPTY()

#Defines table for comment posts
db.define_table('comment_post',
   Field('body','text',label='Your comment'),
   auth.signature)

#Table for User suggestions for the website
db.define_table('suggestions',
        Field('date_posted', 'datetime'),
        Field('user_id', db.auth_user),
        Field('category'),
        Field('msg', 'text'),
        )

#Restrictions/Settings for suggestions table
CATEGORY = ['Suggestion', 'Issue/bug', 'Comment']
db.suggestions.category.readable=True
db.suggestions.category.default = 'Comment'
db.suggestions.category.required = True
db.suggestions.category.requires = IS_IN_SET(CATEGORY, zero=None)
db.suggestions.date_posted.default = datetime.utcnow()
db.suggestions.date_posted.writable =db.suggestions.date_posted.readable = False
db.suggestions.user_id.default=auth.user_id
db.suggestions.user_id.writable = db.suggestions.user_id.readable = False

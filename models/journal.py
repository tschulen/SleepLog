from datetime import datetime

db.define_table('entry',
        Field('title'),
        Field('body', 'text'), 
        Field('date_posted', 'datetime'),
        Field('is_lucid', 'boolean'),
        Field('user_id', db.auth_user),
        )

db.entry.user_id.default = auth.user_id
db.entry.user_id.writable = db.entry.user_id.readable = False

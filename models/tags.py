db.define_table('tags',
    Field('title'),
    format='%(id)s'
)

db.define_table('entry_tag',
    Field('entry_id'),
    Field('tag_id'),
    format='%(entry_id)s'
)

db.define_table('tags',
    Field('title'),
)

db.define_table('entry_tag',
    Field('entry_id'),
    Field('tag_id'),
)

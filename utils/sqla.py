from flask_sqlalchemy import SQLAlchemy


def list_models(db: SQLAlchemy):
    classes, models, table_names = [], [], []
    for clazz in db.Model._decl_class_registry.values():
        if getattr(clazz, '__tablename__', None):
            table_names.append(clazz.__tablename__)
            classes.append(clazz)
    for table in db.metadata.tables.items():
        if table[0] in table_names:
            models.append(classes[table_names.index(table[0])])

    return models

# Peewee helpers, so we don't need peewee as a dependancy
# TODO: Move this to ext


def has_base(obj, class_name):
    for base in obj.__class__.__mro__:
        if base.__name__ == class_name:
            return True

    return False


def is_model(obj):
    return has_base(obj, 'Model')


def is_model_select(obj):
    return has_base(obj, 'ModelSelect')


def is_foreign_key(field):
    return has_base(field, 'ForeignKeyField')


def model_to_dict(model):
    """
    Simple model_to_dict -- with recuse forever as default
    """
    data = {}

    for field in model._meta.sorted_fields:

        field_data = model.__data__.get(field.name)

        if is_foreign_key(field):
            if field_data:
                rel_obj = getattr(model, field.name)
                field_data = model_to_dict(rel_obj)
            else:
                field_data = None

        data[field.name] = field_data

    return data

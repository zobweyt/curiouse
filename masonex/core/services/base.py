from django.db.models import Manager

from .decorators import all_fields_decorator


@all_fields_decorator
def all_objects(objects: Manager):
    return objects.all()


@all_fields_decorator
def filter_objects(objects: Manager, **kwargs):
    return objects.filter(**kwargs)


def create_object(objects: Manager, **kwargs):
    objects.create(**kwargs)


def update_object(obj, **kwargs):
    obj.update(**kwargs)


def delete_object(obj):
    obj.delete()

from django.db.models import Manager


# similar methods

def select_related_fields_decorator(service_func: callable):

    def select_related_fields_wrapper(objects: Manager, select_related=(), **kwargs) -> Manager:
        return service_func(objects, **kwargs).select_related(*select_related)
    
    return select_related_fields_wrapper


def prefetch_related_fields_decorator(service_func: callable):

    def prefetch_related_fields_wrapper(objects: Manager, prefetch_related=(), **kwargs) -> Manager:
        return service_func(objects, **kwargs).prefetch_related(*prefetch_related)

    return prefetch_related_fields_wrapper


def only_fields_decorator(service_func: callable):

    def only_fields_wrapper(objects: Manager, only=(), **kwargs) -> Manager:
        return service_func(objects, **kwargs).only(*only)
    
    return only_fields_wrapper

# similar methods


def limit_fields_decorator(service_func: callable):

    def limit_fields_wrapper(objects: Manager, limit=None, **kwargs) -> Manager:
        return service_func(objects, **kwargs)[:limit]
    
    return limit_fields_wrapper


def all_fields_decorator(service_func: callable):
    
    @select_related_fields_decorator
    @prefetch_related_fields_decorator
    @only_fields_decorator
    @limit_fields_decorator
    def all_fields_wrapper(objects: Manager, **kwargs) -> Manager:
        return service_func(objects, **kwargs)
    
    return all_fields_wrapper

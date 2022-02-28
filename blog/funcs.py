from django.http import Http404


"""Статические функции, которые могут быть использованы в формировании представлений"""


def control_empty(get_queryset):
        def wrapper(self):
            obj = get_queryset(self)
            if len(obj) == 0:
                raise Http404
            return obj
        return wrapper
from django.forms.fields import Field


class TitleMixin:
    """
    Adds `title` to the context.
    """

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_title()
        return context
    
    def get_title(self):
        return self.title


class DecorateFormFieldsMixin:
    """
    Adds `css_class` to every `Field` instance in a form.
    """

    css_class = "form-control"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            self.__decorate_field(field)

    def __decorate_field(self, field):
        if isinstance(field, Field):
            extra_css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = " ".join((self.css_class, extra_css_class))

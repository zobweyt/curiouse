from django.forms.fields import CharField, ChoiceField


class TitleMixin:
    """
    Provides an easy way to work with page title.
    """

    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context
    
    def get_title(self):
        return self.title


class DecorateFormInputsMixin:
    """
    Adds 'css_class' CSS class attribute to every 'css_decorated_fields' fields in a form.
    """

    css_class_decorated_fields = (
        CharField,
        ChoiceField,
    )

    css_class = 'form-control form-control-sm lh-sm fs-md'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            self.__decorate_field(field)

    def __decorate_field(self, field):
        if isinstance(field, self.css_class_decorated_fields):
            field.widget.attrs.update({'class': self.css_class})

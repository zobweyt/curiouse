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


class DecorateFormFieldsMixin:
    """
    Adds 'css_class' CSS class attribute to every 'css_decorated_fields' fields in a form.
    """

    css_class_decorated_fields = (
        CharField,
    )

    css_class = 'form-control'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields.values():
            self.__decorate_field(field)

    def __decorate_field(self, field):
        if isinstance(field, self.css_class_decorated_fields):
            additional_css_class = field.widget.attrs.get('class')
            coupled_css_class = (additional_css_class + ' ' if additional_css_class else '') + self.css_class 
            field.widget.attrs.update({'class': coupled_css_class})

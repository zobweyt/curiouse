from django.forms.fields import CharField, ChoiceField


class CharFieldCSSClassMixin:
    """Adds custom CSS class to every CharField in a form."""

    input_css_class = 'form-control'
    input_size_css_class = 'sm'

    def __init__(self, *args, **kwargs):
        if not self.input_css_class:
            raise AttributeError('input_css_class must be provided.')

        classes = [self.input_css_class]

        if self.input_size_css_class:
            classes.append(f'{self.input_css_class}-{self.input_size_css_class}')

        formated_classes = ' '.join(classes)

        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            if isinstance(field, CharField) or isinstance(field, ChoiceField):
                field.widget.attrs.update({'class': formated_classes})

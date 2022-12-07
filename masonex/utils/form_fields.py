from django.forms.fields import CharField, ChoiceField


class InputFieldCSSClassMixin:
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

        [
            field.widget.attrs.update({'class': formated_classes}) 
            for field 
            in self.fields.values() 
            if isinstance(field, CharField) or isinstance(field, ChoiceField)
        ]

from django import forms
from .models import Product, Category
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    """ Set up the default product form """
    class Meta:
        """ Give the form fields """
        model = Product
        # All fields
        fields = '__all__'

    # Set up the image field to use custom widget
    image = forms.ImageField(
        label='Image', required=True,
        widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """ Show friendly names for categories """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        # Add classes for styling the fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'text-info bg-info-dark'

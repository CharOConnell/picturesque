from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """ Customise the look of the image entry box in add product view """
    # Set up the default variables
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Image')
    input_text = _('')
    aid = 'products/custom_widget_templates/custom_clearable_file_input.html'
    template_name = aid

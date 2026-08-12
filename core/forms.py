from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'display:none !important', 'tabindex': '-1', 'autocomplete': 'off'}),
        label='',
    )

    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your message here...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            if 'form-control' not in css:
                field.widget.attrs['class'] = f'{css} form-control'.strip()
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = f'Enter your {field.label.lower()}'

    def clean_honeypot(self):
        value = self.cleaned_data.get('honeypot', '')
        if value:
            raise forms.ValidationError('Spam detected.')
        return value

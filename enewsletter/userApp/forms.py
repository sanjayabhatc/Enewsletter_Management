from django import forms
from .models import Department,NewsLetter  # Import the Department model

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=5,
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        min_length=5,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class SignUpForm(forms.Form):
    username = forms.CharField(
        min_length=5,
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        min_length=5,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    regNo = forms.IntegerField(
        min_value=210000000,
        max_value=260000000,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    department = forms.ChoiceField(
        choices=[],  # Initially empty, will be populated in __init__
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    isAdmin = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['department'].choices = [(dept.id, dept.name) for dept in Department.objects.all()]


class UploadForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['title', 'message', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'min_length': 5, 'max_length': 500}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 12, 'min_length': 0, 'max_length': 10000}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
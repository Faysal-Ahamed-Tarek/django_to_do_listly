from django import forms


class newTask(forms.Form):
    description = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "+ New task",
                "required": "required",
            }
        ),
    )

class listly_user_form(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg rounded-3",
                "placeholder": "Enter your name",
                "required": "required",
            }
        ),
    )

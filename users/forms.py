from django import forms
from .models import User
from django.contrib.auth.hashers import make_password


class UserForm(forms.ModelForm):
    pass_1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            "placeholder": "Введите пароль"
        }),
        label="Пароль"
    )

    pass_2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            "placeholder": "Подтвердите пароль"
        }),
        label="Подтвердите пароль"
    )

    class Meta:
        model = User
        fields = ["full_name", "email", "role"]

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Введите имя пользователя"
            }),
            "email": forms.EmailInput(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                "placeholder": "Введите email"
            }),
            "role": forms.Select(attrs={
                "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            }),
        }

    def clean_email(self):
        """Email unikalligini tekshirish"""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован!")
        return email

    def clean(self):
        """Parolni tekshirish"""
        cleaned_data = super().clean()
        pass_1 = cleaned_data.get("pass_1")
        pass_2 = cleaned_data.get("pass_2")

        if pass_1 and pass_2 and pass_1 != pass_2:
            raise forms.ValidationError("Пароли не совпадают!")

        return cleaned_data

    def save(self, commit=True):
        """Parolni shifrlab saqlash"""
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["pass_1"])  # Parolni hash qilish
        if commit:
            user.save()
        return user

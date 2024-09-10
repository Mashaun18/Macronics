from django.contrib import admin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Userr

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Password confirmation')

    class Meta:
        model = Userr
        fields = ('email', 'username', 'first_name', 'last_name', 'user_type')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Userr
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'country', 'is_active', 'is_staff', 'is_superuser', 'user_type')

    def clean_password(self):
        return self.initial["password"]

class CustomUserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('user_type', 'is_active', 'is_staff')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'user_type'),
        }),
    )

    filter_horizontal = ()

admin.site.register(Userr, CustomUserAdmin)

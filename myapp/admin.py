from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Reason, Record, Agent, PhoneNumber
from django.contrib.admin import AdminSite
# Need to import this since auth models get registered on import.
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth
from rest_framework.authtoken.admin import (
    TokenProxy
)

admin.site.unregister(TokenProxy)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
admin.site.register(PhoneNumber)


# Custom form to create an Agent and User together
class AgentAdminForm(forms.ModelForm):
    user_username = forms.CharField(label="Username")
    user_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    user_email = forms.EmailField(label="Email", required=True)
    
    
    class Meta:
        model = Agent
        fields = ['user_username', 'user_password', 'user_email', 'phone_numbers']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['user_username'],
            password=self.cleaned_data['user_password'],
            email=self.cleaned_data['user_email']
        )
        agent = super().save(commit=False)
        agent.user = user
        if commit:
            agent.save()
        return agent


# class PhoneNumberInline(admin.TabularInline):  # Inline for multiple numbers
#     model = Agent
#     extra = 1  # Allows adding extra phone numbers


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    form = AgentAdminForm
    list_display = ('id', 'user', 'get_phone_numbers')
    search_fields = ('user__username',)

    # inlines = [PhoneNumberInline]  # Show phone numbers inside Agent admin

    def get_phone_numbers(self, obj):
        return ", ".join([phone.number for phone in obj.phone_numbers.all()])
    get_phone_numbers.short_description = "Phone Numbers"


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'number', 'reason', 'formatted_delay', 'time')
    list_filter = ('agent', 'reason',)
    search_fields = ('agent__user__username',)
    list_per_page = 10

    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="records.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Agent', 'Number', 'Reason', 'Delay'])

        for record in queryset:
            minutes, seconds = divmod(record.delay, 60)
            delay_formatted = f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"
            writer.writerow([record.id, record.agent, record.number, record.reason.title, delay_formatted])

        return response

    export_as_csv.short_description = "Export Selected Records as CSV"

    def formatted_delay(self, obj):
        minutes, seconds = divmod(obj.delay, 60)
        return f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"

    formatted_delay.short_description = "Delay (Formatted)"

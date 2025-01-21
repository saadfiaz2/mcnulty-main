from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Reason, Record, Agent
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


class MyAdminSite(AdminSite):
    site_header = "My Custom Admin"
    site_title = "My Admin Portal"
    index_title = "Welcome to My Admin Portal"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = 'css/custom_admin.css'
        return context


admin_site = MyAdminSite(name='myadmin')


# Custom form for adding an Agent and User together
class AgentAdminForm(forms.ModelForm):
    user_username = forms.CharField(label="Username")
    user_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    user_email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = Agent
        fields = ['user_username', 'user_password', 'user_email', 'assigned_phone_number']

    def save(self, commit=True):
        # Create a new User and link it to the Agent
        user_data = {
            'username': self.cleaned_data['user_username'],
            'password': self.cleaned_data['user_password'],
            'email': self.cleaned_data['user_email'],
        }
        user = User.objects.create_user(**user_data)
        agent = super().save(commit=False)
        agent.user = user
        if commit:
            agent.save()
        return agent


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    form = AgentAdminForm
    list_display = ('id', 'user', 'assigned_phone_number')
    search_fields = ('user__username', 'assigned_phone_number')


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'number', 'reason', 'formatted_delay')
    list_filter = ('agent', 'reason',)
    search_fields = ('agent__user__username', 'assigned_phone_number',)
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
            # Format delay using the same logic as `formatted_delay`
            minutes, seconds = divmod(record.delay, 60)
            delay_formatted = f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"
            writer.writerow([record.id, record.agent, record.number, record.reason.title, delay_formatted])

        return response


    export_as_csv.short_description = "Export Selected Records as CSV"

    def formatted_delay(self, obj):
        minutes, seconds = divmod(obj.delay, 60)
        if minutes > 0:
            return f"{minutes} min {seconds} sec"
        else:
            return f"{seconds} sec"
    
    formatted_delay.short_description = "Delay (Formatted)"

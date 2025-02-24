from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from .models import Reason, Record, Agent, PhoneNumber
from django.contrib.admin import AdminSite
import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth
from rest_framework.authtoken.admin import TokenProxy

admin.site.unregister(TokenProxy)
admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)
admin.site.register(PhoneNumber)

class AgentCreationForm(forms.ModelForm):
    """Form for creating new Agents with associated User account and phone numbers"""
    user_username = forms.CharField(label="Username")
    user_password = forms.CharField(label="Password", widget=forms.PasswordInput)
    user_email = forms.EmailField(label="Email", required=True)
    new_numbers = forms.CharField(
        label="New Phone Numbers (comma-separated)",
        required=False,
        help_text="Enter new phone numbers, separated by commas."
    )
    
    class Meta:
        model = Agent
        fields = ['phone_numbers']

    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['user_username'],
            password=self.cleaned_data['user_password'],
            email=self.cleaned_data['user_email']
        )
        # Create the Agent and link to User
        agent = super().save(commit=False)
        agent.user = user
        if commit:
            agent.save()
            self.save_m2m()  # Save many-to-many relationships

        # Process new phone numbers
        new_numbers = self.cleaned_data.get('new_numbers', '')
        numbers_list = [num.strip() for num in new_numbers.split(',') if num.strip()]
        for number in numbers_list:
            phone_number, created = PhoneNumber.objects.get_or_create(number=number)
            agent.phone_numbers.add(phone_number)

        return agent

class AgentChangeForm(forms.ModelForm):
    """Form for editing existing Agents with phone number management"""
    new_numbers = forms.CharField(
        label="New Phone Numbers (comma-separated)",
        required=False,
        help_text="Enter new phone numbers, separated by commas."
    )

    class Meta:
        model = Agent
        fields = ['phone_numbers']

    def save(self, commit=True):
        agent = super().save(commit=commit)
        
        if commit:
            self.save_m2m()  # Ensure existing M2M relationships are saved

        # Process new phone numbers
        new_numbers = self.cleaned_data.get('new_numbers', '')
        numbers_list = [num.strip() for num in new_numbers.split(',') if num.strip()]
        for number in numbers_list:
            phone_number, created = PhoneNumber.objects.get_or_create(number=number)
            agent.phone_numbers.add(phone_number)

        return agent

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_phone_numbers')
    search_fields = ('user__username',)
    filter_horizontal = ('phone_numbers',)

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return AgentCreationForm
        else:
            return AgentChangeForm

    def get_phone_numbers(self, obj):
        return ", ".join([phone.number for phone in obj.phone_numbers.all()])
    get_phone_numbers.short_description = "Phone Numbers"

# [Keep the ReasonAdmin and RecordAdmin classes unchanged from original code]

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

    def formatted_delay(self, obj):
        minutes, seconds = divmod(obj.delay, 60)
        return f"{minutes} min {seconds} sec" if minutes > 0 else f"{seconds} sec"

    export_as_csv.short_description = "Export Selected Records as CSV"
    formatted_delay.short_description = "Delay (Formatted)"
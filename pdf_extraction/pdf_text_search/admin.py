from django.contrib import admin

# Register your models here.
from .models import Reasoning

@admin.register(Reasoning)
class ReasoningAdmin(admin.ModelAdmin):
    list_display = ("content", "date", "version_tag", "security_tag" ,"access_tag")
    search_fields = ("content", "version_tag", "security_tag","access_tag")
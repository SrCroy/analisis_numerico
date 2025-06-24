from django.contrib import admin
from .models import DifferenceDividedHistory

@admin.register(DifferenceDividedHistory)
class DifferenceDividedHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'function', 'x_value', 'h_value', 'created_at')
    search_fields = ('user__username', 'function')
    list_filter = ('created_at',)

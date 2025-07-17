from django.contrib import admin
from .models import MachineLog


@admin.register(MachineLog)
class MachineLogAdmin(admin.ModelAdmin):
    """Admin configuration for MachineLog model."""
    
    list_display = [
        'machine_id',
        'operator_id', 
        'log_timestamp',
        'engine_hours',
        'fuel_used_l',
        'load_cycles',
        'seatbelt_status',
        'safety_alert_triggered'
    ]
    
    list_filter = [
        'log_timestamp',
        'machine_id',
        'operator_id',
        'seatbelt_status',
        'safety_alert_triggered',
        'created_at'
    ]
    
    search_fields = [
        'machine_id',
        'operator_id'
    ]
    
    date_hierarchy = 'log_timestamp'
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('machine_id', 'operator_id', 'log_timestamp')
        }),
        ('Operation Metrics', {
            'fields': ('engine_hours', 'fuel_used_l', 'load_cycles', 'idling_time_min')
        }),
        ('Safety Information', {
            'fields': ('seatbelt_status', 'safety_alert_triggered')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Enable bulk actions
    actions = ['export_selected_logs']
    
    def export_selected_logs(self, request, queryset):
        """Custom admin action to export selected logs."""
        # This could be expanded to generate CSV/Excel exports
        self.message_user(request, f"Selected {queryset.count()} logs for export")
    export_selected_logs.short_description = "Export selected logs"

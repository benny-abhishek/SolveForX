from django.db import models
from django.utils import timezone


class MachineLog(models.Model):
    """
    Model to store machine operation logs.
    
    This model tracks various operational metrics for machines including
    engine hours, fuel consumption, load cycles, and safety status.
    """
    
    # Primary key is automatically created by Django as 'id' (SERIAL)
    log_timestamp = models.DateTimeField(
        help_text="Timestamp when the log entry was recorded"
    )
    
    machine_id = models.CharField(
        max_length=50,
        help_text="Unique identifier for the machine"
    )
    
    operator_id = models.CharField(
        max_length=50,
        help_text="Identifier for the machine operator"
    )
    
    engine_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Total engine hours recorded"
    )
    
    fuel_used_l = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Fuel consumed in liters"
    )
    
    load_cycles = models.IntegerField(
        null=True,
        blank=True,
        help_text="Number of load cycles performed"
    )
    
    idling_time_min = models.IntegerField(
        null=True,
        blank=True,
        help_text="Time spent idling in minutes"
    )
    
    SEATBELT_CHOICES = [
        ('FASTENED', 'Fastened'),
        ('UNFASTENED', 'Unfastened'),
        ('UNKNOWN', 'Unknown'),
    ]
    
    seatbelt_status = models.CharField(
        max_length=20,
        choices=SEATBELT_CHOICES,
        null=True,
        blank=True,
        help_text="Status of operator seatbelt"
    )
    
    safety_alert_triggered = models.BooleanField(
        null=True,
        blank=True,
        help_text="Whether a safety alert was triggered during operation"
    )
    
    # Additional Django fields for better management
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'machine_logs'  # This will create the exact table name you specified
        ordering = ['-log_timestamp']  # Order by most recent first
        verbose_name = 'Machine Log'
        verbose_name_plural = 'Machine Logs'
        
        # Add database indexes for better performance
        indexes = [
            models.Index(fields=['machine_id', 'log_timestamp']),
            models.Index(fields=['operator_id']),
            models.Index(fields=['log_timestamp']),
        ]
    
    def __str__(self):
        """String representation of the model."""
        return f"Machine {self.machine_id} - {self.log_timestamp}"
    
    def save(self, *args, **kwargs):
        """Override save to set log_timestamp if not provided."""
        if not self.log_timestamp:
            self.log_timestamp = timezone.now()
        super().save(*args, **kwargs)

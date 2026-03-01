import uuid
from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Filters out deleted records by default."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class DeletedObjectManager(models.Manager):
    """Returns only soft-deleted records."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class BaseModel(models.Model):
    # UUIDs are better for security/distributed systems than auto-incrementing IDs
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Audit trail fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Soft delete fields
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Managers
    objects = SoftDeleteManager()          # Default: excludes deleted records
    all_objects = models.Manager()         # All records including deleted
    deleted_objects = DeletedObjectManager()  # Only deleted records

    def __str__(self):
        return f"{self.__class__.__name__}({self.id})"

    def delete(self, **kwargs):
        """Soft delete: just set the timestamp."""
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        """Undo a soft delete, making the record active again."""
        self.deleted_at = None
        self.is_active = True
        self.save()

    def hard_delete(self, **kwargs):
        """Actually remove from DB if absolutely necessary."""
        super().delete(**kwargs)

    class Meta:
        abstract = True
        
        
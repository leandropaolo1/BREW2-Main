from Accounts.models import AccountModel
from django.db import models
import uuid


class CategoryModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    public_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    private_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        unique=True,
        blank=False,
        null=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    def __str__(self):
        return self.name


class CommentModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    public_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    private_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    account_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    comment = models.CharField(
        max_length=255,
        blank=False,
        null=True)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name_plural = "Comment Models"
        verbose_name = "Comment Model"
        ordering = ['-date_posted']

    def __str__(self):
        return str(self.id)


class DownVoteModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    public_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    private_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    account_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name_plural = "DownVote Models"
        verbose_name = "DownVote Model"
        ordering = ['-date_posted']

    def __str__(self):
        return str(self.account_relation.username)


class UpVoteModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    public_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    private_uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=False,
        max_length=255,
        editable=False,
        unique=True,
        blank=False,
        null=False)

    account_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name_plural = "UpVote Models"
        verbose_name = "UpVote Model"
        ordering = ['-date_posted']

    def __str__(self):
        return str(self.account_relation.username)

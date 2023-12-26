from Singletons.models import CategoryModel, CommentModel, UpVoteModel, DownVoteModel
from django.utils.translation import gettext_lazy as _
from Accounts.models import AccountModel
from django.utils import timezone
from django.urls import reverse
from django.db import models
from PIL import Image
import uuid


class BrewModel(models.Model):
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

    header_image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,)

    header = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True)

    content = models.TextField(
        max_length=255,
        unique=False,
        blank=False,
        null=False)

    category_relation = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    views = models.IntegerField(
        blank=False,
        null=False,
        default=0)

    upVote_relations = models.ManyToManyField(
        AccountModel)

    downVotes_relations = models.ManyToManyField(
        AccountModel)

    comment_relations = models.ManyToManyField(
        CommentModel)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    class Meta:
        verbose_name_plural = "Brew Models"
        verbose_name = "Brew Model"
        ordering = ['-date_created']

    def numUpVotes(self):
        return self.upVote_relations.count()

    def numDownVotes(self):
        return self.downVotes_relations.count()

    @property
    def numComments(self):
        return self.comment_relations.count()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        header_image = Image.open(self.header_image.path)
        if header_image.height > 300 or header_image.width > 300:
            output_size = (1100, 1000)
            header_image.thumbnail(output_size)
            header_image.save(self.header_image.path)

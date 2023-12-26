from django.utils.translation import gettext_lazy as _
from Singletons.models import CategoryModel
from Accounts.models import AccountModel
from Brews.models import BrewModel
from django.db import models
from PIL import Image
import uuid


class RoomsModel(models.Model):
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

    memberList_relation = models.ForeignKey(
        'models.MemberListModel',
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    brew_relations = models.ManyToManyField(
        BrewModel)

    category = models.ForeignKey(
        CategoryModel,
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    account_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    name = models.CharField(
        max_length=255,
        editable=True,
        unique=True,
        blank=False,
        null=False)

    description = models.CharField(
        max_length=255,
        editable=True,
        unique=True,
        blank=False,
        null=False)

    image = models.ImageField(
        upload_to='profile_pics',
        default="tent.jpg",
        blank=True,
        null=True)

    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    @property
    def numMembers(self):
        return self.memberList_relation.account_relations.count()

    @property
    def numBrews(self):
        return self.brew_relations.count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)

    class Meta:
        verbose_name_plural = "Room Models"
        verbose_name = "Room Model"
        ordering = ['-date_created']

    def __str__(self):
        return self.account_relation.username

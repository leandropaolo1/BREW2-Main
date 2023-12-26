from Accounts.models import AccountModel
from Rooms.models import RoomsModel
from django.db import models
import uuid


class FriendListModel(models.Model):
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

    account_relations = models.ManyToManyField(
        AccountModel)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    def addAccount(self, account_instance: AccountModel):
        if not account_instance in self.account_relations.all():
            self.account_relations.add(account_instance)
            self.save()

    def removeAccount(self, account_instance: AccountModel):
        if account_instance in self.account_relations.all():
            self.account_relations.remove(account_instance)

    def findAccount(self, account_instance: AccountModel):
        if account_instance in self.account_relations.all():
            return True
        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Friend List Models"
        verbose_name = "Friend List Model"
        ordering = ['-date_created']

    def __str__(self):
        return self.account_relation.username


class FriendRequestModel(models.Model):
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

    sender_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    receiver_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    def accept(self):
        try:
            receiver_friend_list = FriendListModel.objects.get(
                account_reltion=self.receiver_relation)
            receiver_friend_list.addAccount(self.sender_relation)
            sender_friend_list = FriendListModel.objects.get(
                account_relation=self.sender_relation)
            sender_friend_list.addAccount(self.receiver_relation)
            self.is_active = False
            self.save()
        except:
            pass

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Friend Request Models"
        verbose_name = "Friend Request Model"
        ordering = ['-date_created']

    def __str__(self):
        return self.sender_relation.username


class MemberListModel(models.Model):
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

    room_relation = models.OneToOneField(
        RoomsModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    account_relations = models.ManyToManyField(
        AccountModel,
        blank=True)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    def addAccount(self, account_instance: AccountModel):
        if not account_instance in self.account_relations.all():
            self.account_relations.add(account_instance)
            self.save()

    def removeAccount(self, account_instance: AccountModel):
        if account_instance in self.account_relations.all():
            self.account_relations.remove(account_instance)

    def findAccount(self, account_instance: AccountModel):
        if account_instance in self.account_relations.all():
            return True
        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Member List Models"
        verbose_name = "Member List Model"
        ordering = ['-date_created']

    def __str__(self):
        return self.room_relation.name


class MemberRequestModels(models.Model):
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

    sender_relation = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    receiver_relation = models.ForeignKey(
        RoomsModel,
        on_delete=models.CASCADE,
        blank=False,
        null=False)

    is_active = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    date_created = models.DateTimeField(
        auto_now_add=True,
        editable=False)

    date_updated = models.DateTimeField(
        auto_now=True)

    def accept(self):
        try:
            receiver_friend_list = FriendListModel.objects.get(
                account_reltion=self.receiver_relation)
            receiver_friend_list.addAccount(self.sender_relation)
            sender_friend_list = FriendListModel.objects.get(
                account_relation=self.sender_relation)
            sender_friend_list.addAccount(self.receiver_relation)
            self.is_active = False
            self.save()
        except:
            pass

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Room List Models"
        verbose_name = "Room List Model"
        ordering = ['-date_created']

    def __str__(self):
        return self.receiver_relation.name

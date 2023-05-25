"""This module define the structure of stored data, including the field types
and possibly also their maximum size, default values, selection list options,
help text for documentation, label text for forms, etc."""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from PIL import Image
from django.urls import reverse
from django.utils.safestring import mark_safe

Role = (("User", "USER"), ("Doctor", "DOCTOR"), ("Admin", "ADMIN"))


class user(AbstractUser):
    """This class corresponds to the user table in the database."""

    passphrase = models.TextField(max_length=500)
    Address = models.CharField(max_length=100)
    privateKey = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="static/profile", null=True, blank=True)
    user_token = models.CharField(max_length=100, default=uuid.uuid4)
    role = models.CharField(max_length=10, choices=Role, default="User")

    # show user profile picture
    def user_profile(self):
        return mark_safe(
            '<img style="border-radius:50%;" src="{url}" width="50" height="50" />'.format(
                url=self.profile_pic.url
            )
        )

    user_profile.short_description = "Profile Picture"
    user_profile.allow_tags = True


class Contacts(models.Model):
    """This class corresponds to the Contact table in the database."""

    user = models.ForeignKey(user, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="static/contact", null=True, blank=True)
    name = models.CharField(max_length=60)
    contact_address = models.CharField(max_length=60)

    def user_profile(self):
        return mark_safe(
            '<img style="border-radius:50%;" src="{url}" width="50" height="50" />'.format(
                url=self.profile_pic.url
            )
        )

    user_profile.short_description = "Profile Picture"
    user_profile.allow_tags = True

    def __str__(self):
        """This function returns the name of the contact."""
        return "" + self.name

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"


class FAQs(models.Model):
    """This class corresponds to the FAQ table in the database."""

    Questions = models.TextField(max_length=500)
    Answer = models.TextField(max_length=1000)
    is_Active = models.BooleanField()

    def __str__(self):
        """It is used to display the first few characters of the text field"""
        return "" + self.Questions

    class Meta:
        verbose_name = "FAQs"
        verbose_name_plural = "FAQs"


class Messages(models.Model):
    """This class corresponds to the Direct_message table in the database."""

    User = models.ForeignKey(user, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(user, on_delete=models.CASCADE, related_name="from_user")
    recipient = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="to_user"
    )
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        """_summary_

        Args:
            from_user: Object of Current User
            to_user: Object of Recipient
            body: Message Body

        Returns: Object of Sent Message
        """
        sender_message = Messages(
            User=from_user, sender=from_user, recipient=to_user, body=body, is_read=True
        )
        sender_message.save()

        recipient_message = Messages(
            User=to_user,
            sender=from_user,
            body=body,
            recipient=from_user,
        )
        recipient_message.save()
        return sender_message

    def get_messages(User):
        """_summary_

        Args:
            User: Object of Current User

        Return: List of Messages
        """
        messages = (
            Messages.objects.filter(User=User)
            .values("recipient")
            .annotate(last=Max("date"))
            .order_by("-last")
        )
        users = []
        for message in messages:
            users.append(
                {
                    "user": user.objects.get(pk=message["recipient"]),
                    "last": message["last"],
                    "last_message": Messages.objects.filter(
                        User=User, recipient=message["recipient"]
                    )
                    .order_by("-date")
                    .first(),
                    "unread": Messages.objects.filter(
                        User=User, recipient__pk=message["recipient"], is_read=False
                    ).count(),
                }
            )
        return users

    def get_unreadmsg(User):
        """_summary_

        Args:
            User: Object of Current User

        Return: List of Unread Messages
        """
        messages = (
            Messages.objects.filter(User=User, is_read=False)
            .values("recipient")
            .annotate(last=Max("date"))
            .order_by("-last")
        )
        users = []
        for message in messages:
            users.append(
                {
                    "user": user.objects.get(pk=message["recipient"]),
                    "last": message["last"],
                    "last_message": Messages.objects.filter(
                        User=User, recipient=message["recipient"]
                    )
                    .order_by("-date")
                    .first(),
                    "unread": Messages.objects.filter(
                        User=User, recipient__pk=message["recipient"], is_read=False
                    ).count(),
                }
            )
        return users

    class Meta:
        verbose_name = "Message"


class TokenRequests(models.Model):
    """This class corresponds to the TokenRequests table in the database."""

    User = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="Request_user"
    )
    sender = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="Request_from_user"
    )
    recipient = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="Request_to_user"
    )
    token = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_rejected = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def send_token(from_user, to_user, token):
        """_summary_

        Args:
            from_user: Object of Current User
            to_user: Object of Recipient
            body: Message Body

        Returns: Object of Token
        """
        sender_token = TokenRequests(
            User=from_user, sender=from_user, recipient=to_user, token=token
        )
        sender_token.save()
        return sender_token

    class Meta:
        verbose_name = "Token  Request"


class Support(models.Model):
    """This class correcsponds to the Support table in the database."""

    User = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="support_user"
    )
    sender = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="Support_from_user"
    )
    recipient = models.ForeignKey(
        user, on_delete=models.CASCADE, related_name="Support_to_user"
    )
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        """_summary_

        Args:
            from_user: Object of Current User
            to_user: Object of Recipient
            body: Message Body

        Returns: Object of Message
        """
        sender_message = Support(
            User=from_user, sender=from_user, recipient=to_user, body=body, is_read=True
        )
        sender_message.save()

        recipient_message = Support(
            User=to_user,
            sender=from_user,
            body=body,
            recipient=from_user,
        )
        recipient_message.save()
        return sender_message

    def get_messages(User):
        """_summary_

        Args:
            User: Object of Current User

        Returns: List of Messages
        """
        messages = (
            Support.objects.filter(User=User)
            .values("recipient")
            .annotate(last=Max("date"))
            .order_by("-last")
        )
        users = []
        for message in messages:
            users.append(
                {
                    "user": user.objects.get(pk=message["recipient"]),
                    "last": message["last"],
                    "last_message": Support.objects.filter(
                        User=User, recipient=message["recipient"]
                    )
                    .order_by("-date")
                    .first(),
                    "unread": Support.objects.filter(
                        User=User, recipient__pk=message["recipient"], is_read=False
                    ).count(),
                }
            )
        return users

    class Meta:
        verbose_name = "Support"
        verbose_name_plural = "Support"


class Email_verify(models.Model):
    """This class corresponds to the Email_verify table in the database."""

    User = models.OneToOneField(user, on_delete=models.CASCADE)
    email_verify_token = models.TextField(max_length=1000, blank=True, null=True)
    verify = models.BooleanField(default=False)


class admin_data(models.Model):
    """This class corresponds to the admin_data table in the database."""

    key = models.CharField(max_length=10, blank=True, null=True)
    values = models.TextField(max_length=500, blank=True, null=True)


class HealthRecords(models.Model):
    """This class corresponds to the HealthRecords table in the database."""

    User = models.OneToOneField(user, on_delete=models.CASCADE)
    NFT_id = models.TextField(max_length=1000, blank=True, null=True)
    NFT_trxn_hash = models.TextField(max_length=1000, blank=True, null=True)
    NFT_image = models.ImageField(upload_to="static/NFT", null=True, blank=True)
    personal = models.BooleanField(default=True)
    emergency = models.BooleanField(default=True)
    PIN = models.CharField(max_length=4, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.PIN:
            self.PIN = None
        super(HealthRecords, self).save(*args, **kwargs)

    def user_profile(self):
        return mark_safe(
            '<img style="border-radius:50%;" src="{url}" width="50" height="50" />'.format(
                url=self.NFT_image.url
            )
        )

    user_profile.short_description = "NFT Image"
    user_profile.allow_tags = True

    class Meta:
        verbose_name = "Health  Record"

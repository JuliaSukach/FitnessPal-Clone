import os
import asyncio
from tortoise import models, fields
from tortoise.signals import pre_save
from enum import IntEnum
from hashlib import sha3_224
from fitnessapp.db import TextCryptoField


class UserStatus(IntEnum):
    ADMIN = 5
    STAFF = 4
    SIMPLE = 3

    def __str__(self):
        return self.name


class MealType(IntEnum):
    BREAKFAST = 0
    LUNCH = 1
    DINNER = 2
    SNACKS = 3

    def __str__(self):
        return self.name


class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=120, unique=True)
    password = TextCryptoField(validators=[])
    email = TextCryptoField(validators=[])
    is_active = fields.BooleanField(default=False)
    created = fields.DatetimeField(auto_now_add=True)
    status = fields.IntEnumField(UserStatus, default=UserStatus.SIMPLE)
    refresh = fields.TextField(validators=[], null=True)
    image_name = fields.CharField(max_length=255, null=True)

    def __str__(self):
        return self.username

    class Meta:
        table = 'users'
        ordering = ('-created',)

    def make_passwd(self):
        hashed_passwd = sha3_224(self.password.encode('utf-8')).hexdigest()
        salt = sha3_224(os.urandom(24).hex().encode('utf-8')).hexdigest()
        mix = ''.join([a + b for a, b in zip(salt, hashed_passwd)])
        mixed_hash = sha3_224(mix.encode('utf-8')).hexdigest()
        self.password = ''.join([a + b for a, b in zip(salt, mixed_hash)])

    async def check_password(self, password):
        salt = self.password[::2]
        passwd = self.password[1::2]
        hashed_passwd = sha3_224(password.encode('utf-8')).hexdigest()
        mix = ''.join([a + b for a, b in zip(salt, hashed_passwd)])
        mixed_hash = sha3_224(mix.encode('utf-8')).hexdigest()
        if passwd == mixed_hash:
            return True
        await asyncio.sleep(3)
        return False


class Post(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('user.User', related_name='posts')
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('user.User', related_name='comments')
    post = fields.ForeignKeyField('user.Post', related_name='comments')
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.content


@pre_save(User)
async def hash_password(sender, instance, using_db, updated_fields):
    if instance.id is None or 'password' in updated_fields:
        instance.make_passwd()


class Message(models.Model):
    id = fields.IntField(pk=True)
    sender = fields.ForeignKeyField('user.User', related_name='sent_messages')
    recipient = fields.ForeignKeyField('user.User', related_name='received_messages')
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    sent = fields.BooleanField(default=False)

    class Meta:
        table = 'messages'


class Meal(models.Model):
    user = fields.ForeignKeyField('user.User', related_name='meals')
    name = fields.CharField(max_length=255)
    calories = fields.TextField()
    meal_type = fields.IntEnumField(MealType, default=MealType.BREAKFAST)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = 'meals'
        ordering = ('-created_at',)



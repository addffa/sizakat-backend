from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from graphene_django import DjangoObjectType


class User(AbstractUser):
    """
    Custom user model for sizakat.
    username, email, and name model is inherited from AbstractUser.
    """

    ROLE_CHOICES = [('ADMIN', 'Admin'), ('STAFF', 'Staff')]

    address = models.CharField(_('address'), max_length=150, blank=True)
    role = models.CharField(
        _('role'),
        max_length=15,
        choices=ROLE_CHOICES,
        default='STAFF'
    )

    # just use 'name' instead of django user 'first name' and 'last name'
    first_name = None
    last_name = None
    name = models.CharField(_('name'), max_length=50)

    # TODO: create image field for photo

    def __str__(self):
        return '{} - {}'.format(self.username, self.role)


class Muzakki(models.Model):
    no_ktp = models.CharField(_('id number'), max_length=20, blank=True)
    name = models.CharField(_('name'), max_length=50)
    address = models.CharField(_('address'), max_length=150)
    email = models.EmailField(_('email address'), blank=True)
    phone = models.CharField(_('phone number'), max_length=15, blank=True)
    created_date = models.DateTimeField(
        _('created date'),
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Period(models.Model):
    year = models.PositiveSmallIntegerField(unique=True)
    desc = models.CharField(_('description'), max_length=50)
    is_active = models.BooleanField(_('active status'), default=False)

    def get_active_period():
        return Period.objects.get(is_active=True)

    def __str__(self):
        if self.is_active:
            return '{} (Active)'.format(self.year)
        return self.year


class ZakatType(models.Model):
    name = models.CharField(_('name'), max_length=20)
    desc = models.CharField(_('description'), max_length=150, blank=True)

    def __str__(self):
        return self.name


class ZakatQuality(models.Model):
    quality_desc = models.CharField(_('description'), max_length=50)
    quality_value = models.PositiveIntegerField()
    zakat_type = models.ForeignKey(
        ZakatType,
        models.CASCADE,
        verbose_name=_('zakat type')
    )

    def __str__(self):
        return self.quality_desc


class ZakatPayment(models.Model):
    payment_code = models.CharField(
        _('payment code'),
        max_length=30,
        unique=True
    )
    payer_name = models.CharField(_('payer name'), max_length=50)
    payer_address = models.CharField(_('payer address'), max_length=150)
    payer_phone = models.CharField(_('payer phone'), max_length=15, blank=True)
    payer_email = models.EmailField(_('payer email'), blank=True)
    payment_date = models.DateTimeField(
        _('payment date'),
        auto_now_add=True
    )
    receiver = models.ForeignKey(
        User,
        models.CASCADE,
        verbose_name=_('payment receiver')
    )
    period = models.ForeignKey(
        Period,
        models.CASCADE,
        verbose_name=_('payment period')
    )

    def generate_payment_code(self):
        self.payment_code = '{}{}{}'.format(
            'TRANSC', self.payment_date.strftime('%d%m%Y'), self.pk)
        self.save()

    def __str__(self):
        return '{} - {}'.format(self.payment_code, self.payer_name)


class ZakatTransaction(models.Model):
    TRANSACTION_TYPES = [('MONEY', 'Uang'), ('RICE', 'Beras'),
                         ('CHECK', 'Cek'), ('GOLD', 'Emas')]

    income_value = models.PositiveIntegerField(_('income value'), default=0)
    income_goods = models.PositiveIntegerField(_('income goods'), default=0)
    muzakki = models.ForeignKey(Muzakki, models.CASCADE)
    transaction_type = models.CharField(
        _('transaction type'),
        max_length=15,
        choices=TRANSACTION_TYPES,
        default='MONEY'
    )
    zakat_quality = models.ForeignKey(
        ZakatQuality,
        models.CASCADE,
        verbose_name=_('zakat quality')
    )
    zakat_payment = models.ForeignKey(
        ZakatPayment,
        models.CASCADE,
        verbose_name=_('zakat payment')
    )

    def __str__(self):
        return '{} - {}'.format(self.zakat_payment.payment_code, self.muzakki.name)

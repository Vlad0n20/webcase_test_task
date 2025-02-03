from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.postgres.indexes import HashIndex

from abstract.models import BaseModel, WhoDidIt
from apps.discount.services.generate_promo_code import PromoCodeGenerator


class PromoCode(BaseModel, WhoDidIt):
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = 'Promo code'
        verbose_name_plural = 'Promo codes'
        indexes = [
            HashIndex(fields=['code'])
        ]

class PercentageDiscount(BaseModel):
    discount = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Percentage discount'
        verbose_name_plural = 'Percentage discounts'

class FixedDiscount(BaseModel):
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Fixed discount'
        verbose_name_plural = 'Fixed discounts'

class AmountDiscount(BaseModel):
    discount = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Amount discount'
        verbose_name_plural = 'Amount discounts'

class SetDiscount(BaseModel):
    constrain = models.JSONField()

    # в constrain зберігається умови для знижки
    # якщо умова це кількість товарів, то вказується кількість товарів
    # та їх id або ід категорії до якої вони належать

    class Meta:
        verbose_name = 'Set discount'
        verbose_name_plural = 'Set discounts'

class AdditionalProductDiscount(BaseModel):
    for_product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='additional_product_product')
    constrain = models.JSONField()
    gift_product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='additional_product_gift')

    class Meta:
        verbose_name = 'Additional product discount'
        verbose_name_plural = 'Additional product discounts'

class GiftForSetDiscount(BaseModel):
    constrain = models.JSONField()
    gift_product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='gift_for_set_product')

    class Meta:
        verbose_name = 'Gift for set discount'
        verbose_name_plural = 'Gift for set discounts'

class Discount(BaseModel, WhoDidIt):
    class DiscountTypeChoices(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        FIXED = 'fixed', 'Fixed'
        AMOUNT = 'amount', 'Amount'
        SET = 'set', 'Set'
        ADDITIONAL_PRODUCT = 'additional_product', 'Additional product'
        GIFT_FOR_SET = 'gift_for_set', 'Gift for set'

    promo_code = models.CharField(max_length=20, unique=True, default=PromoCodeGenerator().create_promo_code())
    discount_type = models.CharField(max_length=20, choices=DiscountTypeChoices.choices)
    content_type = models.ForeignKey(ContentType, related_name='discount_subtypes',
                                          on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    discount = GenericForeignKey('content_type', 'object_id')
    is_active = models.BooleanField(default=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'
        indexes = [
            HashIndex(fields=['promo_code'])
        ]


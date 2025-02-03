from rest_framework import serializers

from utils.fields import ChoicesField
from apps.discount import models

class PercentageDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PercentageDiscount
        fields = ['discount']

class FixedDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FixedDiscount
        fields = ['discount']

class AmountDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AmountDiscount
        fields = ['discount']

class SetDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SetDiscount
        fields = ['constrain']

class AdditionalProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdditionalProductDiscount
        fields = ['for_product', 'constrain', 'gift_product']

class GiftForSetDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GiftForSetDiscount
        fields = ['constrain', 'gift_product']


class DiscountDetailSerializer(serializers.ModelSerializer):
    discount_type = ChoicesField(models.Discount.DiscountTypeChoices)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        discount_type = instance.discount_type
        match discount_type:
            case models.Discount.DiscountTypeChoices.PERCENTAGE:
                data['discount'] = PercentageDiscountSerializer(instance.discount).data
            case models.Discount.DiscountTypeChoices.FIXED:
                data['discount'] = FixedDiscountSerializer(instance.discount).data
            case models.Discount.DiscountTypeChoices.AMOUNT:
                data['discount'] = AmountDiscountSerializer(instance.discount).data
            case models.Discount.DiscountTypeChoices.SET:
                data['discount'] = SetDiscountSerializer(instance.discount).data
            case models.Discount.DiscountTypeChoices.ADDITIONAL_PRODUCT:
                data['discount'] = AdditionalProductDiscountSerializer(instance.discount).data
            case models.Discount.DiscountTypeChoices.GIFT_FOR_SET:
                data['discount'] = GiftForSetDiscountSerializer(instance.discount).data

        return data

    class Meta:
        model = models.Discount
        fields = ['id', 'promo_code', 'discount_type', 'is_active', 'start_datetime', 'end_datetime']


class DiscountDataSerializer(serializers.Serializer):
    discount_count = serializers.IntegerField(required=False)
    constrain = serializers.JSONField(allow_null=True, required=False)
    for_product = serializers.IntegerField(required=False)
    gift_product = serializers.IntegerField(required=False)


class DiscountCreateSerializer(serializers.ModelSerializer):
    promo_code = serializers.CharField(max_length=20, required=False)
    discount_data = DiscountDataSerializer(write_only=True)

    def get_fields(self):
        # почав робити це для того щоб у свагері відображались правильні поля
        # але потім зрозумів що це не буде працювати оскільки на момент прогрузки документації
        # не буде відомо який тип знижки вибрав користувач

        fields = super().get_fields()
        discount_type = self.context.get('request').data.get('discount_type')
        if discount_type:
            match discount_type:
                case models.Discount.DiscountTypeChoices.PERCENTAGE:
                    fields['discount'] = serializers.IntegerField()
                case models.Discount.DiscountTypeChoices.FIXED:
                    fields['discount'] = serializers.DecimalField(max_digits=10, decimal_places=2)
                case models.Discount.DiscountTypeChoices.AMOUNT:
                    fields['discount'] = serializers.IntegerField()
                case models.Discount.DiscountTypeChoices.SET:
                    fields['discount'] = serializers.JSONField()
                # case models.Discount.DiscountTypeChoices.ADDITIONAL_PRODUCT:
                #     fields['discount'] = AdditionalProductDiscountSerializer()
                # case models.Discount.DiscountTypeChoices.GIFT_FOR_SET:
                #     fields['discount'] = GiftForSetDiscountSerializer()
        return fields


    def validate_promo_code(self, value):
        if models.PromoCode.objects.filter(code=value).exists():
            raise serializers.ValidationError('Promo code already exists')
        return value


    def create(self, validated_data):
        if code := validated_data.get('promo_code'):
            models.PromoCode.objects.create(code=code)

        discount_type = validated_data.get('discount_type')
        discount_data = validated_data.pop('discount_data')
        discount = validated_data.pop('discount')
        match discount_type:
            case models.Discount.DiscountTypeChoices.PERCENTAGE:
                sub_item = models.PercentageDiscount.objects.create(discount=discount_data.get('discount_count'))
            case models.Discount.DiscountTypeChoices.FIXED:
                sub_item = models.FixedDiscount.objects.create(discount=discount_data.get('discount_count'))
            case models.Discount.DiscountTypeChoices.AMOUNT:
                sub_item = models.AmountDiscount.objects.create(discount=discount_data.get('discount_count'))
            case models.Discount.DiscountTypeChoices.SET:
                sub_item = models.SetDiscount.objects.create(constrain=discount_data.get('constrain'))
            case models.Discount.DiscountTypeChoices.ADDITIONAL_PRODUCT:
                sub_item = models.AdditionalProductDiscount.objects.create(
                    for_product_id=discount_data.get('for_product'),
                    constrain=discount_data.get('constrain'),
                    gift_product_id=discount_data.get('gift_product'),
                )
            case models.Discount.DiscountTypeChoices.GIFT_FOR_SET:
                sub_item = models.GiftForSetDiscount.objects.create(
                    constrain=discount_data.get('constrain'),
                    gift_product_id=discount_data.get('gift_product'),
                )
            case _:
                raise ValueError('Unknown discount type')
        return models.Discount.objects.create(discount=sub_item, object_id=sub_item.id, **validated_data)


    class Meta:
        model = models.Discount
        fields = ['promo_code', 'discount_type', 'discount_data', 'start_datetime', 'end_datetime']


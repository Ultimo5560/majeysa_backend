from rest_framework import serializers

# class DessertDataSerializer(serializers.Serializer):
#     priceOfDessert = serializers.FloatField(required=False, allow_null=True)
#     countPersons = serializers.IntegerField(required=False, allow_null=True)
#     styleDessert = serializers.CharField(required=False, allow_null=True)
#     savorDessert = serializers.CharField(required=False, allow_null=True)
#     filling = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     dessert = serializers.CharField(required=False, allow_null=True)
#     firstColor = serializers.CharField(required=False, allow_null=True)
#     secondColor = serializers.CharField(required=False, allow_null=True)
#     imageRef = serializers.URLField(required=False, allow_null=True)
#     dateCollectDessert = serializers.CharField(required=False, allow_null=True)
#     hourCollectDessert = serializers.TimeField(required=False, allow_null=True)

class PaymentSerializer(serializers.Serializer):
    transaction_amount = serializers.FloatField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    cardholderEmail = serializers.EmailField(required=False, allow_null=True)


class SendMailFinishSerializar(serializers.Serializer):
    # dataPayer
    token = serializers.CharField(required=False, allow_null=True)
    payment_method_id = serializers.CharField(required=False, allow_null=True)
    inputName = serializers.CharField(required=False, allow_null=True)
    inputEmail = serializers.EmailField(required=False, allow_null=True)
    inputCelPhone = serializers.CharField(required=False, allow_null=True)
    inputMsg = serializers.CharField(required=False, allow_null=True)

    priceOfDessert = serializers.FloatField(required=False, allow_null=True)
    countPersons = serializers.IntegerField(required=False, allow_null=True)
    styleDessert = serializers.CharField(required=False, allow_null=True)
    savorDessert = serializers.CharField(required=False, allow_null=True)
    filling = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dessert = serializers.CharField(required=False, allow_null=True)
    firstColor = serializers.CharField(required=False, allow_null=True)
    secondColor = serializers.CharField(required=False, allow_null=True)
    imageRef = serializers.URLField(required=False, allow_null=True)
    dateCollectDessert = serializers.CharField(required=False, allow_null=True)
    hourCollectDessert = serializers.TimeField(required=False, allow_null=True)
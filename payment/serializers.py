from rest_framework import serializers

class DessertDataSerializer(serializers.Serializer):
    countPersons = serializers.IntegerField(required=False, allow_null=True)
    styleDessert = serializers.CharField(required=False, allow_null=True)
    savorDessert = serializers.CharField(required=False, allow_null=True)
    filling = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dessert = serializers.CharField(required=False, allow_null=True)
    colorOfDessert = serializers.CharField(required=False, allow_null=True)
    colorOfBorderDessert = serializers.CharField(required=False, allow_null=True)
    imageExampleDessert = serializers.URLField(required=False, allow_null=True)
    dateCollectDessert = serializers.CharField(required=False, allow_null=True)
    hourCollectDessert = serializers.TimeField(required=False, allow_null=True)

class PaymentSerializer(serializers.Serializer):
    # dataPayer
    token = serializers.CharField(required=False, allow_null=True)
    issuer_id = serializers.CharField(required=False, allow_null=True)
    payment_method_id = serializers.CharField(required=False, allow_null=True)
    transaction_amount = serializers.FloatField(required=False, allow_null=True)
    installments = serializers.IntegerField(required=False, allow_null=True)
    inputName = serializers.CharField(required=False, allow_null=True)
    inputEmail = serializers.EmailField(required=False, allow_null=True)
    inputCelPhone = serializers.CharField(required=False, allow_null=True)
    inputMsg = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    cardholderName = serializers.CharField(required=False, allow_null=True)
    # dataDessert
    dessertData = DessertDataSerializer(required=False)
    cardholderEmail = serializers.EmailField(required=False, allow_null=True)
    cardholderName = serializers.CharField(required=False, allow_null=True)

    # def create(self, validated_data):
    #     dessert_data = validated_data.pop('dessertData', None)
    #     # Process dessert_data if present
    #     return validated_data
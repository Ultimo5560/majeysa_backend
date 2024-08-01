from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer
from django.core.mail import send_mail
import mercadopago
from django.conf import settings

sdk = mercadopago.SDK(settings.SECRET_KEY_MERCADO_PAGO)  # Reemplaza ACCESS_TOKEN con tu token de acceso

class ProcessPaymentView(APIView):
    def post(self, request):
        print('------------------------------------------------------------------------')
        print(request.data)
        print('------------------------------------------------------------------------')

        # Inicializa el serializer con los datos del request
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extrae y organiza los datos validados
            validated_data = serializer.validated_data
            # payer_info = validated_data["payer"]

            # print("payer_info:", payer_info)

            payment_data_mercado_pago = {
                "token": validated_data["token"],
                "issuer_id": validated_data["issuer_id"],
                "payment_method_id": validated_data["payment_method_id"],
                "transaction_amount": validated_data["transaction_amount"],
                "installments": validated_data["installments"],
                "payer": {
                    "email": validated_data["cardholderEmail"],
                    "first_name": validated_data["cardholderName"]
                },
            }

            payment_data = {
                # payment
                "inputName": validated_data.get("inputName", 'No especificado'),
                "inputEmail": validated_data.get("inputEmail", 'No especificado'),
                "inputCelPhone": validated_data.get("inputCelPhone", 'No especificado'),
                "inputMsg": validated_data.get("inputMsg", 'No especificado'),
                "description": validated_data.get("description", 'No especificado'),
                "cardholderEmail": validated_data.get("cardholderEmail", 'No especificado'),
                "cardholderName": validated_data.get("cardholderName", 'No especificado'),
                # dessert data
                "countPersons": validated_data.get("dessertData", {}).get("countPersons", 'No especificado'),
                "styleDessert": validated_data.get("dessertData", {}).get("styleDessert", 'No especificado'),
                "savorDessert": validated_data.get("dessertData", {}).get("savorDessert", 'No especificado'),
                "filling": validated_data.get("dessertData", {}).get("filling", 'No especificado'),
                "dessert": validated_data.get("dessertData", {}).get("dessert", 'No especificado'),
                "colorOfDessert": validated_data.get("dessertData", {}).get("colorOfDessert", 'No especificado'),
                "colorOfBorderDessert": validated_data.get("dessertData", {}).get("colorOfBorderDessert", 'No especificado'),
                "imageExampleDessert": validated_data.get("dessertData", {}).get("imageExampleDessert", 'No especificado'),
                "dateCollectDessert": validated_data.get("dessertData", {}).get("dateCollectDessert", 'No especificado'),
                "hourCollectDessert": validated_data.get("dessertData", {}).get("hourCollectDessert", 'No especificado'),
            }

            print('Datos de pago:', payment_data_mercado_pago['token'])
            print('cardholderEmail:', payment_data['cardholderEmail'])

            payment_response = sdk.payment().create(payment_data_mercado_pago)
            payment = payment_response["response"]
            print(payment_response)

            if payment_response["status"] in (200, 201):
                asunto = 'Confirmación de compra'

                mensaje_cliente = f"""
                <html>
                <body>
                    <p>Estimado(a) {payment_data['inputName']},</p>
                    <p>Gracias por su compra. Los detalles de su transacción son los siguientes:</p>
                    <ul>
                        <li>Producto: {payment_data['dessert']}</li>
                        <li>Monto: ${payment_data_mercado_pago['transaction_amount']}</li>
                        <li>Método de pago: {payment_data_mercado_pago['payment_method_id']}</li>
                        <li>Correo del pagador: {payment_data_mercado_pago['payer']['email']}</li>
                        <li>Correo del cliente: {payment_data['inputEmail']}</li>
                        <li>Tamaño o cantidad: para {payment_data['countPersons']} personas</li>
                        <li>Forma del postre: {payment_data['styleDessert']}</li>
                        <li>Sabor del postre: {payment_data['savorDessert']}</li>
                        <li>Relleno: {payment_data['filling']}</li>
                        <li>Fecha de recogida del postre: {payment_data['dateCollectDessert']}</li>
                        <li>Hora de recogida del postre: {payment_data['hourCollectDessert']}</li>
                    </ul>
                    <p>Gracias por su preferencia.</p>
                    <p>Atentamente,<br>Pasteleria Majeysa</p>
                </body>
                </html>
                """

                # Crear mensaje para el vendedor
                mensaje_vendedor = f"""
                    <html>
                    <body>
                        <p>Estimado Vendedor,</p>
                        <p>Se ha realizado un nuevo pedido de un postre. Los detalles de la transacción son los siguientes:</p>
                        <ul>
                            <li>Cliente: {payment_data['inputName']}</li>
                            <li>Correo del cliente: {payment_data['inputEmail']}</li>
                            <li>Celular del cliente: {payment_data['inputCelPhone']}</li>
                            <li>Mensaje del cliente: {payment_data['inputMsg']}</li>
                            <li>Producto: {payment_data['dessert']}</li>
                            <li>Monto: ${payment_data_mercado_pago['transaction_amount']}</li>
                            <li>Método de pago: {payment_data_mercado_pago['payment_method_id']}</li>
                            <li>Correo del pagador: {payment_data_mercado_pago['payer']['email']}</li>
                            <li>Fecha de recogida del postre: {payment_data['dateCollectDessert']}</li>
                            <li>Hora de recogida del postre: {payment_data['hourCollectDessert']}</li>
                            <li>Tamaño del postre: para {payment_data['countPersons']} personas</li>
                            <li>Forma del postre: {payment_data['styleDessert']}</li>
                            <li>Sabor del postre: {payment_data['savorDessert']}</li>
                            <li>Relleno: {payment_data['filling']}</li>
                            <li>Imagen de ejemplo: <a href="{payment_data.get('imageExampleDessert', '#')}" target="_blank">Ver imagen</a></li>
                            <li>Color del postre: <span style="display:inline-block; width:200px; height:40px; color:#feffc5; background-color:{payment_data['colorOfDessert']};">{payment_data['colorOfDessert']}</span></li>
                            <li>Color del borde: <span style="display:inline-block; width:200px; height:40px; color:#feffc5; background-color: {payment_data['colorOfBorderDessert']};">{payment_data['colorOfBorderDessert']} </span></li>
                        </ul>
                    </body>
                    </html>
                    """

                email_remitente = 'majeysapasteleria@gmail.com'
                email_destinatario_cliente = payment_data['inputEmail']
                email_destinatario_vendedor_1 = 'jemima_q@hotmail.com'  # Email del vendedor
                email_destinatario_vendedor_2 = 'eber926@hotmail.com'  # Email del vendedor

                send_mail(asunto, mensaje_vendedor, email_remitente, [email_destinatario_vendedor_1, email_destinatario_vendedor_2], html_message=mensaje_vendedor)
                send_mail(asunto, mensaje_cliente, email_remitente, [email_destinatario_cliente], html_message=mensaje_cliente)

                return Response(payment, status=status.HTTP_201_CREATED)
            else:
                print(payment_response)
                return Response(payment, status=status.HTTP_400_BAD_REQUEST)
        else:
            print('Errores de validación:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreatePreferenceView(APIView):
    def post(self, request):
        print('------------------------------------------------------------------------')
        print(request.data)
        print('------------------------------------------------------------------------')
        preference_data = {
            "items": [
                {
                    "title": request.data.get("title"),
                    "quantity": 1,
                    "unit_price": float(request.data.get("unit_price"))
                }
            ],
            "payer": {
                "email": request.data.get("email"),
            },
            "auto_return": "approved",
        }
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        return Response(preference, status=status.HTTP_201_CREATED)


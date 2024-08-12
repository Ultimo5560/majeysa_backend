from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer
from django.core.mail import send_mail
import mercadopago
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import mercadopago
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import Purchase

sdk = mercadopago.SDK('APP_USR-1053615135302620-081121-f7dd03566086d9a1e3bf39c2f394a75e-1939559437')  # Reemplaza ACCESS_TOKEN con tu token de acceso

# class ProcessPaymentView(APIView):
#     def post(self, request):
#         print('------------------------------------------------------------------------')
#         print(request.data)
#         print('------------------------------------------------------------------------')

#         # Inicializa el serializer con los datos del request
#         serializer = PaymentSerializer(data=request.data)
        
#         if serializer.is_valid():
#             # Extrae y organiza los datos validados
#             validated_data = serializer.validated_data
#             # payer_info = validated_data["payer"]

#             # print("payer_info:", payer_info)

#             payment_data_mercado_pago = {
#                 "token": validated_data["token"],
#                 "issuer_id": validated_data["issuer_id"],
#                 "payment_method_id": validated_data["payment_method_id"],
#                 "transaction_amount": validated_data["transaction_amount"],
#                 "installments": validated_data["installments"],
#                 "payer": {
#                     "email": validated_data["cardholderEmail"],
#                     "first_name": validated_data["cardholderName"]
#                 },
#             }

#             payment_data = {
#                 # payment
#                 "inputName": validated_data.get("inputName", 'No especificado'),
#                 "inputEmail": validated_data.get("inputEmail", 'No especificado'),
#                 "inputCelPhone": validated_data.get("inputCelPhone", 'No especificado'),
#                 "inputMsg": validated_data.get("inputMsg", 'No especificado'),
#                 "description": validated_data.get("description", 'No especificado'),
#                 "cardholderEmail": validated_data.get("cardholderEmail", 'No especificado'),
#                 "cardholderName": validated_data.get("cardholderName", 'No especificado'),
#                 # dessert data
#                 "countPersons": validated_data.get("dessertData", {}).get("countPersons", 'No especificado'),
#                 "styleDessert": validated_data.get("dessertData", {}).get("styleDessert", 'No especificado'),
#                 "savorDessert": validated_data.get("dessertData", {}).get("savorDessert", 'No especificado'),
#                 "filling": validated_data.get("dessertData", {}).get("filling", 'No especificado'),
#                 "dessert": validated_data.get("dessertData", {}).get("dessert", 'No especificado'),
#                 "colorOfDessert": validated_data.get("dessertData", {}).get("colorOfDessert", 'No especificado'),
#                 "colorOfBorderDessert": validated_data.get("dessertData", {}).get("colorOfBorderDessert", 'No especificado'),
#                 "imageExampleDessert": validated_data.get("dessertData", {}).get("imageExampleDessert", 'No especificado'),
#                 "dateCollectDessert": validated_data.get("dessertData", {}).get("dateCollectDessert", 'No especificado'),
#                 "hourCollectDessert": validated_data.get("dessertData", {}).get("hourCollectDessert", 'No especificado'),
#             }

#             print('Datos de pago:', payment_data_mercado_pago['token'])
#             print('cardholderEmail:', payment_data['cardholderEmail'])

#             payment_response = sdk.payment().create(payment_data_mercado_pago)
#             payment = payment_response["response"]
#             print(payment_response)

#             if payment_response["status"] in (200, 201):
#                 asunto = 'Confirmación de compra'

#                 mensaje_cliente = f"""
#                 <html>
#                 <body>
#                     <p>Estimado(a) {payment_data['inputName']},</p>
#                     <p>Gracias por su compra. Los detalles de su transacción son los siguientes:</p>
#                     <ul>
#                         <li>Producto: {payment_data['dessert']}</li>
#                         <li>Monto: ${payment_data_mercado_pago['transaction_amount']}</li>
#                         <li>Método de pago: {payment_data_mercado_pago['payment_method_id']}</li>
#                         <li>Correo del pagador: {payment_data_mercado_pago['payer']['email']}</li>
#                         <li>Correo del cliente: {payment_data['inputEmail']}</li>
#                         <li>Tamaño o cantidad: para {payment_data['countPersons']} personas</li>
#                         <li>Forma del postre: {payment_data['styleDessert']}</li>
#                         <li>Sabor del postre: {payment_data['savorDessert']}</li>
#                         <li>Relleno: {payment_data['filling']}</li>
#                         <li>Fecha de recogida del postre: {payment_data['dateCollectDessert']}</li>
#                         <li>Hora de recogida del postre: {payment_data['hourCollectDessert']}</li>
#                     </ul>
#                     <p>Gracias por su preferencia.</p>
#                     <p>Atentamente,<br>Pasteleria Majeysa</p>
#                 </body>
#                 </html>
#                 """

#                 # Crear mensaje para el vendedor
#                 mensaje_vendedor = f"""
#                     <html>
#                     <body>
#                         <p>Estimado Vendedor,</p>
#                         <p>Se ha realizado un nuevo pedido de un postre. Los detalles de la transacción son los siguientes:</p>
#                         <ul>
#                             <li>Cliente: {payment_data['inputName']}</li>
#                             <li>Correo del cliente: {payment_data['inputEmail']}</li>
#                             <li>Celular del cliente: {payment_data['inputCelPhone']}</li>
#                             <li>Mensaje del cliente: {payment_data['inputMsg']}</li>
#                             <li>Producto: {payment_data['dessert']}</li>
#                             <li>Monto: ${payment_data_mercado_pago['transaction_amount']}</li>
#                             <li>Método de pago: {payment_data_mercado_pago['payment_method_id']}</li>
#                             <li>Correo del pagador: {payment_data_mercado_pago['payer']['email']}</li>
#                             <li>Fecha de recogida del postre: {payment_data['dateCollectDessert']}</li>
#                             <li>Hora de recogida del postre: {payment_data['hourCollectDessert']}</li>
#                             <li>Tamaño del postre: para {payment_data['countPersons']} personas</li>
#                             <li>Forma del postre: {payment_data['styleDessert']}</li>
#                             <li>Sabor del postre: {payment_data['savorDessert']}</li>
#                             <li>Relleno: {payment_data['filling']}</li>
#                             <li>Imagen de ejemplo: <a href="{payment_data.get('imageExampleDessert', '#')}" target="_blank">Ver imagen</a></li>
#                             <li>Color del postre: <span style="display:inline-block; width:200px; height:40px; color:#feffc5; background-color:{payment_data['colorOfDessert']};">{payment_data['colorOfDessert']}</span></li>
#                             <li>Color del borde: <span style="display:inline-block; width:200px; height:40px; color:#feffc5; background-color: {payment_data['colorOfBorderDessert']};">{payment_data['colorOfBorderDessert']} </span></li>
#                         </ul>
#                     </body>
#                     </html>
#                     """

#                 email_remitente = 'majeysapasteleria@gmail.com'
#                 email_destinatario_cliente = payment_data['inputEmail']
#                 email_destinatario_vendedor_1 = 'jemima_q@hotmail.com'  # Email del vendedor
#                 email_destinatario_vendedor_2 = 'eber926@hotmail.com'  # Email del vendedor

#                 send_mail(asunto, mensaje_vendedor, email_remitente, [email_destinatario_vendedor_1, email_destinatario_vendedor_2], html_message=mensaje_vendedor)
#                 send_mail(asunto, mensaje_cliente, email_remitente, [email_destinatario_cliente], html_message=mensaje_cliente)

#                 return Response(payment, status=status.HTTP_201_CREATED)
#             else:
#                 print(payment_response)
#                 return Response(payment, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             print('Errores de validación:', serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreatePreferenceView(APIView):
    def post(self, request):
        print('------------------------------------------------------------------------')
        print(request.data)
        print('------------------------------------------------------------------------')

        # Inicializa el serializer con los datos del request
        serializer = PaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extrae y organiza los datos validados
            validated_data = serializer.validated_data

            # Datos de la preferencia
            preference_data = {
                "items": [
                    {
                        "title": validated_data.get("description", "No especificado"),
                        "quantity": 1,
                        "unit_price": float(validated_data.get("transaction_amount", 0))
                    }
                ],
                "payer": {
                    "email": validated_data.get("cardholderEmail", "no-reply@example.com"),
                },
                "auto_return": "approved",
                "back_urls": {
                    "success": "https://pasteleriamajeysa.netlify.app/making-order/success-transaction",  # Cambia esta URL por la tuya
                    "failure": "https://pasteleriamajeysa.netlify.app/making-order/error-transaction",  # Cambia esta URL por la tuya
                    "pending": "https://pasteleriamajeysa.netlify.app/making-order/pending-transaction"   # Cambia esta URL por la tuya
                },
                "notification_url": "https://majeysa-backend.onrender.com/api/mercado-pago-webhook/",  # Cambia esta URL por la tuya
            }

            # Crear preferencia en Mercado Pago
            try:
                preference_response = sdk.preference().create(preference_data)
                preference = preference_response["response"]
                
                # Guardar los detalles de la compra en la base de datos
                purchase = Purchase.objects.create(
                    preference_id=preference["id"],
                    input_name=validated_data.get("inputName", 'No especificado'),
                    input_email=validated_data.get("inputEmail", 'No especificado'),
                    input_cel_phone=validated_data.get("inputCelPhone", 'No especificado'),
                    input_msg=validated_data.get("inputMsg", 'No especificado'),
                    description=validated_data.get("description", 'No especificado'),
                    cardholder_email=validated_data.get("cardholderEmail", 'No especificado'),
                    cardholder_name=validated_data.get("cardholderName", 'No especificado'),
                    count_persons=validated_data.get("dessertData", {}).get("countPersons", None),
                    style_dessert=validated_data.get("dessertData", {}).get("styleDessert", None),
                    savor_dessert=validated_data.get("dessertData", {}).get("savorDessert", None),
                    filling=validated_data.get("dessertData", {}).get("filling", None),
                    dessert=validated_data.get("dessertData", {}).get("dessert", None),
                    color_of_dessert=validated_data.get("dessertData", {}).get("colorOfDessert", None),
                    color_of_border_dessert=validated_data.get("dessertData", {}).get("colorOfBorderDessert", None),
                    image_example_dessert=validated_data.get("dessertData", {}).get("imageExampleDessert", None),
                    date_collect_dessert=validated_data.get("dessertData", {}).get("dateCollectDessert", None),
                    hour_collect_dessert=validated_data.get("dessertData", {}).get("hourCollectDessert", None),
                    transaction_amount=validated_data.get("transaction_amount", 0),
                    payment_method_id=validated_data.get("payment_method_id", None)
                )

                print(preference)
                return Response(preference, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error creando preferencia:", e)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print('Errores de validación:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@csrf_exempt
def mercado_pago_webhook(request):

    if request.method == "POST":
        data = json.loads(request.body)
        print("Webhook recibido:", data)

        # Obtener el ID de la preferencia desde el webhook
        preference_id = data.get("data", {}).get("id")
        if not preference_id:
            return JsonResponse({"error": "ID de preferencia no encontrado"}, status=400)

        try:
            # Buscar la compra en la base de datos usando el ID de la preferencia
            purchase = Purchase.objects.get(preference_id=preference_id)

            # Configuración del correo
            asunto = 'Confirmación de compra'

            mensaje_cliente = f"""
            <html>
            <body>
                <p>Estimado(a) {purchase.input_name},</p>
                <p>Gracias por su compra. Los detalles de su transacción son los siguientes:</p>
                <ul>
                    <li>Producto: {purchase.dessert}</li>
                    <li>Monto: ${purchase.transaction_amount}</li>
                    <li>Método de pago: {purchase.payment_method_id}</li>
                    <li>Correo del pagador: {purchase.cardholder_email}</li>
                    <li>Correo del cliente: {purchase.input_email}</li>
                    <li>Tamaño o cantidad: para {purchase.count_persons} personas</li>
                    <li>Forma del postre: {purchase.style_dessert}</li>
                    <li>Sabor del postre: {purchase.savor_dessert}</li>
                    <li>Relleno: {purchase.filling}</li>
                    <li>Fecha de recogida del postre: {purchase.date_collect_dessert}</li>
                    <li>Hora de recogida del postre: {purchase.hour_collect_dessert}</li>
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
                        <li>Cliente: {purchase.input_name}</li>
                        <li>Correo del cliente: {purchase.input_email}</li>
                        <li>Celular del cliente: {purchase.input_cel_phone}</li>
                        <li>Mensaje del cliente: {purchase.input_msg}</li>
                        <li>Producto: {purchase.dessert}</li>
                        <li>Monto: ${purchase.transaction_amount}</li>
                        <li>Método de pago: {purchase.payment_method_id}</li>
                        <li>Correo del pagador: {purchase.cardholder_email}</li>
                        <li>Fecha de recogida del postre: {purchase.date_collect_dessert}</li>
                        <li>Hora de recogida del postre: {purchase.hour_collect_dessert}</li>
                        <li>Tamaño del postre: para {purchase.count_persons} personas</li>
                        <li>Forma del postre: {purchase.style_dessert}</li>
                        <li>Sabor del postre: {purchase.savor_dessert}</li>
                        <li>Relleno: {purchase.filling}</li>
                        <li>Imagen de ejemplo: <a href="{purchase.image_example_dessert}" target="_blank">Ver imagen</a></li>
                        <li>Color del postre: <span style="display:inline-block; width:200px; height:40px; color:#feffc5; background-color:{purchase.color_of_dessert};">{purchase.color_of_dessert}</span></li>
                        <li>Color del borde: <span style="display:inline-block; width:200px; height:40px; color:#feffc5; background-color: {purchase.color_of_border_dessert};">{purchase.color_of_border_dessert} </span></li>
                    </ul>
                </body>
                </html>
                """

            email_remitente = 'majeysapasteleria@gmail.com'
            email_destinatario_cliente = purchase.input_email
            email_destinatario_vendedor_1 = 'jemima_q@hotmail.com'  # Email del vendedor
            email_destinatario_vendedor_2 = 'eber926@hotmail.com'  # Email del vendedor

            send_mail(asunto, mensaje_vendedor, email_remitente, [email_destinatario_vendedor_1, email_destinatario_vendedor_2], html_message=mensaje_vendedor)
            send_mail(asunto, mensaje_cliente, email_remitente, [email_destinatario_cliente], html_message=mensaje_cliente)

            return JsonResponse({"status": "ok"})
        except Purchase.DoesNotExist:
            return JsonResponse({"error": "Compra no encontrada"}, status=404)
        except Exception as e:
            print("Error enviando correos:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer, SendMailFinishSerializar
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

sdk = mercadopago.SDK(settings.SECRET_KEY_MERCADO_PAGO)  # Reemplaza ACCESS_TOKEN con tu token de acceso


class SendMailFinishView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendMailFinishSerializar(data=request.data)

        if serializer.is_valid():
            # Extraer los datos del serializador
            validated_data = serializer.validated_data

            # Verificar si el campo 'bank' no es None o vacío
            bank_info = ""
            if validated_data.get('bank'):
                bank_info = f"""
                <li>Banco: {validated_data.get('bank')}</li>
                <li>Nombre de la tarjeta: {validated_data.get('cardName')}</li>
                <li>Folio: {validated_data.get('folio')}</li>
                <li>Referencia: {validated_data.get('referencia')}</li>
                """
                bank_name = validated_data.get('bankName')
            else:
                bank_info = f"""
                <li>ID: {validated_data.get('token')}</li>
                """
                bank_name = "Mercado Pago"

            # Crear el mensaje del cliente
            mensaje_cliente = f"""
            <html>
            <body>
                <p>Estimado(a) {validated_data.get('inputName')},</p>
                <p>Gracias por su compra. Los detalles de su transacción son los siguientes:</p>
                <ul>
                    <li>Producto: {validated_data.get('dessert')}</li>
                    <li>Monto: {validated_data.get('priceOfDessert')}</li>
                    <li>Nombre del banco: {bank_name}</li>
                    {bank_info}
                    <li>Correo del cliente: {validated_data.get('inputEmail')}</li>
                    <li>Tamaño o cantidad: para {validated_data.get('countPersons')} personas</li>
                    <li>Forma del postre: {validated_data.get('styleDessert')}</li>
                    <li>Sabor del postre: {validated_data.get('savorDessert')}</li>
                    <li>Relleno: {validated_data.get('filling')}</li>
                    <li>Fecha de recogida del postre: {validated_data.get('dateCollectDessert')}</li>
                    <li>Hora de recogida del postre: {validated_data.get('hourCollectDessert')}</li>
                </ul>
                <p>Gracias por su preferencia.</p>
                <p>Atentamente,<br>Pastelería Majeysa</p>
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
                    <li>Cliente: {validated_data.get('inputName')}</li>
                    <li>Correo del cliente: {validated_data.get('inputEmail')}</li>
                    <li>Celular del cliente: {validated_data.get('inputCelPhone')}</li>
                    <li>Mensaje del cliente: {validated_data.get('inputMsg')}</li>
                    <li>Producto: {validated_data.get('dessert')}</li>
                    <li>Monto: {validated_data.get('priceOfDessert')}</li>
                    <li>Nombre del banco: {bank_name}</li>
                    {bank_info}
                    <li>Fecha de recogida del postre: {validated_data.get('dateCollectDessert')}</li>
                    <li>Hora de recogida del postre: {validated_data.get('hourCollectDessert')}</li>
                    <li>Tamaño del postre: para {validated_data.get('countPersons')} personas</li>
                    <li>Forma del postre: {validated_data.get('styleDessert')}</li>
                    <li>Sabor del postre: {validated_data.get('savorDessert')}</li>
                    <li>Relleno: {validated_data.get('filling')}</li>
                    <li>Imagen de ejemplo: <a href="{validated_data.get('imageRef', '#')}" target="_blank">Ver imagen</a></li>
                    <li>Color del postre: <span style="display:inline-block; width:300px; height:40px; background-color:{validated_data.get('firstColor')};">{validated_data.get('firstColor')}</span></li>
                    <li>Color del borde: <span style="display:inline-block; width:300px; height:40px; background-color: {validated_data.get('secondColor')};">{validated_data.get('secondColor')}</span></li>
                </ul>
            </body>
            </html>
            """

            email_remitente = 'majeysapasteleria@gmail.com'
            email_destinatario_cliente = validated_data.get('inputEmail')
            email_destinatario_vendedor_1 = 'jemima_q@hotmail.com'  # Email del vendedor
            email_destinatario_vendedor_2 = 'eber926@hotmail.com'  # Email del vendedor

            try:
                # Enviar correos
                send_mail('Confirmación de Pedido - Pastelería Majeysa', mensaje_cliente, email_remitente, [email_destinatario_cliente], html_message=mensaje_cliente)
                send_mail('Nuevo Pedido - Pastelería Majeysa', mensaje_vendedor, email_remitente, [email_destinatario_vendedor_1, email_destinatario_vendedor_2], html_message=mensaje_vendedor)

                return Response({"status": "Correos enviados exitosamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreatePreferenceView(APIView):
    def post(self, request):
        print('------------------------------------------------------------------------')
        print(request.data)
        print('------------------------------------------------------------------------')

        # Inicializa el serializer con los datos del request
        serializer = PaymentSerializer(data=request.data)

        # Configuración de Mercado Pago
        # sdk = mercadopago.SDK(settings.SECRET_KEY_MERCADO_PAGO)
        
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
                    "email": validated_data.get("cardholderEmail",),
                },
                "auto_return": "approved",
                "back_urls": {
                    "success": "https://pasteleriamajeysa.netlify.app/success-transaction/",  # Cambia esta URL por la tuya
                    "failure": "https://pasteleriamajeysa.netlify.app/error-transaction/",  # Cambia esta URL por la tuya
                    "pending": "https://pasteleriamajeysa.netlify.app/pending-transaction/"   # Cambia esta URL por la tuya
                },
                "notification_url": "https://majeysa-backend.onrender.com/api/mercado-pago-webhook/",  # Cambia esta URL por la tuya
            }

            # Crear preferencia en Mercado Pago
            try:
                preference_response = sdk.preference().create(preference_data)
                preference = preference_response["response"]
                

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
        try:
            data = json.loads(request.body)
            print("Webhook recibido:", data)

            # Obtener el ID de la preferencia desde el webhook
            preference_id = data.get("data", {}).get("id")
            if not preference_id:
                return JsonResponse({"error": "ID de preferencia no encontrado"}, status=400)

            # Aquí realizamos una consulta a la API de Mercado Pago para obtener el estado de la transacción
            url = f"https://api.mercadopago.com/v1/payments/{preference_id}"
            headers = {
                "Authorization": f"Bearer {settings.SECRET_KEY_MERCADO_PAGO}"  # Correcta inclusión del token de acceso # Reemplaza esto con tu token de acceso
            }
            response = requests.get(url, headers=headers)
            print(response)
            if response.status_code != 200:
                return JsonResponse({"error": "Error al consultar el estado de la transacción"}, status=500)

            payment_data = response.json()
            transaction_status = payment_data.get("status")

            # Verificar si la transacción fue aprobada
            if transaction_status == "approved":
                # Configuración del correo para el vendedor
                asunto = 'Nuevo pedido recibido'
                mensaje_vendedor = f"""
                <html>
                <body>
                    <p>Estimado Vendedor,</p>
                    <p>Se ha recibido un nuevo pedido con el siguiente ID de preferencia:</p>
                    <p>ID de preferencia: {preference_id}</p>
                    <p>Estado de la transacción: {transaction_status}</p>
                    <p>Por favor, revisa los detalles del pedido en un correo posterior.</p>
                    <p>Atentamente,<br>Pastelería Majeysa</p>
                </body>
                </html>
                """

                email_remitente = 'majeysapasteleria@gmail.com'
                email_destinatario_vendedor_1 = 'jemima_q@hotmail.com'
                email_destinatario_vendedor_2 = 'eber926@hotmail.com'

                send_mail(
                    asunto, 
                    mensaje_vendedor, 
                    email_remitente, 
                    [email_destinatario_vendedor_1, email_destinatario_vendedor_2],
                    html_message=mensaje_vendedor
                )

                return JsonResponse({"status": "Correo enviado y preferencia encontrada", "preference_id": preference_id}, status=200)
            else:
                return JsonResponse({"status": "Transacción no aprobada", "transaction_status": transaction_status}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Error en el formato del JSON recibido"}, status=400)
        except Exception as e:
            print("Error en el procesamiento:", e)
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)




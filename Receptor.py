import pika
import smtplib

# Configuración de conexión con RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declarar una cola
channel.queue_declare(queue='correo')

def callback(ch, method, properties, body):
    # Enviar el mensaje por correo electrónico
    mensaje = body.decode('utf-8')
    destinatario = 'juan.garcia@udla.edu.ec'
    remitente = 'camila.pillajo@udla.edu.ec'
    asunto = 'Mensaje recibido desde la cola'

    # Configuración de SMTP
    servidor_smtp = 'servidor.udla'
    puerto_smtp = 587

    # Crear mensaje
    cuerpo_mensaje = f'Asunto: {asunto}\n\n{mensaje}'

    # Enviar correo electrónico
    with smtplib.SMTP(servidor_smtp, puerto_smtp) as servidor:
        servidor.starttls()
        servidor.login('usuario@dominio.com', 'contraseña')
        servidor.sendmail(remitente, destinatario, cuerpo_mensaje)

    print(f"Mensaje enviado por correo electrónico: {mensaje}")

# Consumir mensajes de la cola
channel.basic_consume(queue='correo', on_message_callback=callback, auto_ack=True)

print('Esperando mensajes. Presiona CTRL+C para salir.')
channel.start_consuming()
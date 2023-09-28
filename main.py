from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import decouple

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = decouple.config('SMTP_USERNAME')
SMTP_PASSWORD = decouple.config('SMTP_PASSWORD')


app = Flask(__name__)
app.config['SECRET_KEY'] = decouple.config('SECRET_KEY')
CORS(app)

@app.route('/enviar-comentario', methods=['POST'])
def recibir_comentario():
    data = request.json

    try:
        email_data = data.get('email')
        phone_data = data.get('phone')
        message_data = data.get('message')

        email_message = f'Subject: Comentario Tango.Store\n\n' \
                        f'Email: {email_data}\n' \
                        f'Telefono: {phone_data}\n' \
                        f'Mensaje: {message_data}\n'.encode('utf-8')


        # Establecer los detalles del servidor SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(user=SMTP_USERNAME, password=SMTP_PASSWORD)
            server.sendmail(
                from_addr=SMTP_USERNAME,
                to_addrs='web.mercadeo@grupo-pb.com',
                msg=email_message,
            )
            server.close()

            print('Email Enviado...')

        return jsonify({"response": {"success": "Successfully sent email"}}), 200


    except Exception as error:
        print(f'Error: {error}')
        return jsonify({"response": {"error": "{}".format(error)}})




if __name__ == "__main__":
  app.run(debug=True)

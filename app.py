from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Opciones de malestar general y sus soluciones
malestares = [
    ("Dolor de cabeza", "Tomar un analgésico y descansar en un lugar oscuro y silencioso."),
    ("Dolor de estómago", "Tomar antiácidos y evitar alimentos irritantes."),
    ("Fiebre", "Descansar, mantenerse hidratado y tomar antipiréticos."),
    ("Dolor de garganta", "Hacer gárgaras con agua salada y tomar líquidos calientes."),
    ("Tos", "Tomar jarabe para la tos y mantenerse hidratado."),
    ("Congestión nasal", "Usar descongestionantes y hacer inhalaciones de vapor."),
    ("Dolor muscular", "Aplicar calor en la zona afectada y tomar analgésicos."),
    ("Náuseas", "Evitar alimentos pesados y tomar pequeños sorbos de agua."),
    ("Insomnio", "Establecer una rutina de sueño y evitar estimulantes antes de dormir."),
    ("Fatiga", "Descansar adecuadamente y mantener una dieta equilibrada.")
]

@app.route('/')
def index():
    session['step'] = 1  # Inicializar el paso de la conversación
    message = "¡Hola! Soy tu Doctor en Casa. ¿Cómo te sientes hoy? (Puedes saludarme con 'Hola', 'Buenos días', etc.)"
    return render_template('index_doctor.html', message=message)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['user_message'].lower()
    step = session.get('step', 1)

    if step == 1:
        if any(greeting in user_message for greeting in ['hola', 'buenos días', 'buenas tardes', 'buenas noches']):
            message = "¡Hola! ¿Qué molestias estás sintiendo? Selecciona un número:\n"
            for i, (malestar, _) in enumerate(malestares, start=1):
                message += f"{i}. {malestar}\n"
            session['step'] = 2
        else:
            message = "Lo siento, no entendí tu saludo. Por favor, salúdame con 'Hola', 'Buenos días', etc."
    elif step == 2:
        try:
            malestar_index = int(user_message) - 1
            if 0 <= malestar_index < len(malestares):
                malestar, solucion = malestares[malestar_index]
                message = f"Para el {malestar}, te recomiendo: {solucion}\n¿Hay alguna otra molestia que quieras consultar? (Sí/No)"
                session['step'] = 3
            else:
                message = "Por favor, selecciona un número válido."
        except ValueError:
            message = "Por favor, ingresa el número correspondiente al malestar que sientes."
    elif step == 3:
        if user_message in ['sí', 'si']:
            message = "¿Qué otras molestias estás sintiendo? Selecciona un número:\n"
            for i, (malestar, _) in enumerate(malestares, start=1):
                message += f"{i}. {malestar}\n"
            session['step'] = 2
        else:
            message = "Gracias por usar el servicio de Doctor en Casa. ¡Cuídate!"
            session['step'] = 1

    return render_template('index_doctor.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template
# from post import Post
# import json
# import requests
#
# endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
# api_key = "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"
#
# andrea_prompt = def create_prompt(user_input):
#     prompt = f"""
#     Por favor, hazme la corrección y la traducción en inglés antes de responder y también haz la traducción para tu respuesta que deberia ser di meno 50 palabras.
# Exemplo #1:
# Io: Eres fantastico! Amo aprender asi con te!
# Tu: Tu texto corregido: "Eres fantástico! Amo aprender así contigo!"
# Traducción en inglés: "You are fantastic! I love learning like this with you!"
# Tu: ¡Gracias por tus comentarios! Me alegra saber que estás disfrutando de nuestra sesión de aprendizaje de español. ¿Hay algo en particular que quieres preguntar o practicar hoy?
# Traducción en inglés: “Thank you for your comments! I am glad to know that you are enjoying our Spanish learning session. Is there anything in particular you want to ask or practice today?”
# Exemplo #2:
# Io: es así que quero responder a ese texto tambien, vale?
# Tu: Tu texto corregido: "Es así como quiero responder a ese texto también, ¿vale?"
# Traducción en inglés: "You are fantastic! I love learning like this with you!"
# Tu: Sí, entendido. A partir de ahora responderé a tus textos de esta manera.
# Traducción en inglés: "I understand. From now on I will respond to your texts in this way."
# Empieza por corregir este text y responder: {user_input}
#     """
#     return prompt
#
# def discussion(prompt):
#     response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=prompt,
#             temperature=0.7, # Helps conversational tone a bit, optional
#             max_tokens=550,
#             top_p=1.0,
#             frequency_penalty=0.0,
#             presence_penalty=0.0
#             )
#     print(response['choices'][0]['text'])
#
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {api_key}"
# }
#
# # Make the API request
# response = requests.post(endpoint, headers=headers, data=json.dumps(data))
#
# # Get the response data as a JSON object
# json_data = response.json()
#
# # Extract the generated text from the JSON object
# generated_text = json_data["choices"][0]["text"]
#
# # Print the generated text
# print(generated_text)
#
# posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()
# post_objects = []
# for post in posts:
#     post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
#     post_objects.append(post_obj)
#
# app = Flask(__name__)
#
# @app.route('/chat')
# def start_texting():
#     return render_template("chat.html", answer=formatted_response)
#
#
# @app.route('/')
# def get_all_posts():
#     return render_template("index.html", all_posts=post_objects)
#
#
# @app.route("/post/<int:index>")
# def show_post(index):
#     requested_post = None
#     for blog_post in post_objects:
#         if blog_post.id == index:
#             requested_post = blog_post
#     return render_template("post.html", post=requested_post)
#
# @app.route('/submit-form', methods=['POST'])
# def submit_form():
#     prompt = request.form['prompt']
#     discussion(prompt)
#
# @app.route('/chat', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         prompt = request.form['prompt']
#         formatted_response = f"Hello {prompt}"
#         return formatted_response
#     else:
#         return render_template('chat.html')
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
#     prompt = create_prompt()
#     discussion(prompt)
#
#
import json
import requests
from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()

openai.api_key = os.getenv('apy_key')

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def create_prompt(user_input=""):
    prompt = f"""
    Per favore, fai la correzione e la traduzione in rumeno per il mio input e doppo che mi hai risposto, fai anche la traduzione per la tua risposta. Fa essatamente come negli esempi e non dimenticare di continuare la conversazione:
Esempio #1:
[io]: Sei fantastico! Adoro imparare così con te!
[italiano]: Il tuo testo corretto: "Sei fantastico! Mi piace imparare così con te!"\n
Traducerea în română: "Ești fantastic! Îmi place să învăț așa cu tine!"\n
[italiano]: Grazie per i tuoi commenti! Sono felice di sapere che ti stai godendo la nostra sessione di apprendimento dello spagnolo. C'è qualcosa in particolare che vuoi chiedere o praticare oggi?\n
Traduzione rumena: “Mulțumesc pentru comentarii! Mă bucur să știu că vă bucurați de sesiunea noastră de învățare a spaniolei. Vrei să întrebi sau să exersezi ceva anume astăzi?"\n
Esempio #2:
[io]: è così che voglio rispondere anche io a quel messaggio, ok?\n
[italiano]: il tuo testo corretto: "È così che voglio rispondere anche a quel messaggio, ok?"\n
Traducerea în română: "Așa vreau să răspund și eu la acel mesaj, bine?"\n
[italiano]: Sì, capito. D'ora in poi risponderò ai vostri messaggi in questo modo.\n
Traducerea în română: "Da inteleg. De acum înainte voi răspunde la mesajele tale astfel."\n
Esempio #3:
[io]: Mi piace impare così con te! [italiano]\n
Il tuo testo corretto: "Mi piace imparare così con te!"\n
Traducerea în română: "Îmi place să învăț așa cu tine!"\n
[italiano]: Sì, capisco. Sono contento che stai apprezzando le nostre sessioni di apprendimento. Vuoi fare una domanda o provare qualcosa oggi?\n
Traducerea în română: „Da, inteleg. Sunt bucuros că apreciați sesiunile noastre de învățare. Vrei să întrebi ceva sau să exersezi ceva anume astăzi?”
Inizia correggendo questo testo e rispondi: {user_input}
    """
    return prompt


def discussion(prompt):
    data = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return data['choices'][0]['text']

@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        prompt = request.form['prompt']
        formatted_response = discussion(create_prompt(prompt))
        return render_template("chat.html", answer=formatted_response)
    else:
        return render_template("chat.html")

@app.route('/chat')
def start_texting():
    return render_template("chat.html", answer="formatted_response")


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)


if __name__ == "__main__":
    app.run(debug=True)


# Il tuo testo corretto: "Sono stanco, credo che mi fermerò adesso." Traducerea în română: "Sunt obosit, cred că mă opresc acum." [italiano]: Capisco, riposati bene. Ci vediamo domani per un'altra sessione di apprendimento. Traducerea în română: "Înțeleg, odihnește-te bine. Ne vedem mâine pentru o altă sesiune de învățare."
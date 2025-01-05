import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return jsonify({"message": "This endpoint requires POST requests for chat."})

    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Call OpenAI's API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        assistant_reply = response['choices'][0]['message']['content']
        return jsonify({"reply": assistant_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# The block below is for local development only. In production, Gunicorn will run the app.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
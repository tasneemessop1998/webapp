from flask import Flask, request, render_template_string
import requests
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html>
<head>
<title>Azure ML Chat Interface</title>
<style>
    body, html {
        height: 100%;
        margin: 0;
        overflow: hidden;
        font-family: Arial, sans-serif;
    }
 .gradient-background {
        animation: gradient-animation 30s ease infinite;
        background: linear-gradient(270deg, #00008b, #800080, #00ced1, #00008b, #800080);
        background-size: 400% 400%;
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: -1;
    }
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .content {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: white;
    }
    input[type=text] {
        padding: 10px;
        margin-bottom: 20px;
        width: 300px;
    }
    input[type=submit] {
        padding: 10px;
        background-color: #4b0082; /* Dark purple color */
        border: none;
        color: white;
        cursor: pointer;
        border-radius: 5px; /* Optional: for rounded corners */
    }
    input[type=submit]:hover {
        background-color: #3a0065; /* A slightly darker purple for hover effect */
    }
    .response-block {
        background-color: white;
        color: black;
        max-height: 300px; /* Maximum height before scroll */
        overflow-y: auto; /* Enable vertical scrolling */
        padding: 20px;
        margin-top: 20px;
        border-radius: 5px; /* Optional: for rounded corners */
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2); /* Optional: for box shadow */
    }
    form {
        margin-bottom: 20px;
    }
</style>
</head>
<body>
<div class="gradient-background"></div>
<div class="content">
    <h1>Ask a Question</h1>
    <form action="/" method="post">
        <input type="text" name="chat_input" placeholder="Type your question here..." required>
        <input type="submit" value="Send">
    </form>
{% if response %}
    <h2>Response:</h2>
    <div class="response-block">
        <p>{{ response }}</p>
    </div>
{% endif %}
</div>
</body>
</html>
'''


def query_endpoint(question):
    url = 'https://tastestproject-pumco.westus.inference.ml.azure.com/score'
    api_key = '002ZbVlmierzg9csacZj0higRJVterR7'
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + api_key,
               'azureml-model-deployment': 'tastestproject-pumco-1'}
    data = {"chat_input": question}
    body = str.encode(json.dumps(data))

    response = requests.post(url, headers=headers, data=body)
    return response.text

@app.route("/", methods=["GET", "POST"])
def chat():
    response_message = ""  # This will hold the actual message to display
    if request.method == "POST":
        user_input = request.form["chat_input"]
        response_json = query_endpoint(user_input)
        # Assuming the response is a JSON string, parse it:
        response_data = json.loads(response_json)
        # Extract the 'chat_output' key value
        response_message = response_data.get("chat_output", "")
    return render_template_string(HTML_TEMPLATE, response=response_message)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, render_template, session
import random
import string
import requests

app = Flask(__name__)
app.secret_key = 'whatever'  # Replace with your secret key

def generate_string(length=10):
    """Generate a random string of fixed length."""
    url_chars = string.ascii_letters + string.digits + "$-_.+!*'()"
    return ''.join(random.choice(url_chars) for _ in range(length))

def generate_palindrome(length=10):
    """Generate a random palindromic string of fixed length."""
    half_length = length // 2
    first_half = generate_string(half_length)
    second_half = first_half[::-1] if length % 2 == 0 else first_half[-1::-1]
    return first_half + second_half

def randomize_order():
    """Randomly return either generate_string() or generate_palindrome() first."""
    funcs = [generate_string(), generate_palindrome()]
    random.shuffle(funcs)
    return funcs

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method != 'POST':
        questions = ['Question 01', 'Question 02', 'Question 03', 'Question 04', 'Question 05', 'Question 06', 'Question 07', 'Question 08', 'Question 09', 'Question 10']
        # Generate a new string and a new palindrome for each question
        session['questions_with_strings'] = {q: randomize_order() for q in questions}
        print("Session: ")
        print(session['questions_with_strings'])

    if request.method == 'POST':
        # Get form data
        form_data = request.form.to_dict()

        # Prepare data for the webhook
        data_for_webhook = {}
        for question, options in session['questions_with_strings'].items():
            selected_option = form_data.get(question)
            non_selected_option = next(option for option in options if option != selected_option)
            data_for_webhook[question] = {'S': selected_option, 'N': non_selected_option}
        print("Data: ")
        print(data_for_webhook)
        # Send data to your Make webhook
        make_webhook_url = 'https://hook.us1.make.com/5thxgtk7vmj47hug1rfvegfuhebdpi64'
        response = requests.post(make_webhook_url, json=data_for_webhook)
        # Generate a new string and a new palindrome for each question
        questions = ['Question 01', 'Question 02', 'Question 03', 'Question 04', 'Question 05', 'Question 06', 'Question 07', 'Question 08', 'Question 09', 'Question 10']
        session['questions_with_strings'] = {q: randomize_order() for q in questions}

    return render_template('survey.html', questions=session.get('questions_with_strings', {}))


if __name__ == '__main__':
    app.run(debug=True)


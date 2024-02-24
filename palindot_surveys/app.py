from flask import Flask, request, render_template
import random
import string
import requests

app = Flask(__name__)

def generate_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_palindrome(length=10):
    """Generate a random palindromic string of fixed length."""
    half_length = length // 2
    first_half = generate_string(half_length)
    second_half = first_half[::-1] if length % 2 == 0 else first_half[-1::-1]
    return first_half + second_half

@app.route('/', methods=['GET', 'POST'])
def survey():
    if request.method == 'POST':
        # Get form data
        form_data = request.form.to_dict()

        # Prepare data for the webhook
        data_for_webhook = {}
        for question, answer in form_data.items():
            all_options = [generate_string(), generate_palindrome()]
            not_chosen_options = [option for option in all_options if option != answer]
            data_for_webhook[question] = [answer] + not_chosen_options

        # Send data to your Make webhook
        make_webhook_url = 'https://hook.us1.make.com/5thxgtk7vmj47hug1rfvegfuhebdpi64'
        response = requests.post(make_webhook_url, json=data_for_webhook)

    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6', 'Question 7', 'Question 8', 'Question 9', 'Question 10']
    # Generate a new string and a new palindrome for each question
    questions_with_strings = {q: (generate_string(), generate_palindrome()) for q in questions}
    return render_template('survey.html', questions=questions_with_strings)

if __name__ == '__main__':
    app.run(debug=True)

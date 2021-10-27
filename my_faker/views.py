from my_faker import app

@app.route('/')
def home():
    return 'Hello!'
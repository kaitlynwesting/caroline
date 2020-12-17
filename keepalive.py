from flask import Flask
app = Flask('')
@app.route('/')
def main():
  return "stay alive pls"
app.run(host="0.0.0.0", port=8000)

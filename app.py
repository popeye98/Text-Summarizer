from flask import Flask, render_template, url_for, request, redirect
from main import *

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def upload_file():

    if request.method == 'POST':



        text=request.form['message']
        input_user=int(request.form['input_user'])

        if len(text)==0:
            return render_template('index.html',results="Please enter Proper plot")
      
        summary=process(text,input_user)

        result_dic={
			'summary':summary
           
   }
        return render_template('index.html', results = result_dic)

if __name__=='__main__':
    app.run(debug=True)
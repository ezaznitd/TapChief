from flask import Flask, render_template, url_for, redirect, request
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

wordSearched = ""
content = ""
dict = {}
list = []


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/")
def document_form():
    return render_template('register.html', title='Register')

@app.route('/', methods=['POST'])
def save_comment():
    # This is to make sure the HTTP method is POST and not any other
    if request.method == 'POST':
        global content
        content = request.form['Document']
        # comment = request.form['comment']
        print(content)
        # the file is going to be written.
        with open('mydoc.txt','w') as inFile:
            inFile.write(str(content))
        return redirect(url_for('index_clear_search'))
        # return render_template("index_search.html")
        # return "successful entry"

@app.route('/index-clear-search')
def index_clear_search():
    return render_template("myinp.html", title="index search")

@app.route('/clear_Function')
def clear_Function():
    global list
    global dict
    list = []
    dict = {}
    print('You have cleared all the index')
    return ""

@app.route('/index_Function')
def index_Function():
    global dict
    global list
    index = 0
    cnt = 0
    s = ""
    for i in range(len(content)):
        if(content[i] == '\n'):
            cnt += 1
        else:
            if(cnt == 4):
                list.append(random.randrange(100000, 500000))
                dict[list[index]] = s
                index += 1
                s = ""
            s += content[i]
            cnt = 0
    list.append(random.randrange(100000, 500000))
    dict[list[index]] = s
    print(content)
    return ""


@app.route('/index-clear-search', methods=['POST'])
def contact():
    if request.method == 'POST':
        if request.form['button'] == 'clear':
            print('clear function called')
            return 'clear function called'
        if request.form['button'] == 'index':
            print('index function called')
            return 'index function called'
        if request.form['button'] == 'search':
            print('search function called')
            return 'search function called'

@app.route('/addRegion', methods=['POST'])
def addRegion():
    global wordSearched
    wordSearched = request.form['projectFilePath']
    s = "you searched for " + wordSearched
    return redirect(url_for('generate_results'))

@app.route('/search-results')
def generate_results():
    d = {}
    w = wordSearched.lower()
    result = []
    is_present = False
    if(len(list) == 0):
        result.append("You haven't index the Paragraphs")
    for i in range(len(list)):
        s = dict[list[i]]
        s = s.lower()
        s_list = s.split(' ')
        cnt = 0
        for j in range(len(s_list)):
            if(s_list[j] == w):
                is_present = True
                break
        if(is_present):
            ch = "Paragraph Id "
            ch = ch + str(list[i]) + '\n'
            result .append(ch)
            result.append(dict[list[i]])
        # print(s_list)
        # result.append(str(list[i]))
    return render_template("search_results.html", result=result)
            
if __name__ == '__main__':
    app.run(threaded=True, port=5000)

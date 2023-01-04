import os

import nltk
from flask import Flask, render_template, request
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import ngrams
from nltk.collocations import *

app = Flask(__name__)
app.config.from_pyfile('config.py')
nltk.download('punkt')
nltk.download('genesis')


@app.route('/', methods=['GET', 'POST'])
def getHome():
    return render_template('index.html')

@app.route('/searchfiledisplaycount', methods=['GET'])
def searchfiledisplaycount():
    search = request.args.get('search')
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    for x in dir_list:
        if x.endswith('.txt') and x ==search+".txt":
            number_of_words = 0
            with open(app.config['UPLOAD_FOLDER'] + x, 'r', encoding='utf-8') as file:
                data = file.read()
                lines = data.split()
                number_of_words += len(lines)

    return render_template('display.html',number_of_words=number_of_words)

@app.route('/removepunctstopwithfilewrite', methods=['GET'])
def removepunctstopwithfilewrite():
    punct = request.args.get('punct')
    punct = '''!()-[]{};:'’”'“""\,<>./?@#$%^&*_~'''
    stopword = request.args.get('stopword')
    stopwords=stopword.split(",")
    file_read = {}
    text = request.args.get('text')
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    filenames=findfilenames(dir_list)
    for filename in filenames:
        without_punct = ""
        without_punctstop_final = ""
        with open(app.config['UPLOAD_FOLDER'] + filename, 'r', encoding='utf-8') as file:
            data = file.read()
            for char in data:
                if char not in punct:
                    without_punct = without_punct +char
        new_file = open(app.config['UPLOAD_FOLDER'] + filename, "w", encoding='utf-8')
        new_file.write(without_punct)
        new_file.close()

        with open(app.config['UPLOAD_FOLDER'] + filename, 'r', encoding='utf-8') as file:
            text = file.readlines()
            for i in range(len(text)):
                textarr=text[i].replace('\n','').split(" ")
                for j in range(len(textarr)):
                 if not textarr[j].lower() in stopwords:
                   without_punctstop_final = without_punctstop_final +" "+ textarr[j]
                without_punctstop_final=without_punctstop_final+"\n"
        file.close()
        new_file = open(app.config['UPLOAD_FOLDER']+filename, "w",encoding='utf-8')
        new_file.write(without_punctstop_final)
        new_file.close()
        file_read[filename]=' '.join(read_file(app.config['UPLOAD_FOLDER']+filename))
    return render_template('display.html',without_punctstop_final=file_read)


@app.route('/findparawithword', methods=['GET'])
def findparawithword():
    file_read = {}
    text = request.args.get('text')
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    filenames=findfilenames(dir_list)
    for filename in filenames:
        with open(app.config['UPLOAD_FOLDER'] + filename, 'r', encoding='utf-8') as file:
            data = file.read()
            paras=data.split("\n\n")
            paranum=0
            index=0
            for para in paras:
                paranum=paranum+1
                if text in para:
                     parafound=para
                     index=para.index(text)
                     file_read[filename]=[filename,paranum,parafound,index]
    return render_template('display.html',para_withword_index=file_read)

def read_file(filename):
    N = 3
    list=[]
    with open(filename, 'r', encoding='utf-8') as file:
        for i in range(N):
            list.append(next(file).strip())
    return list

@app.route('/upperlower', methods=['GET'])
def upperlower():
    textfile = request.args.get('textfile')+".txt"
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    words_to_lower=[]
    with open(app.config['UPLOAD_FOLDER'] + textfile, 'r', encoding='utf-8') as file:
        text = file.readlines()
        for i in range(len(text)):
            words_to_lower.append(text[i].lower())
    return render_template('display.html',words_to_lower=words_to_lower)


def findfilenames(dir_list):
    filenames=[]
    for x in dir_list:
        if x:
            filenames.append(x)
    return filenames


def firstNlines(filename):
    N = 10
    filename="1.txt"
    with open(app.config['UPLOAD_FOLDER']+filename,  'r', encoding='utf-8') as file:
        for i in range(N):
            line = next(file).strip()
            print(line)



@app.route('/findwordcountlines', methods=['GET'])
def findwordcountlines():
    search = request.args.get('search')
    filename = request.args.get('filename')
    lineswithword=[]
    number_of_words=0
    linecount=0
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    for x in dir_list:
        if x.endswith('.txt') and x ==filename+".txt":
            number_of_lines = 0
            with open(app.config['UPLOAD_FOLDER'] + x, 'r', encoding='utf-8') as file:
                text = file.readlines()
                for i in range(len(text)):
                    textarr = text[i].replace('\n', '').split(" ")
                    for j in range(len(textarr)):
                        if  textarr[j].lower() == search:
                            number_of_words += 1;
                    if search in text[i]:
                        if(linecount <=2):
                            lineswithword.append(text[i])
                        linecount=linecount+1

    return render_template('display.html',number_of_words=number_of_words,lineswithword=lineswithword)




@app.route('/wordstemmerwithoutfilewrite', methods=['GET'])
def wordstemmerwithoutfilewrite():
    ps = PorterStemmer()
    stemword = request.args.get('stemword')
    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    filenames = findfilenames(dir_list)
    stemwordslist = []
    for filename in filenames:
        stemmed_final = ""
        textfilename = app.config['UPLOAD_FOLDER'] + filename
        with open(textfilename, 'r', encoding='utf-8') as file:
            text = file.readlines()
            for i in range(len(text)):
                stemmed_final=""
                textarr = text[i].replace('\n', '').split(" ")
                for j in range(len(textarr)):
                    if textarr[j].lower() == stemword.lower():
                        stemmed_final = stemmed_final + " " + ps.stem(textarr[j])
                    else:
                        stemmed_final = stemmed_final + " " + textarr[j]
                stemwordslist.append(stemmed_final)

    return render_template('display.html', stemwordslist=stemwordslist)



@app.route('/findtwowordNlines', methods=['GET'])
def findtwowordNlines():
    number = int(request.args.get('number'))
    wordsinput = request.args.get('wordsinput')
    file_read = {}

    dir_list = os.listdir(app.config['UPLOAD_FOLDER'])
    filenames=findfilenames(dir_list)
    for filename in filenames:
        lineswithword = []
        linecount = 0
        with open(app.config['UPLOAD_FOLDER'] + filename, 'r', encoding='utf-8') as file:
            text = file.readlines()
            for i in range(len(text)):
                if wordsinput.lower() in text[i].lower():
                    if(linecount < number):
                        lineswithword.append(text[i])
                    linecount=linecount+1
        file_read[filename]=' '.join(lineswithword)
    return render_template('display.html',adjwordNlines=file_read)



if __name__ == "__main__":
    app.run(host="0.0.0.0")

#** Priscilla Nunez
#** SI 364 F18
#** 9/15/18

#################################


## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
#*** HW1 numbers 1 to 4 are my own solutions - NunezP


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"
#*** Install Flask itself is a library.

import requests
import json
import datetime
from flask import Flask, request

#*** Initializing flask application
app = Flask(__name__)
app.debug = True



@app.route('/class')
def courseView():
    return "Welcome to SI 364!" #endpoint /class is welcome

## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }

@app.route('/movie/<name>')                         # I used 1 word movie name titanic for <name>
def movie_name(name):
    url = "https://itunes.apple.com/search"
    params = {"media": "movie", "term": name}       # This is for my search
    get_name = requests.get(url, params = params)   # Code requesting the url of itunes and responds
    json_format = json.loads(get_name.text)         # I get the dictionary
    return str(json_format)                         # String


## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

#*** Removed value = "0" - doesn't need to be there, just a placeholder.
@app.route('/question', methods= ['POST', 'GET'])
def fav_num():
    i= '''<!DOCTYPE html>
<html>
<body>
<form action="/result" method="GET">
<div>
    Enter favorite number:
    <input type= "text" name= "number"> 
    <br> <br>
    <input type= "submit" value= "Submit"
</div>
</form>
</body>
</html>'''

    return i

@app.route('/result', methods= ['POST', 'GET'])   # endpoint is result
def doubled_num():
    if request.method == 'GET':
        double = request.args                     # Request the args for number
        favorite = double.get('number')           # args is assigned to double for number
        multiply = 2 * (int(favorite))            # Fave number is 13 and output will be doubled to 26    
        return "Double your favorite number is {}".format(multiply)     #prints string and shows number 26

## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

#***
#*** Points will be assigned for each specification in the problem. Action is problem4results. Radio button for source link options.
#***

@app.route('/problem4form', methods= ['POST', 'GET'])
def time_selection():
    i= '''<!DOCTYPE html>
<html>
<body>
<form action="/problem4result" method="GET">
<div>
    Enter a news topic to search: <br>
    <input type="text" name="topic"><br>
    Would you like to include link to the source of the news?(y/n): <br>
    <input type= "radio" name= "options" value=true > True <br>
    <input type= "radio" name= "options" value=false > False <br>
    <br>
    <input type= "submit" value= "Next"
</div>
</form>
</body>
</html>'''

    return i

@app.route('/problem4result', methods= ['POST', 'GET'])  # Used endpoint problem4form
def get_todays_news():
    if request.method == 'GET':
        result = request.args
        include_source = result.get('options')
        topic = result.get('topic')
        
        base_url = 'https://newsapi.org/v2/everything?' # Strawberries and white wine helped me with problem 4. Pulled from NewsApi.org.
        api_key = 'd924e2624fb342c095e9c489f2d697a0'    # Registered api key
        full_url = base_url + "q=" + topic + "&from=" + datetime.datetime.today().strftime('%Y-%m-%d') + "&sortBy=publishedAt&apiKey=" + api_key

        response = requests.get(full_url)                # Requests
        articles = json.loads(response.text)["articles"] 
       
        output = ""                                      # Output
        for article in articles:

            if(not include_source):
                output += ("<br> <br>" +" Author: {}".format(article["author"]) + "<br>" + "Title: {}".format(article["title"]) + "<br> <img height='300px' width='300px' src={} />".format(article["urlToImage"] or "https://www.freeiconspng.com/uploads/no-image-icon-15.png") +"<br>" + "Description: {}".format(article["description"]) + "<br>")
            else:
                output += ("<br> <br>" +" Author: {}".format(article["author"]) + "<br>" + "Title: {}".format(article["title"]) + "<br> <img  height='300px' width='300px' src={} />".format(article["urlToImage"] or "https://www.freeiconspng.com/uploads/no-image-icon-15.png") +"<br>" + "Description: {}".format(article["description"]) + "<br>" + "Source: <a href={}>link </a>".format(article["url"]) + "<br>")
        return output



if __name__ == '__main__':
    app.run()

#%fullscreen
# Welcome back! We got all of your project proposals and there was an almost FLASK

# We will be using Flask, a web framework written in Python. It's what we use to build the programmingfeelthepower.com website! This lets you focus on writing web applications and let Flask do the heavy lifiting in the background. Let's take a look at what you can do!

# First, download `flask_template.zip` and unzip it into your home directory. When you enter flask_template, you'll see a file named `app.py`, and 2 folders named `static` and `templates`. To run the server which will let you see the website, run `python app.py`. Now you can visit <a href="127.0.0.1:5000">127.0.0.1:5000</a> to see your web app in action. 127.0.0.1 is a special url that is for servers which are running locally on your own computer.
# If you see a 'Yay first web app' message, then you have successfully run your first web app!

# If you take a look inside `app.py`, you'll see the following code:
@app.route('/')
def index():
    return 'Yay first web app!'
# The `@app.route('/')` is a special type of syntax called a `decorator`, and it is put above function definitions. This decorator is pretty straightforward - it tells Flask to run the `index` function whenever someone goes to the route `/`. Note that routes are given without the full hostname e.g. the route `/` means someone is requesting the url `127.0.0.1:5000/` and the route `/about` means someone is requesting the url `127.0.0.1:5000/about`
# You can add your own routes in this manner - just make sure that the function you define returns a string like in the example code because this is the data that is returned and displayed by the browser

# You can also use Flask to serve static files! A static file is anything whose contents don't change or don't depend on other information. Examples of this are imgages, pdfs, and most HTML pages.
# To add a static file, simply place it in the `static` folder and then go to the corresponding url. A file located at `static/images/foo.jpg` can be accessed at the url `127.0.0.1/static/images/foo.png`
# There is already a `lu.png` file located in `static`, so visit the corresponding url in your browser and you should see a striking photo of our very own Lu Cheng in his younger days

# Finally, you can use Flask to serve templated files. If you visit `facebook.com` you'll notice that at first the url shows you a page which asks you to login. Once you do so, you'll end up at another page, but the url is still facebook.com! And to add to that, the page you see is different than the page someone else sees at the same url!
# This is an example of a templated page, which is exactly what it sounds like. Facebook has an HTML template for the news feed, but it marks certain places in the file where values need to be inserted (like madlibs). When you visit Facebook, it will read the template file, and start filling in the blanks with your name, email, friends' statuses, etc. If someone else visits Facebook, it will use the same template but fill it in with different information which is why you see different pages.
# We can simulated this in Flask using HTML templates. If you look in the `templates` folder, you should see a file called `random.html`. It's contents should look like `<h1>{{ random_num }} is a random number!</h1>`. The {{ and }} represent a 'template tag'. When Flask processes the templates, it will replace the entire template tag with the value of the `random_num` variable i.e. if `random_num = 5`, then the HTML Flask produces is `<h1>5 is a random number!</h1>`
# You'll notice the following code in `app.py`:
@app.route('/random_example')
def random_example():
    return render_template('random.html', random_num=randint(1, 100))
# which will show the `random.html` template when you visit `127.0.0.1:5000/random_example`. Notice that the number you see will change each time you refresh because `random_num` is set to a random number in the code!

# Cool you have the basics of Flask down! You can start building your website using these tools!

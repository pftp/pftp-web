#%fullscreen
# Welcome back! We got all of your project proposals and a lot of you had a web related project so <a href="http://www.youtube.com/watch?v=olLxrojmvMg">it is time</a> for you to learn about web programming.
# We will be using Flask, a web framework written in Python. It's what we use to build the programmingfeelthepower.com website! This lets you focus on writing web applications and let Flask do the heavy lifiting in the background. Let's take a look at what you can do!

# First, download `flask_template.zip` and unzip it into your home directory. When you enter flask_template, you'll see a file named `app.py`, and 2 folders named `static` and `templates`. To run the server which will let you see the website, run `python app.py`. Now you can visit <a href="http://127.0.0.1:5000">127.0.0.1:5000</a> to see your web app in action. 127.0.0.1 is a special url that is for servers which are running locally on your own computer.
# If you see a 'Yay first web app' message, then you have successfully run your first web app!

# If you take a look inside `app.py`, you'll see the following code:
@app.route('/')
def index():
    return 'Yay first web app!'
# The `@app.route('/')` is a special type of syntax called a `decorator`, and it is put above function definitions. This decorator is pretty straightforward - it tells Flask to run the `index` function whenever someone goes to the route `/`. Note that routes are given without the full hostname e.g. the route `/` means someone is requesting the url `127.0.0.1:5000/` and the route `/about` means someone is requesting the url `127.0.0.1:5000/about`
# You can add your own routes in this manner - just make sure that the function you define returns a string like in the example code because this is the data that is returned and displayed by the browser

# You can also use Flask to serve static files! A static file is anything whose contents don't change or don't depend on other information. Examples of this are imgages, pdfs, and most HTML pages.
# To add a static file, simply place it in the `static` folder and then go to the corresponding url. A file located at `static/images/foo.jpg` can be accessed at the url `127.0.0.1/static/images/foo.png`
# There is already a `lu.png` file located in `static`, so visit the corresponding url in your browser and you should see a striking photo of our very own Lu Cheng in his younger days. You can also find the url for `page1.html`, which is also in the static folder.

# Finally, you can use Flask to serve templated HTML. A template is sort of like an HTML version of <a href="http://0.media.collegehumor.cvcdn.com/98/25/9106a4058cff59571a51450a113d04d9.jpg">Mablibs</a>. You write an HTML file but designate certain portions of it which will be filled in later.
# If you look in the `templates` folder, you should see a file called `random.html`. It's contents should look like normal HTML except for the line `&lt;h1&gt;{{ random_num }} is a random number!&lt;/h1&gt;`. The {{ and }} represent a 'template tag'. When Flask processes the templates, it will replace the entire template tag with the value of the `random_num` variable i.e. if `random_num = 5`, then the HTML Flask produces is `&lt;h1&gt;5 is a random number!&lt;/h1&gt;`
# You'll notice the following code in `app.py`:
@app.route('/random_example')
def random_example():
    return render_template('random.html', random_num=randint(1, 100))
# which 'renders' the `random.html` template by filling in all the template tags. When you visit `127.0.0.1:5000/random_example`, notice that the number you see changes each time!

# Cool you have the basics of Flask down!

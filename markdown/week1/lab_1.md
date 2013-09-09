<script type="text/javascript" src="{{url_for('static', filename='lib/codemirror/lib/codemirror.js') }}"></script>
<script type="text/javascript" src="{{url_for('static', filename='lib/codemirror/mode/python/python.js')}}"></script>
<script type="text/javascript" src="{{url_for('static', filename='lib/skulpt/dist/skulpt.js')}}"></script>
<script type="text/javascript" src="{{url_for('static', filename='lib/skulpt/dist/builtin.js')}}"></script>
<link rel="stylesheet" type="text/css" href="{{url_for('static', filename='lib/codemirror/lib/codemirror.css')}}" />
<link rel="stylesheet" type="text/css" href="{{url_for('static', filename='lib/codemirror/theme/cobalt.css')}}" />

<script type="text/javascript">
  var builtinRead = function(x) {
    if (Sk.builtinFiles === undefined ||
        Sk.builtinFiles['files'][x] === undefined)
      throw "File not found: '" + x + "'";
    return Sk.builtinFiles['files'][x];
  };
  var genOutf = function(execObj) {
    return function(text) {
      if (!('output' in execObj)) {
        execObj['output'] = '';
      }
      execObj['output'] += text;
    };
  };
  var executeCode = function(execObj) {
    try {
      Sk.configure({output: genOutf(execObj), read: builtinRead});
      eval(Sk.importMainWithBody('<stdin>', false, execObj['input']));
    } catch (err) {
      if (err.toString().trim() === "TypeError: Cannot read property 'constructor' of null") {
        execObj['error'] = 'Error: Your function does not have return value. Your function needs a return value.';
      } else if (err.toString().trim() === 'ImportError: No module named <stdin>') {
        execObj['error'] = 'Error: You did not type any code. You must type some code.';
      } else {
        execObj['error'] = err.toString();
      }
    }
  };
  var runit = function(code) {
    var runObj = {'input': code};
    executeCode(runObj);
    if (runObj['output'] !== undefined) {
      $('#lab_output').text(runObj['output']);
    } else {
      $('#lab_output').text(runObj['error']);
    }
    return runObj;
  };

  var lab_content = [
    ["Welcome to Lab 1! We are going to learn some turtle graphics today. Hit the 'Next' button to get started."],
    ["This is Winston, your guide to the magic that is Python.\nDon't worry about what <code>import</code> or <code>turtle.Turtle()</code> means - we will get into that later. All that matters is that we have a turtle and his name is Winston. He will listen to your instructions and execute them in order with no mistakes because he is just that good.",
    'import turtle\nwinston = turtle.Turtle()'],
    ["You can call Winston by his name and tell him to move! Try adding a line at the end that says <code>winston.forward(100)</code>. This tells Winston to move 100 units in the direction he's facing. Hit the 'Run It!' button when you're done to see Winston in action."],
    ["Now try bringing Winston back to where he started with <code>winston.backward()</code> (You still need to supply a number between the parentheses so Winston knows how far to go."],
    ["Winston can even change directions! Try telling Winston to turn right by adding a line at the end that says <code>winston.right(90)</code>."],
    ["Try making Winston spin in a circle counter-clockwise. (Hint: Winston will have to turn left and he only understands angles in degrees."],
    ["Now Winston is pretty smart for a turtle, and using just these commands, you can tell him to draw shapes. Try adding these lines at the end: <pre>winston.right(90)\nwinston.forward(100)\nwinston.right(90)\nwinston.forward(100)\nwinston.right(90)\nwinston.forward(100)\nwinston.right(90)\nwinston.forward(100)</pre>"],
    ["Now it's your turn! Make Winston draw a triangle. You can edit or delete the lines from the previous step to do this."],
    ["Cool! Now normally Winston drags a pen behind him when he moves, and this leaves the lines that you see. You can tell Winston to stop slacking off and carry the pen if you don't want him to draw: <code>winston.penup()</code>. Try adding this line and then make Winston move. You should see that there is no line behind him as he moves this time!"],
    ["You can use this to make separate shapes! Just tell Winston to put his pen back down and draw a shape, and then pick it up while he moves to a different spot to start the next shape. Try adding these lines to see it: <pre>winston.pendown()\nwinston.right(90)\nwinston.forward(100)\nwinston.right(90)\nwinston.forward(100)\nwinston.right(90)\nwinston.forward(100)\nwinston.right(90)\nwinston.forward(100)\n\nwinston.penup()\nwinston.forward(200)\nwinston.pendown()\n\nwinston.right(120)\nwinston.forward(100)\nwinston.right(120)\nwinston.forward(100)\nwinston.right(120)\nwinston.forward(100)</pre>"],
    ["Now you try making a pentagon and a hexagon with some space in between."],
    ['Winston also has one of those giant packs of crayons, so you can tell him to change the color he draws too: <code>winston.color("green")</code>. He will understand the following list of colors: <pre>aliceblue\nantiquewhite\naqua\naquamarine\nazure\nbeige\nbisque\nblack\nblanchedalmond\nblue\nblueviolet\nbrown\nburlywood\ncadetblue\nchartreuse\nchocolate\ncoral\ncornflowerblue\ncornsilk\ncrimson\ncyan\ndarkblue\ndarkcyan\ndarkgoldenrod\ndarkgray\ndarkgreen\ndarkgrey\ndarkkhaki\ndarkmagenta\ndarkolivegreen\ndarkorange\ndarkorchid\ndarkred\ndarksalmon\ndarkseagreen\ndarkslateblue\ndarkslategray\ndarkslategrey\ndarkturquoise\ndarkviolet\ndeeppink\ndeepskyblue\ndimgray\ndimgrey\ndodgerblue\nfirebrick\nfloralwhite\nforestgreen\nfuchsia\ngainsboro\nghostwhite\ngold\ngoldenrod\ngray\ngreen\ngreenyellow\ngrey\nhoneydew\nhotpink\nindianred\nindigo\nivory\nkhaki\nlavender\nlavenderblush\nlawngreen\nlemonchiffon\nlightblue\nlightcoral\nlightcyan\nlightgoldenrodyellow\nlightgray\nlightgreen\nlightgrey\nlightpink\nlightsalmon\nlightseagreen\nlightskyblue\nlightslategray\nlightslategrey\nlightsteelblue\nlightyellow\nlime\nlimegreen\nlinen\nmagenta\nmaroon\nmediumaquamarine\nmediumblue\nmediumorchid\nmediumpurple\nmediumseagreen\nmediumslateblue\nmediumspringgreen\nmediumturquoise\nmediumvioletred\nmidnightblue\nmintcream\nmistyrose\nmoccasin\nnavajowhite\nnavy\noldlace\nolive\nolivedrab\norange\norangered\norchid\npalegoldenrod\npalegreen\npaleturquoise\npalevioletred\npapayawhip\npeachpuff\nperu\npink\nplum\npowderblue\npurple\nred\nrosybrown\nroyalblue\nsaddlebrown\nsalmon\nsandybrown\nseagreen\nseashell\nsienna\nsilver\nskyblue\nslateblue\nslategray\nslategrey\nsnow\nspringgreen\nsteelblue\ntan\nteal\nthistle\ntomato\nturquoise\nviolet\nwheat\nwhite\nwhitesmoke\nyellow\nyellowgreen</pre>'],
    ["Awesome! Now your assignment for this week is to make a picture of something cool"]
  ];
  var section = 0;

  $(function() {
    var editor, execObj, execHistory = [];
    Sk.canvas = 'turtle_canvas';
    Sk.pre = 'lab_output';
    editor = CodeMirror.fromTextArea(document.getElementById('lab_code'), {
      autofocus: true,
      theme: 'cobalt',
      lineNumbers: true,
      indentUnit: 4,
      mode: 'python'
    });
    $('#lab_run_code').click(function(e) {
      var runObj, testObjs, correct,
        code = editor.getValue().replace(/\t/g, '    ');
      runObs = runit(code);
    });
    $('#next_section').click(function() {
      if (section < lab_content.length - 1) {
        section++;
        update(section);
      }
    });
    $('#prev_section').click(function() {
      if (section > 0) {
        section--;
        update(section);
      }
    });
    var update = function(section) {
      $('#lab_text').html(lab_content[section][0]);
      if (lab_content[section][1])
        editor.setValue(lab_content[section][1]);
    };

    update(section);
  });
</script>

Lab 1
=====

<div class="row">
  <div class="span6">
    <div style="height: 200px">
      <div id="lab_text" style="overflow: auto; height: 195px;"></div></br>
    </div>
    <button id="prev_section">Prev</button>
    <button id="next_section">Next</button>
    <textarea id="lab_code" style="display:none;"></textarea>
    <button id="lab_run_code">Run It!</button>
    <pre id="lab_output"></pre>
  </div>
  <div class="span6" id="canvas_container">
    <canvas id="turtle_canvas" width="500" height="500" style="border: 1px solid black;"></canvas>
  </div>
</div>

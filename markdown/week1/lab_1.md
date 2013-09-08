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
  $(function() {
    $('#turtle_canvas').css('width', $("#canvas_container").clientWidth);
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
  });
</script>

Lab 1
=====

<div class="row">
  <div class="span6">
    <textarea id="lab_code" style="display:none;"></textarea>
    <button id="lab_run_code">Run It!</button>
    <pre id="lab_output"></pre>
  </div>
  <div class="span6" id="canvas_container">
    <canvas id="turtle_canvas" style="border: 1px solid black;"></canvas>
  </div>
</div>

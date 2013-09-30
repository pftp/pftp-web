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
  var runObj = {'input': code}, outText = '';
  executeCode(runObj);
  if (runObj['output'] !== undefined) {
    outText += runObj['output'];
  }
  if (runObj['error'] !== undefined) {
    outText += runObj['error'];
  }
  $('#lab_output').text(outText);
  return runObj;
};

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
    var code = editor.getValue().replace(/\t/g, '    ');
    $('#lab_output').text('');
    runit(code);
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

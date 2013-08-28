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
    $('#output').text(runObj['output']);
  } else {
    $('#output').text(runObj['error']);
  }
  return runObj;
};
$(function() {
  var editor, execObj, execHistory = [];
  Sk.canvas = 'turtle_canvas';
  Sk.pre = 'output';
  editor = CodeMirror.fromTextArea(document.getElementById('code_area'), {
    autofocus: true,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python'
  });
  $('#run_code').click(function(e) {
    var runObj, testObjs, correct,
      code = editor.getValue().replace(/\t/g, '    ');
    $('#output').text('');
    runObj = runit(code);
  });
  $('#program_title').tooltip();
  $('#program_title').click(function(e) {
    $('#new_program_title').val($('#program_title').text());
    $('#rename_modal').modal('show');
  });
  $('#rename_ok').click(function(e) {
    $('#program_title').text($('#new_program_title').val());
    $('#rename_modal').modal('hide');
  });
});

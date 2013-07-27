var builtinRead = function(x) {
  if (Sk.builtinFiles === undefined ||
      Sk.builtinFiles['files'][x] === undefined)
    throw "File not found: '" + x + "'";
  return Sk.builtinFiles['files'][x];
};
var genOutf = function(outputs) {
  return function(text) {
    if ($.trim(text) !== '') {
      outputs.push(text);
    }
  };
};
var runit = function(code, outputs) {
  Sk.configure({output: genOutf(outputs), read: builtinRead});
  try {
    eval(Sk.importMainWithBody('<stdin>', false, code));
  } catch (err) {
    if (err.toString().trim() === "TypeError: Cannot read property 'constructor' of null") {
      outputs.push('Error: Your function does not have return value. Your function needs a return value.');
    } else if (err.toString().trim() === 'ImportError: No module named <stdin>') {
      outputs.push('Error: You did not type any code. You must type some code.');
    } else {
      outputs.push(err.toString());
    }
  }
  $('#output').text(outputs[outputs.length-1]);
};
$(function() {
  var editor, inputs = [], outputs = [], curOutput;
  Sk.canvas = 'turtle_canvas';
  Sk.pre = 'output';
  editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    autofocus: true,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python'
  });
  $('#run_code').click(function(e) {
    var code = editor.getValue().replace(/\t/g, '    ');
    inputs.push(code);
    $('#output').text('');
    runit(code, outputs);
  });
  $('#show_hint').click(function(e) {
    $('#show_hint').hide();
    $('#hint_wrapper').show();
  });
});

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
  $('#practice_output').text(outText);
  return runObj;
};
$(function() {
  var editor, execObj, execHistory = [], got_hint = false,
    start_time = new Date().getTime() / 1000;
  Sk.canvas = 'turtle_canvas';
  Sk.pre = 'practice_output';
  editor = CodeMirror.fromTextArea(document.getElementById('practice_code'), {
    autofocus: true,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python',
    extraKeys: {"Enter": false}
  });
  $('#practice_run_code').click(function(e) {
    var runObj, testObjs, correct, template_vars, test_code, code,
      result_no_test, result_test, result_no_test_error, result_test_error,
      submit_time;
    template_vars = $('#template_vars').text().trim();
    test_code = $('#test_cases').text().trim();
    concept_names = $('#concept_names').text().trim();
    code = editor.getValue().replace(/\t/g, '    ');
    result_no_test = '';
    result_no_test_error = false;
    result_test = '';
    result_test_error = false;
    submit_time = new Date().getTime() / 1000;

    $('#practice_output').text('');
    runObj = runit(code);
    if (runObj['output'] !== undefined) {
      result_no_test += runObj['output'];
    }
    if (runObj['error'] !== undefined) {
      result_no_test += runObj['error'];
      result_no_test_error = true;
    }
    testObj = {'input': code + '\n' + test_code};
    executeCode(testObj);
    if (testObj['output'] !== undefined) {
      result_test += testObj['output'];
    }
    if (testObj['error'] !== undefined) {
      result_test += testObj['error'];
      result_test_error = true;
    }
    $.ajax({
      type: 'POST',
      url: 'submit/',
      data: {
        code: code,
        result_test: result_test,
        result_test_error: result_test_error,
        result_no_test: result_no_test,
        result_no_test_error: result_no_test_error,
        start_time: start_time,
        submit_time: submit_time,
        got_hint: got_hint,
        template_vars: template_vars,
        concept_names: concept_names
      },
      success: function(data) {
        if (data == "correct") {
          alert("Nice Job! You're done");
        } else {
          alert(data);
        }
      }
    });
  });
  $('#next_exercise').click(function(e) {
    window.location.href = $('#next_exercise').attr('href');
  });
  $('#show_hint').click(function(e) {
    $('#show_hint').hide();
    $('#show_solution').show();
    $('#hint_wrapper').show();
  });
  $('#show_solution').click(function(e) {
    $('#show_solution').hide();
    $('#solution_wrapper').show();
  });
});

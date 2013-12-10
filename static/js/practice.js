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
    } else if (err.toString().trim() === 'ImportError: No module named <stdin> on line <unknown>') {
      execObj['error'] = 'Error: You did not type any code. You must type some code.';
    } else {
      execObj['error'] = err.toString();
    }
  }
};
var runit = function(code) {
  var runObj = {'input': code};
  executeCode(runObj);
  return runObj;
};
var submitCode = function(editor, startTime, gotHint, gaveUp) {
  var runObj, testObjs, correct, template_vars, test_code, code, result_no_test,
    result_test, result_no_test_error, result_test_error, submit_time,
    successFunc;
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
  if (!gaveUp) {
    $('#practice_output').text(result_no_test);
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
  if (gaveUp) {
    successFunc = function(data) {
      window.location.href = '/practice/' + data['next_problem'];
    }
  } else {
    successFunc = function(data) {
      if (data['correct'] === 'correct') {
        $('#solution').text(data['solution']);
        $('#correct_modal').modal('show');
        $('#give_up').hide();
        $('#modal_next_exercise').attr('href', '/practice/' + data['next_problem']);
        $('#next_exercise').attr('href', '/practice/' + data['next_problem']);
        $('#next_exercise').show();
      } else if (data['correct'] === 'error') {
        $('#error_modal').modal('show');
      } else {
        $('#failure_quote').text(data['failure_quote'][0]);
        $('#failure_quote_author').text(data['failure_quote'][1]);
        $('#incorrect_modal').modal('show');
      }
    }
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
      start_time: startTime,
      submit_time: submit_time,
      got_hint: gotHint,
      gave_up: gaveUp,
      template_vars: template_vars,
      concept_names: concept_names
    },
    dataType: 'json',
    success: successFunc
  });
}
$(function() {
  var editor, got_hint = false, start_time = new Date().getTime() / 1000;
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
    $('#practice_run_code').prop('disabled', true);
    $('#give_up').prop('disabled', true);
    submitCode(editor, start_time, got_hint, false);
  });
  $('#give_up').click(function(e) {
    $('#practice_run_code').prop('disabled', true);
    $('#give_up').prop('disabled', true);
    $('#give_up_modal').modal('show');
  });
  $('#give_up_confirm').click(function(e) {
    $('#practice_run_code').prop('disabled', true);
    $('#give_up').prop('disabled', true);
    submitCode(editor, start_time, got_hint, true);
  });
  $('#show_hint').click(function(e) {
    got_hint = true;
    $('#show_hint').hide();
    $('#hint_wrapper').show();
    $('#no_hint_yet').hide();
  });
  // Fix bug where we cannot select text that is blocked by hidden modal
  $('.modal').on('show.bs.modal', function (e) {
    $('.modal').css('z-index', 1050);
  })
  $('.modal').on('hidden.bs.modal', function (e) {
    $('.modal').css('z-index', -1);
    $('#practice_run_code').prop('disabled', false);
    $('#give_up').prop('disabled', false);
  })
});

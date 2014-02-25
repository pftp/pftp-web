//HACKHACK hijack console.log to capture output
(function(){
  var nativeLog = console.log;
  console.log = function() {
    //record all log messages
    console._history = console._history || [];
    var args = Array.prototype.slice.call(arguments);
    console._history.push(args.join(" "));
    nativeLog.apply(console, arguments);
  };
})();

var executeCode = function(execObj) {
  try {
    //TODO jsHint for better style
    console._history = [];
    eval(execObj['input']);
    execObj['output'] = console._history.join('\n');
  } catch (err) {
    //TODO write better error messages
    if (console._history.length > 0) {
      execObj['output'] = console._history.join('\n') + '\n';
    }
    execObj['output'] += err.toString();
    execObj['error'] = true;
  }
};
var runit = function(code) {
  var runObj = {'input': code, 'output': ''};
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

  $('#homework_output').text('');
  runObj = runit(code);
  if (runObj['output'] !== undefined) {
    result_no_test += runObj['output'];
  }
  if (runObj['error'] !== undefined) {
    result_no_test += runObj['error'];
    result_no_test_error = true;
  }
  if (!gaveUp) {
    $('#homework_output').text(result_no_test);
    if (result_no_test !== '') {
      $('#correct_output').text(result_no_test);
      $('#correct_output_container').show();
    } else {
      $('#correct_output_container').hide();
    }
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
      window.location.href = '/practice/javascript';
    }
  } else {
    successFunc = function(data) {
      if (data['correct'] === 'correct') {
        $('#solution').text(data['solution']);
        $('#correct_modal').modal('show');
        $('#give_up').hide();
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
  // TODO Timeout if code takes more than 1 second to run
  editor = CodeMirror.fromTextArea(document.getElementById('homework_code'), {
    autofocus: true,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'javascript',
    extraKeys: {"Enter": false}
  });
  $('#homework_submit_code').click(function(e) {
    var runObj;
    $('#homework_submit_code').prop('disabled', true);
     runObj = runit(editor.getValue());
     // TODO: finish me
  });
  $('#homework_run_code').click(function(e) {
    var runObj = runit(editor.getValue());
    $('#homework_output').text(runObj['output']);
  });
  // Fix bug where we cannot select text that is blocked by hidden modal
  $('.modal').on('show.bs.modal', function (e) {
    $('.modal').css('z-index', 1050);
  })
  $('.modal').on('hidden.bs.modal', function (e) {
    $('.modal').css('z-index', -1);
    $('#homework_run_code').prop('disabled', false);
  })
});

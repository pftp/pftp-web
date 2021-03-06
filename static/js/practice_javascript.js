//HACKHACK hijack console.log to capture output
(function(){
  var nativeLog = console.log;
  console.log = function() {
    var args, i;
    //record all log messages
    console._history = console._history || [];
    args = Array.prototype.slice.call(arguments);
    for (i = 0; i < args.length; i++) {
      if (args[i] === null) {
        args[i] = "null";
      } else if (args[i] === undefined) {
        args[i] = "undefined";
      }
    }
    console._history.push(args.join(" "));
    nativeLog.apply(console, arguments);
  };
})();

var executeCode = function(execObj) {
  try {
    //clear log messages
    console._history = [];
    eval(execObj['input']);
    execObj['output'] = console._history.join('\n');
  } catch (err) {
    //TODO write better error messages
    execObj['error'] = err.toString();
  }
};
var runit = function(code) {
  var runObj = {'input': code};
  executeCode(runObj);
  return runObj;
};
var submitCode = function(editor, gotHint, gaveUp) {
  var runObj, testObjs, correct, template_vars, test_code, code, result_no_test,
    result_test, result_no_test_error, result_test_error, successFunc,
    startTime;
  template_vars = $('#template_vars').text().trim();
  test_code = $('#test_cases').text().trim();
  concept_names = $('#concept_names').text().trim();
  code = editor.getValue().replace(/\t/g, '    ');
  result_no_test = '';
  result_no_test_error = false;
  result_test = '';
  result_test_error = false;
  startTime = $('#start_time').text().trim();

  $('#output').text('');
  runObj = runit(code);
  if (runObj['output'] !== undefined) {
    result_no_test += runObj['output'];
  }
  if (runObj['error'] !== undefined) {
    result_no_test += runObj['error'];
    result_no_test_error = true;
  }
  if (!gaveUp) {
    $('#output').text(result_no_test);
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
  var got_hint = false;
  // TODO Timeout if code takes more than 1 second to run

  var editor = ace.edit('editor');
  editor.setTheme('ace/theme/monokai');
  editor.getSession().setMode('ace/mode/javascript');

  $('#practice_run_code').click(function(e) {
    $('#practice_run_code').prop('disabled', true);
    $('#give_up').prop('disabled', true);
    submitCode(editor, got_hint, false);
  });

  $('#give_up').click(function(e) {
    $('#practice_run_code').prop('disabled', true);
    $('#give_up').prop('disabled', true);
    $('#give_up_modal').modal('show');
  });

  $('#give_up_confirm').click(function(e) {
    $('#practice_run_code').prop('disabled', true);
    $('#give_up').prop('disabled', true);
    submitCode(editor, got_hint, true);
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

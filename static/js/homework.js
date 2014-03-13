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
  var runObj = {'input': code, 'output': '', 'error': false};
  executeCode(runObj);
  return runObj;
};
var submitCode = function(code) {
  var runObj, testObjs, correct, template_vars, test_code, successFunc,
    startTime;
  problem_name = $('#problem_name').text().trim();
  template_vars = $('#template_vars').text().trim();
  test_code = $('#test_cases').text().trim();
  concept_names = $('#concept_names').text().trim();
  startTime = $('#start_time').text().trim();

  runObj = runit(code);
  testObj = runit(code + '\n' + test_code);
  $('#homework_output').text(runObj['output']);
  if (runObj['output'] !== '') {
    $('#correct_output').text(runObj['output']);
    $('#correct_output_container').show();
  } else {
    $('#correct_output_container').hide();
  }
  successFunc = function(data) {
    if (data['correct'] === 'correct') {
      $('#solution').text(data['solution']);
      $('#correct_modal').modal('show');
      $('#next_problem').show();
    } else if (data['correct'] === 'error') {
      $('#error_modal').modal('show');
    } else {
      $('#failure_quote').text(data['failure_quote'][0]);
      $('#failure_quote_author').text(data['failure_quote'][1]);
      $('#incorrect_modal').modal('show');
    }
  }
  $.ajax({
    type: 'POST',
    url: '/practice/javascript/' + problem_name + '/submit/',
    data: {
      code: code,
      result_test: testObj['output'],
      result_test_error: testObj['error'],
      result_no_test: runObj['output'],
      result_no_test_error: runObj['error'],
      start_time: startTime,
      got_hint: false,
      gave_up: false,
      template_vars: template_vars,
      concept_names: concept_names
    },
    dataType: 'json',
    success: successFunc
  });
};
$(function() {
  var got_hint = false;
  // TODO Timeout if code takes more than 1 second to run
  var editor = ace.edit('homework_code');
  editor.setTheme('ace/theme/monokai');
  editor.getSession().setMode('ace/mode/javascript');

  $('#homework_submit_code').click(function(e) {
    $('#homework_submit_code').prop('disabled', true);
    submitCode(editor.getValue());
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
    $('#homework_submit_code').prop('disabled', false);
  })
});

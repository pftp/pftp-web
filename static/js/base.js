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
var testit = function(code) {
  var testCases, testCase, testObj, runLines, testResult, testObjs = [];
  testCases = JSON.parse($('#test_cases').text());
  for (testCase in testCases) {
    if (testCases.hasOwnProperty(testCase)) {
      testObj = {};
      if (testCase !== '') {
        testObj['input'] = code + '\nprint\nprint repr(' + testCase + ')';
      } else {
        testObj['input'] = code;
      }
      testObj['expected'] = testCases[testCase];
      executeCode(testObj);
      if (testObj['output'] !== undefined) {
        if (testCase !== '') {
          runLines = testObj['output'].split('\n');
          testObj['output'] = runLines[runLines.length - 2];
        }
        testResult = testObj['output'];
      } else {
        testResult = testObj['error'];
      }
      testObj['correct'] = (testObj['expected'] === testResult) ? 1 : 0;
      testObjs.push(testObj);
    }
  }
  return testObjs;
};
$(function() {
  var editor, execObj, execHistory = [];
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
    var runObj, testObjs, correct,
      code = editor.getValue().replace(/\t/g, '    ');
    $('#output').text('');
    runObj = runit(code);
    /*
    testObjs = testit(code);
    correct = testObjs.reduce(function(acc, testObj) {
      return acc && testObj['correct'];
    }, true);
    if (correct) {
      $('#next_exercise').show();
    }
   */
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
  $('#toggle_console').click(function(e) {
    var href = $(e.currentTarget).attr('href');
    if (href === '#console') {
      $(e.currentTarget).attr('href', '#');
    } else if (href === '#') {
      $(e.currentTarget).attr('href', '#console');
    }
  });
});

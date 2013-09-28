var editor, saveTimer, programId;
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
  $('#output').text(outText);
  return runObj;
};
var saveCode = function() {
  var saveData = {
    title: $('#program_title').text(),
    code: editor.getValue()
  };
  if (programId !== '-1') {
    saveData['program_id'] = programId;
  }
  $('#save_msg').text('Saving...');
  clearTimeout(saveTimer);
  $.ajax({
    type: 'POST',
    url: '/save_program/',
    data: saveData
  }).done(function(pid) {
    programId = pid;
    $('#save_msg').text('All changes saved');
  });
};
$(function() {
  var execObj, execHistory = [];
  programId = $('#program_id').text();
  if (isNaN(programId)) {
    programId = '-1';
  }
  Sk.canvas = 'turtle_canvas';
  Sk.pre = 'output';
  editor = CodeMirror.fromTextArea(document.getElementById('code_area'), {
    autofocus: true,
    width: 500,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python'
  });
  $('#run_code').click(function(e) {
    var runObj, testObjs, correct, codeRunData,
    code = editor.getValue().replace(/\t/g, '    ');
    $('#output').text('');
    runObj = runit(code);
    codeRunData = {
      title: $('#program_title').text(),
      code: code,
      output: runObj['output'],
      error: runObj['error'],
      program_id: programId
    };
    $.ajax({
      type: 'POST',
      url: '/save_code_run/',
      data: codeRunData
    });
  });
  $('#run_server_code').click(function(e) {
    $.ajax({
      type: 'POST',
      url: '/run_server_code/',
      data: {
        title: $('#program_title').text(),
        code: editor.getValue().replace(/\t/g, '    ')
      }
    }).done(function(output) {
      $('#output').text(output);
    });
  });
  $('#save_code').click(function(e) {
    saveCode();
  });
  $('#program_title').tooltip();
  $('#save_code_disabled').tooltip();
  $('#program_title').click(function(e) {
    $('#new_program_title').val($('#program_title').text());
    $('#rename_modal').modal('show');
  });
  $('#rename_ok').click(function(e) {
    $('#program_title').text($('#new_program_title').val());
    $('#rename_modal').modal('hide');
    saveCode();
  });
  editor.on('change', function(cm, changeObj) {
    $('#save_msg').text('Saving...');
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveCode, 1000);
  });
});

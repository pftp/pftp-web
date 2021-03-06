var editor, saveTimer, programId, section;
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
var saveCode = function() {
  var saveData = {
    title: 'Lab ' + $('#lab_id').text(),
    code: editor.getValue(),
    section: section,
    lab_id: $('#lab_id').text()
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
var update = function(section, updateCode) {
  $('#lab_text').html(lab_content[section][0]);
  $('#lab_text').scrollTop(0);
  if (updateCode && lab_content[section][1])
    editor.setValue(lab_content[section][1]);
};
$(function() {
  programId = $('#program_id').text();
  if (isNaN(programId)) {
    programId = '-1';
  }
  section = parseInt($('#section').text());
  if (isNaN(section)) {
    section = 0;
  }
  Sk.canvas = 'turtle_canvas';
  Sk.pre = 'lab_output';

  editor = ace.edit('lab_code');
  editor.setTheme('ace/theme/monokai');
  editor.getSession().setMode('ace/mode/python');

  $('#lab_run_code').click(function(e) {
    var code = editor.getValue().replace(/\t/g, '    ');
    $('#lab_output').text('');
    runit(code);
  });

  $('#next_section').click(function() {
    if (section < lab_content.length - 1) {
      section++;
      update(section, true);
      saveCode();
    }
  });

  $('#prev_section').click(function() {
    if (section > 0) {
      section--;
      update(section, false);
      saveCode();
    }
  });

  update(section, true);

  $('#save_canvas').click(function() {
    var uri = $('#turtle_canvas')[0].toDataURL();
    window.open(uri, '_blank');
  });

  editor.on('change', function(e) {
    $('#save_msg').text('Saving...');
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveCode, 1000);
  });
});

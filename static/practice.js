$(function() {
  var editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    autofocus: true,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python'
  });
});

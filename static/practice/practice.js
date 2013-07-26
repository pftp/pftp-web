function outf(text) {
  var mypre = document.getElementById("output");
  mypre.innerHTML = mypre.innerHTML + text;
}
function builtinRead(x) {
  if (Sk.builtinFiles === undefined ||
      Sk.builtinFiles["files"][x] === undefined)
    throw "File not found: '" + x + "'";
  return Sk.builtinFiles["files"][x];
}
$(function() {
  var editor;
  editor = CodeMirror.fromTextArea(document.getElementById('code'), {
    autofocus: true,
    theme: 'cobalt',
    lineNumbers: true,
    indentUnit: 4,
    mode: 'python'
  });
  $('#run_code').click(function(e) {
    var code;
    code = editor.getValue().replace(/\t/g, '    ');
    Sk.canvas = "turtle_canvas";
    Sk.pre = "output";
    Sk.configure({output: outf, read: builtinRead});
    eval(Sk.importMainWithBody("<stdin>", false, code));
  });
});

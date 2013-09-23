$(function() {
  $('#submit_quiz').click(function(e) {
    selected = [];
    $(":radio:checked").each(function (i) {
      selected.push($(this).val());
    });

    $.ajax({
      type: 'POST',
      url: 'submit/',
      data: {
        selected: selected
      }
    }).done(function() {
      $('#quiz_container').html('<br><br><br><br><br><h1 style="font-size:1000%"> NICE JOB! </h1>');
      setTimeout(function() {window.location.href = '/'; }, 1500);
    });
  });
});

$(document).ready(function() {
  $('#student_name').autocomplete({
      source: students
  });

  $('#submit_grade').click(function() {
    var assignment = $('#assignment_id').val();
    var name = $('#student_name').val();
    var score = $('#assignment_score').val();

    if (!assignment || !name || !score)
      return;

    data = new FormData();
    data.append('assignment_id', assignment);
    data.append('score', score);

    for (var id in id_map) {
      if (id_map[id] === name) {
        data.append('user_id', id);

        $.ajax({
            type: 'POST',
            url: '/admin/submit_grade/',
            data: data,
            contentType: false,
            processData: false,
            success: function(g) {
              $('#student_name').val('');
              $('#score').val('');
              $('#student_name').focus();
            }
        });
      }
    }
  });
});

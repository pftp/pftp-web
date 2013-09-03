var students = new Array();
$(document).ready(function() {
  $('#student_name').autocomplete({
    source: students
  });
  $('#assignment_name').change(function(e) {
    $('#max_score').html('out of ' + assignment_to_score[$('#assignment_name').val()]);
  });
  $('#assignment_score').keypress(function(e) {
    if (e.which == 13) {
      data = {};
      data['assignment_name'] = $('#assignment_name').val();
      data['student_name'] = $('#student_name').val();
      data['score'] = $('#assignment_score').val();
      $.ajax({
        type: 'POST',
        url: '/admin/submit_grade/',
        data: JSON.stringify(data),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(g) {
          $('#student_name').val('');
          $('#score').val('');
          $('#student_name').focus();
        }
      });
    }
  });
});

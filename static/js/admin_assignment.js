$(function() {
  $('.submit-grade').click(function(e) {
    var userId, assignmentId, score;
    e.preventDefault();
    assignmentId = $('#assignment_id').text();
    userId = $(e.currentTarget).data('user-id');
    score = $('#score'+userId).val();
    $('#score_display').text(score);
    $('#user_name_display').text($(e.currentTarget).data('user-name'));
    $.ajax({
      type: 'POST',
      url: '/admin/submit_grade/',
      data: { assignment_id: assignmentId, user_id: userId, score: score }
    }).done(function() {
      $('#submit_ok_modal').modal('show');
    });
  });
});

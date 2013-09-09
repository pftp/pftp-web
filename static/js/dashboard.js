$(function() {
  var submitAssignmentId, submitProgramId;
  $('.submit-assignment').click(function(e) {
    submitAssignmentId = $(e.currentTarget).data('assignment-id');
    $('.submit-assignment-name').text($(e.currentTarget).data('assignment-name'));
  });
  $('.choose-program').click(function(e) {
    e.preventDefault();
    submitProgramId = $(e.currentTarget).data('program-id');
    $('#submit_program_title').text($(e.currentTarget).text());
  });
  $('.view-submission').click(function(e) {
    e.preventDefault();
    $('#view_submission_name').text($(e.currentTarget).data('assignment-name'));
    $('#view_submission_code').text($(e.currentTarget).data('submission-code'));
  });
  $('#submit_ok').click(function(e) {
    $.ajax({
      type: 'POST',
      url: '/submit_assignment/',
      data: {
        assignment_id: submitAssignmentId,
        program_id: submitProgramId
      }
    }).done(function() {
      location.reload();
    });
  });
});

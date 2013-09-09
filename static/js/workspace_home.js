var saveCode = function() {
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
  var submitProgramId, deleteProgramId;
  $('.submit-program').click(function(e) {
    submitProgramId = $(e.currentTarget).data('program-id');
    $('#submit_program_title').text($(e.currentTarget).data('program-title'));
  });
  $('.delete-program').click(function(e) {
    deleteProgramId = $(e.currentTarget).data('program-id');
    $('#delete_program_title').text($(e.currentTarget).data('program-title'));
  });
  $('#delete_ok').click(function(e) {
    $.ajax({
      type: 'POST',
      url: '/delete_program/',
      data: { program_id: deleteProgramId }
    }).done(function() {
      location.reload();
    });
  });
});

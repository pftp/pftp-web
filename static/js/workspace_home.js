$(function() {
  var deleteProgramId;
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

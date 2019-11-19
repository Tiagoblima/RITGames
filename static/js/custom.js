$( document ).ready(function() {
$(function () {
  $("#btnForm").click(function () {
    $("#formModalCenter")._dialog({
      title:"Dodaj opinie",
      width: 430,
      height: 200,
      modal:true,
      buttons: {
        Close:
        function(){
          $(this)._dialog('close');
        }
      }
    });

  });
})


});


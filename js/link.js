jQuery(document).ready(function($)
    {

	$(".hidden_id").keypress(function()
		{
//        if(($(this).val().length)>15){
//		    e.preventDefault();
		    var txt = $(".hidden_id").val();
            geturl = new RegExp(
          "(^|[ \t\r\n])((ftp|http|https|gopher|mailto|news|nntp|telnet|wais|file|prospero|aim|webcal):(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-]))"
         ,"g"
       );
//            var urls = geturl.exec($(this).val());
//            $(".entradeta").val(urls);
//            alert(urls[0]);
//            $('#urls').html(url[0]);
		    $.post("/link/", $(this).serializeArray(),
			  function(data) {
			      if(data["voteobj"]) {
                      alert(data["voteobj"])
				  alert.text("-");
			      }
			      else {
				  alert.text("+");
                      alert(data)
			      }
			  }


            );


		});
    });

//
//
//
//jQuery(document).ready(function($)
//    {
//	$("#id_text").keypress(function()
//		{
//            if ($('#id_text').length > 0) {
//    // the element exists
//
//             var text = $('#id_text').val();
//
////                document.getElementById('id_entradilla').value="yes";
//
////            document.getElementById('id_entradilla').value="yes";
//            $.ajax({
//                url: "/links/",
//                data: {
//                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
//                    text: text},
//                type: "POST",
//                success: function(data) {
//                    alert("Congratulations! You scored: "+data);
//                },
//
//                error: function(){
//                    document.getElementById('id_entradilla').value='si';
//                }
//
//
//
////               $.get('/links', {text: text}, function(data){
//
//
////               $('#like_count').html(data);
////               $('#likes').hide();
////           });
//
//
//		});
//    }
//    });
//    });


/**
 * Created with PyCharm.
 * User: sergi
 * Date: 19/08/14
 * Time: 08:11
 * To change this template use File | Settings | File Templates.
 */
jQuery(document).ready(function($)
    {
    $(".votedebat_form").submit(function(e)
		{
		    e.preventDefault();
		    var btn = $("button", this);
		    var l_id = $(".hidden_id", this).val();
		    btn.attr('disabled', true);
		    $.post("/votedebat/", $(this).serializeArray(),
			  function(data) {
			      if(data["votedebatobj"]) {
				  btn.text("-");
			      }
			      else {
				  btn.text("+");
			      }
			  });
		    btn.attr('disabled', false);
		});
    });
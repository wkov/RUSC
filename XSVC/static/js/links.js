

$(document).ready(function()
{
//araaaaaaaaaaaaaaaaaaaafunction urlExists(url, callback){
//  $.ajax({
//    type: 'HEAD',
//    url: url,
//    success: function(){
//      callback(true);
//    },
//    error: function() {
//      callback(false);
//    }
//  });
//}
//urlExists(url, function(exists){
//  //do more stuff based on the boolean value of exists
//});

//function urlExists(url, callback){
//  $.ajax({
//    type: 'HEAD',
//    url: url,
//    success: function(){
//      callback(true);
//    },
//    error: function() {
//      callback(false);
//    }
//  });
//}
//urlExists(url, function(exists){
//  //do more stuff based on the boolean value of exists
//});

$("#aportacio").submit(function(e)
{
    var f = $("#l1").attr('href')
    var s = $("#url", this)
    if(f){
        s.val(f);
        $.post("/link/", $(this).serializeArray());
         var f2 = $("#l2").attr('href')
        if(f2){
            s.val(f2);
            $.post("/link/", $(this).serializeArray());
            var f3 = $("#l3").attr('href')
            if(f3){
                s.val(f3);
                $.post("/link/", $(this).serializeArray());
                var f4 = $("#l4").attr('href')
                if(f4){
                    s.val(f4);
                    $.post("/link/", $(this).serializeArray());
        }
        }
        }
    }


});
$("#id_text").keyup(function(e)
{

   var links = new Array;
   var text = $('#id_text').val();
   var regexp = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
//   var urlExists = (function(url){
//        return $.ajax({
//            type: 'HEAD',
//            url : url
//        });
//   });

    var url;


e.preventDefault();

   while(matches = regexp.exec(text))
{

url=matches[0];
links.push(url);

}
if(links.length>0){
$.ajax({
//                cache: false,
//                async: false,
                url: "/url/",
                data: {
//                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                    'links[]': links},
                type: "POST",
                success: function(response) {
//     $.post("/url/", links,
//			  function(data) {


                    var z = 0
    var i = 0
    var final_links = new Array;
    var f = $("#l1").attr('href')

//    var
    if(f){
    final_links.push(f);
         f = $("#l2").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l3").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }
    }
    while(response[i])
    {
        if(response[i] == final_links[0]||response[i] == final_links[1]||response[i] == final_links[2]||response[i] == final_links[3]){
            i++;
            continue
        }
        else{
            final_links.push(response[i]);
            z=1;
        }
        i++;

//        $("#result").html("<a href='"+links[i]+"' class='oembed'/>").add()


    }
    var d;
    var input;
    if(z==1){
//        while(final_links[d]){
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
//            $('<button/>', {
//                text: 'holaaaaaaaa', //set text 1 to 10
//                id: 'l1',
//                click: function remove_link(){
//
//
//
//
//                }
//    });
            $("#result1").html(("<a href='"+final_links[d]+"' id='l1' class='oembed' />link1</a> <button type='button' class='r1'>x</button>"))
            $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'/>link2</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'/>link3</a> <button type='button' class='r3'>x</button>").add()
            $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'/>link4</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
    }
            }
        }



},
                    error: function(){
//                    links.push(matches[0]);
                }
   })
}


//        urlExists(matches[0])
//           .done(function() {
//             links.push(matches[0]);
//           }).fail(function() {
////             links.push(matches[0]);
//            });




//     urlExists(matches[0], function(success) {
//                                                                     if (success) {
//                                                                                        links.push(matches[0]);
//                                                                                      }
//                               });










//    exists = urlExists(matches[0]);
//  //do more stuff based on the boolean value of exists
//
//        if(exists==true){
//        links.push(matches[0]);
//        }

//    if((urlExists(matches[0]))=='True'){
//        links.push(matches[0]);
//    }








//   links.each(links, function(url){
//  $('#result').fadeIn(400);
//
//  $(".oembed").oembed(url,
//                        {
//                        embedMethod: "append", // you can use .. fill , auto , replace
//                        maxWidth: 600,
//                        maxHeight: 350,
//                        });
//});
//            geturl = new RegExp(
//          "(^|[ \t\r\n])((ftp|http|https|gopher|mailto|news|nntp|telnet|wais|file|prospero|aim|webcal):(([A-Za-z0-9$_.+!*(),;/?:@&~=-])|%[A-Fa-f0-9]{2}){2,}(#([a-zA-Z0-9][a-zA-Z0-9$_.+!*(),;/?:@&~=%-]*))?([A-Za-z0-9$_+!*();/?:~-]))"
//         ,"g"
//       );

//   var urls = geturl.exec($(this).val());


//  $('#result').fadeIn(400);
//
//  $("#result").oembed(text,
//                        {
//                        embedMethod: "append", // you can use .. fill , auto , replace
//                        maxWidth: 600,
//                        maxHeight: 350,
//                        });


//  $('#box').val("");

//- See more at: http://www.lessoncup.com/2013/12/jquery-extract-data-from-url.html#sthash.rsQPr69W.dpuf

//var content=$(this).val();
//var urlRegex = /(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
//// Filtering URL from the content using regular expressions
//var url= content.match(urlRegex);
//
//if(url.length>0)
//{
//$("#linkbox").slideDown('show');
//$("#linkbox").html("<img src='link_loader.gif'>");
//// Getting cross domain data
//$.get("/link/="+url,function(response)
//{
//// Loading <title></title>data
//var title=(/<title>(.*?)<\/title>/m).exec(response)[1];
//// Loading first .png image src='' data
//var logo=(/src='(.*?).png'/m).exec(response)[1];
//$("#linkbox").html("<img src='"+logo+".png' class='img'/><div><b>"+title+"</b><br/>"+url)
//});
//
//}
//return false;
});
//gestionem a continuacio el borrat de links ja afegits

$(".r1").on('click',function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l2").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l3").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }

        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()

        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed' />link1</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'/>link2</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'/>link3</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'/>link4</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
        }



    });

$(".r2").on('click',function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l1").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l3").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }


        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()



        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed' />link1</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'/>link2</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'/>link3</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'/>link4</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
        }



    });

$(".r3").on('click',function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l1").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l2").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l4").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }


        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()



        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed' />link1</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'/>link2</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'/>link3</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'/>link4</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
        }




    });

 $(".r4").on('click',function(){

//        $("#result1").html("").add()


        var final_links = new Array;

        var f = $("#l1").attr('href')
        if(f){
            final_links.push(f);
            f = $("#l2").attr('href')
            if(f){
                final_links.push(f);
                f = $("#l3").attr('href')
                if(f){
                    final_links.push(f);
        }
        }
        }


        $("#result1").html("").add()
        $("#result2").html("").add()
        $("#result3").html("").add()
        $("#result4").html("").add()



        var d;
        for (d = 0; d < final_links.length; ++d) {
            if(d==0){
            $("#result1").html("<a href='"+final_links[d]+"' id='l1' class='oembed' />link1</a> <button type='button' class='r1'>x</button>").add()
              $("#l1").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
                }
            if(d==1){
            $("#result2").html("<a href='"+final_links[d]+"' id='l2' class='oembed'/>link2</a> <button type='button' class='r2'>x</button>").add()
            $("#l2").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==2){
            $("#result3").html("<a href='"+final_links[d]+"' id='l3' class='oembed'/>link3</a> <button type='button' class='r3'>x</button>").add()
             $("#l3").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
            if(d==3){
            $("#result4").html("<a href='"+final_links[d]+"' id='l4' class='oembed'/>link4</a> <button type='button' class='r4'>x</button>").add()
            $("#l4").oembed(null,
                {
                embedMethod: "append", // you can use .. fill , auto , replace
                maxWidth: 600,
                maxHeight: 350
                });
            }
        }




    });












});
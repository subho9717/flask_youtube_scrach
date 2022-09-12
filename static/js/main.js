$(document).ready(function(){
  // $("#comment_table").hide();
  


  var count = 0;
  var counter = setInterval(function(){
  if (count < 101){
    $('.count').text(count + '%');
    $('.loader').css('width', count +  '%')
    count++
  }
  else{
    clearInterval(counter)
  }
})

  $('#videourlform').on('submit',function(e){
    $('#preloader').show()

    // alert($('#videourl').val(),$('#videounum').val())
    videourl = $('#videourl').val()
    videounum = $('#videounum').val()
    console.log(videounum,videourl)
    //   $.ajax({
    //     url: "/video_url",
    //     type: "POST",
    //     data: {'videourl':videourl,'videounum':videounum},

    //   }).done(function(data){
    //     console.log(data)
    //     window.location = data;
    //    })
    //   e.preventDefault();
  //
  //
  });
  // var display =  $("#comment_table").css("display");
  //   if(display!="none")
  //   {
  //       $("#comment_table").attr("style", "display:none");
  //   }
  // $('#comment').click(function(e){
  //   $("#comment_table").show();
  // })

  // $("#comment_table tr td").each(function(){
  //   var emptyrows = $.trim($(this).text());
  //   console.log(emptyrows.length)
  //   if (emptyrows.length == 0){
  //     $("#comment_table").hide();
  //   }
  // }); 
  var trd_count = $("#comment_table tr ").length
  if (trd_count < 2){
        $("#comment_table").hide();
      }

  })
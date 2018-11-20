$(document).ready(function() {

  $("textarea").text("");
  $('#search-popup-btn').on('click', function(){
    $('.wrap').toggleClass('active');
    $('.type-input').css('visibility','visible'); 
  });

  $('#mic-popup-btn').on('click', function(){
   
    speak("Hello! How may I help you?");
    $('.wrap').toggleClass('active');
    $('.mic-search-box').css('visibility','visible');

    
        if (annyang) 
        {
          
          setTimeout(function(){ annyang.start(); }, 3000);

          annyang.addCallback('result', function(userSaid) {
          annyang.abort();
          $('.mic-input').text(userSaid[0]);
          speak("Please wait while we process your query");

          fetch_result(userSaid[0]);

          });
        }


    
  });

  $('.close-button').click(function()
  {
     $('.mic-search-box').css('visibility','hidden');
     $('.type-input').css('visibility','hidden');
     $('.wrap.active').toggleClass('active');
     $('textarea').text("");
  });

  $('#submit-query').click(function()
  {
    fetch_result_text($('#type-input').text());
  });

});

function speak(dialogue) {
    var su = new SpeechSynthesisUtterance();
    su.lang = "en";
    su.text = dialogue;
    speechSynthesis.speak(su);
}

function fetch_result(input)
{
  $.ajax({
    type:"POST",
    url:"/",
    data: $('form').serialize(),
    success: function(response) {
      console.log(response);
      $(".row").empty();
      
        speak(response[0]);
        $(".row").append('<div class="col-sm-12">');
        var res = response[1];
        res.forEach(function(data) {

          var html = '<div class="showing-colleges no-filter-sticky college-details"><div class="media"><div class="media-left showing-colleges-img-big image-inner"><a href="#"><img class="media-object" src="/static/css/images/listing-img.jpg" alt="showing colleges"></a></div><div class="media-body media-detail"><h4 class="media-heading">'+data[0]+'</h4><p class="b-bottom"><span>Established: <strong>'+data[2]+'</strong> </span><span class="right-filter mob-space-r">Location: <strong>'+data[7]+','+data[8]+'</strong></span><span class="right-filter mob-space-r">Affiliation: <strong>'+data[1]+'</strong></span></p><p><span class="college-facilities"><strong>College Facilities: </strong>'+data[3]+'</span></p></div><p class="b-bottom"><span>Course: <strong>'+data[9]+'</strong> </span><span class="right-filter mob-space-r">Eligiblity: <strong>'+data[15]+'</strong></span><span class="right-filter mob-space-r">Duration: <strong>'+data[12]+'</strong></span><span class="right-filter mob-space-r">Fee: <strong>'+data[11]+'</strong></span></p><div class="clg-review"><p><strong>Review: </strong>'+data[5]+'</p></div>'

          $(".col-sm-12").append(html);
        });
      

    },
    
  });
}

function fetch_result_text(input)
{
  $.ajax({
    type:"POST",
    url:"/",
    data: $('form').serialize(),
    success: function(res) {
      console.log(res);
      $(".row").empty();
        speak(res[0]);
    },
    
  });
}
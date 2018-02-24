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
    fetch_result($('#type-input').text());
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
    success: function(data) {
      console.log(data);
    },
    
  });
}
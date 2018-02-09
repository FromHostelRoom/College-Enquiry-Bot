$(document).ready(function() {

  $('#search-popup-btn').on('click', function(){
    $('.wrap').toggleClass('active');
    $('.type-input').css('visibility','visible');
    
  });

  $('#mic-popup-btn').on('click', function(){
   
    var su = new SpeechSynthesisUtterance();
    su.lang = "en";
    su.text = "Hello! How may I help you?";
    speechSynthesis.speak(su);

    $('.wrap').toggleClass('active');
    $('.mic-search-box').css('visibility','visible');

    
        if (annyang) 
        {
          
          setTimeout(function(){ annyang.start(); }, 3000);

          annyang.addCallback('result', function(userSaid) {
          annyang.abort();
          $('.mic-input').text(userSaid[0]);
          su.text = "Please wait while we process your query.";
          speechSynthesis.speak(su);

          fetch_result(userSaid, su);

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

});


function fetch_result(input,su)
{
  $.ajax({
    type:"POST",
    url:"/",
    data: $('form').serialize(),
    success: function(data) {
      su.text = data;
      speechSynthesis.speak(su);
    },
    
  });
}
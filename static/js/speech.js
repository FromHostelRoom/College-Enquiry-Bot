
      
function startDictation() {
      recognition = new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      recognition.lang = "en-US";


      recognition.onresult = function(e) {
      for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
        document.getElementById('messageText').value
                                        = e.results[i][0].transcript;

       // recognition.stop();




         document.getElementById('button1').click();
        // recognition.start();
        }}
      };
 recognition.start();

   

      recognition.onerror = function(e) {
        recognition.stop();

      }

    }






function stopDictation() {
         
        recognition.stop();

       }
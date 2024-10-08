document.addEventListener("DOMContentLoaded", function() {
     const sentence = document.getElementById("animetion_sentence");

     setTimeout(function() {
        if(sentence) {
            sentence.classList.add('show');
        }
         
        const summaryElement = document.getElementById("summary");
        
        if(summaryElement) {
            setTimeout(function() {
                summaryElement.style.visibility = "visible";
                 typeEffect(summaryElement, 25);
            }, 500);
        }
     }, 0);

    function typeEffect(element, speed) {
        let text = element.innerHTML;
        element.innerHTML = "";
        let i = 0;

        let timer = setInterval(function() {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }
});
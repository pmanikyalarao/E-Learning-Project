let chatbotForm = document.getElementById("chatbotForm")
let messageBox = document.getElementById("userMessage")
let chatBody = document.getElementsByClassName("chat-body")[0]


console.log(chatbotForm)
console.log(messageBox)
console.log(chatBody)

//handle chat messages
chatbotForm.addEventListener('click', function(event) {
    
    // let messageBox = document.getElementById("userMessage")
    // let chatBody = document.getElementsByClassName("chat-body")[0]

    console.log("Clicked")
    // console.log(messageBox)
    // console.log(chatBody)

    event.preventDefault(); //prevent the default form submission
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/commonChatBotPage', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    
    let userMessage = messageBox.value;
    
    // appending the user message to the chat body
    chatBody.innerHTML += '<div class="message user">'+
                          '<div class="text">'+userMessage+'</div>'+
                              '<span class="uicon">You</span>'+
                          '</div>';
    
    // clear the input box
    messageBox.value = '';
    
    // add a loading animation for the bot response
    let loadingMessage = document.createElement('div');
    loadingMessage.classList.add('bot', 'message');
    loadingMessage.innerHTML = '<span class="bicon">🤖</span>'+
                            '<div class="loading-dots">'+
                                   '<span></span><span></span><span></span>'+
                            '</div>';
    chatBody.appendChild(loadingMessage);

    // scroll to the bottom of the chat body
    chatBody.scrollTop = chatBody.scrollHeight;

    
    xhr.onload = function() {
        if (xhr.status == 200) {
            // Update the page with the received data
            var response = xhr.responseText;

                // Remove the loading message
                chatBody.removeChild(loadingMessage);

            chatBody.innerHTML += '<div class="message bot">'+
                                    '<span class="bicon">🤖</span>'+
                                    '<div class="text">'+response+'</div>'+
                                '</div>';
            
            // Scroll to the bottom of the chat body
            chatBody.scrollTop = chatBody.scrollHeight;
        }
        else{
            // Remove the loading message
            chatBody.removeChild(loadingMessage);
        
            chatBody.innerHTML += '<div class="bot message">'+
                    '<span class="bicon">🤖</span>'+
                    '<div class="text">error</div>'+
                '</div>';
            }
    };

    // Send the request with the user message
    xhr.send(JSON.stringify({ message: userMessage }));
});
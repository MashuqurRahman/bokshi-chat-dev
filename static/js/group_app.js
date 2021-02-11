// static/js/group_app
let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

// Fetch all users from database through api
function updateUserList() {
    $.getJSON('api/v1/user/', function (data) {
        // userList.children('.user').remove();[mashuq commented this]

        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');//[the previous selected active username er front end er active class remove hobe]
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.text);
        });
    });
}

function updateGroupList(){
    $.getJSON('api/v1/groups/', function (data) {
        // userList.children('.user').remove();[mashuq commented this]

        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item group">${data[i]['name']}</a>`;
            $(userItem).appendTo('#group-list');
            console.log(userItem);
        }
        // $('.user').click(function () {
        //     userList.children('.active').removeClass('active');//[the previous selected active username er front end er active class remove hobe]
        //     let selected = event.target;
        //     $(selected).addClass('active');
        //     setCurrentRecipient(selected.text);
        // });
    });
}

function updateGroupList(){
    $.getJSON('http://localhost:8000/api/v1/groups/', function (data) {
        // userList.children('.user').remove();[mashuq commented this]

        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item group">${data[i]['name']}</a>`;
            $(userItem).appendTo('#group-list');
            console.log(userItem);
        }
        // $('.user').click(function () {
        //     userList.children('.active').removeClass('active');//[the previous selected active username er front end er active class remove hobe]
        //     let selected = event.target;
        //     $(selected).addClass('active');
        //     setCurrentRecipient(selected.text);
        // });
    });
}
// Receive one message and append it to message list
function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.timestamp);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

// Fetch last 20 conversatio from the database
function getConversation(recipient) {
    $.getJSON(`/api/v1/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

// Retrive message by message id and add to messageList
// Access message id from websocket
function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`/api/v1/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

// Send message to messages api
function sendMessage(recipient, body) {
    $.post('/api/v1/message/', {
        recipient: recipient,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

// set clicked user as currentRecipient
// get all conversation of currentRecipient or currentUser
function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


// Enable input button
function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

// Disable input button
function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    // updateUserList();
    updateGroupList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var socket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/group?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    // Receive message from websocket
    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});

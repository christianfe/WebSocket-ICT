
const webSocket = new WebSocket("ws://localhost:9001");


webSocket.onmessage = (event) => {
	let d = JSON.parse(event.data)
	if (d["hi"] != undefined) {
		id = d["hi"]
		updatevals(d["hi"], d["connected"])
	} else if (d["join"] != undefined) {
		updatevals(id, d["connected"])
		addMessage("server", d["join"] + " join the chat", false)
	} else if (d["left"] != undefined) {
		updatevals(id, d["connected"])
		addMessage("server", d["left"] + " left the chat", false)
	} else if (d["sender"] != undefined) {
		addMessage(d["sender"], d["msg"], d["admin"] == "1")
	}
};

function updatevals(id, conns) {
	$("#id").html("Your id: " + id)
	$("#online").html(conns + " online")
}


$("#messageForm").submit(function (e) {
	let msg = $("#msg").val()
	$("#msg").val("")
	webSocket.send("{\"admin\": \"0\", \"action\": \"msg\", \"msg\": \"" + msg + "\"}")
	e.preventDefault();
});


function addMessage(sender, msg, admin) {
	let adminCode = ""
	if (admin)
		adminCode = "&#9733;"

	if (sender == "server")
		$("#msgContainer").prepend("<div class=\"card bg-warning mb-3\"> <div class=\"card-body text-center\"> <p class=\"card-text\">" + msg + "</p> </div> </div> ")
	else if (sender == id)
		$("#msgContainer").prepend("<div class=\"card bg-primary mb-3\"> <div class=\"card-header\">You " + adminCode + "</div> <div class=\"card-body\"> <p class=\"card-text\">" + msg + "</p> </div> </div>")
	else
		$("#msgContainer").prepend("<div class=\"card text-white bg-dark mb-3\">	<div class=\"card-header text-end\">" + sender + adminCode + "</div> <div class=\"text-end card-body\"> <p class=\"card-text\">" + msg + "</p> </div> </div>")
}
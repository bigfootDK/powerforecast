document.getElementById("body").onload = function() {
	document.getElementById("update_button").style.visibility = "hidden";
};


function add_one(){
    document.getElementById("slider").value = Number(document.getElementById("slider").value) + 1;
}

function subtract_one(){
    document.getElementById("slider").value = Number(document.getElementById("slider").value) - 1;
}

function show_value(x){
	document.getElementById("update_button").style.visibility = "visible";
    document.getElementById("slider_value").innerHTML=x;
}
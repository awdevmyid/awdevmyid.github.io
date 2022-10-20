function run() {
 var html = document.getElementById("html");
 var css = document.getElementById("css");
 var js = document.getElementById("js");
 var output = document.getElementById("output")
 
 .contentWindow.document;
 
 document.body.onkeyup = function() {
 output.open();
 output.writeln(
 html.value +
 "<style>" +
 css.value +
 "</style>" +
 "<script>" +
 js.value +
 "</script>"
 );
 output.close();
 };
 }
 
 run();

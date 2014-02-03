(function(window, undefined) {
var dictionary = {
"8b620454-b996-4c10-aab3-81553933e8a7": "Dad",
"95adc887-3e85-4566-95d6-d7b6077c8c85": "Login",
"8a638ee1-d936-47c6-b4d7-1fa17ca84294": "Patches",
"67034e1e-598f-47cc-993b-694b231d4a83": "Mom",
"70bb128e-46f2-4626-8d71-4815e1caf146": "Loading screen",
"1e8a452c-0c3e-434b-9a69-9f88c989dab1": "Template 1"
};

var uriRE = /^(\/#)?(screens|templates|masters)\/(.*)(\.html)?/;
window.lookUpURL = function(fragment) {
var matches = uriRE.exec(fragment || "") || [],
folder = matches[2] || "",
canvas = matches[3] || "",
name, url;
if(dictionary.hasOwnProperty(canvas)) { /* search by name */
url = folder + "/" + canvas;
}
return url;
};

window.lookUpName = function(fragment) {
var matches = uriRE.exec(fragment || "") || [],
folder = matches[2] || "",
canvas = matches[3] || "",
name, canvasName;
if(dictionary.hasOwnProperty(canvas)) { /* search by name */
canvasName = dictionary[canvas];
}
return canvasName;
};
})(window);
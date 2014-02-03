jQuery("#simulation")
.on("click", ".s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 .click", function(event, data) {
var jEvent, jFirer, cases;
if(data === undefined) { data = event; }
jEvent = jimEvent(event);
jFirer = jEvent.getEventFirer();
if(jFirer.is("#s-Label_62")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"target": "screens/8b620454-b996-4c10-aab3-81553933e8a7",
"transition": "slideleft"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
} else if(jFirer.is("#s-Image_map_33")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"target": "screens/8b620454-b996-4c10-aab3-81553933e8a7",
"transition": "slideleft"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
} else if(jFirer.is("#s-Label_4")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"isbackward": true,
"transition": "slideright"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
} else if(jFirer.is("#s-Label_66")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"target": "screens/67034e1e-598f-47cc-993b-694b231d4a83",
"transition": "slideleft"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
} else if(jFirer.is("#s-Image_map_40")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"target": "screens/67034e1e-598f-47cc-993b-694b231d4a83",
"transition": "slideleft"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
} else if(jFirer.is("#s-Label_3")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"target": "screens/95adc887-3e85-4566-95d6-d7b6077c8c85"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
}
})
.on("focusin", ".s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 .focusin", function(event, data) {
var jEvent, jFirer, cases;
if(data === undefined) { data = event; }
jEvent = jimEvent(event);
jFirer = jEvent.getEventFirer();
if(jFirer.is("#s-Input_6")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimChangeStyle",
"parameter": [ {
"#s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 #s-Input_6 .valign": {
"attributes": {
"vertical-align": "middle",
"line-height": "11pt"
}
}
},{
"#s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 #s-Input_6 input": {
"attributes": {
"color": "#C0C0C0",
"text-align": "left",
"text-decoration": "none",
"font-family": "Roboto-Regular",
"font-size": "11pt"
}
}
} ]
},
{
"action": "jimMove",
"parameter": {
"target": "#s-Image_44",
"type": "movebyoffset",
"containment": true,
"top": 0,
"left": -114
}
},
{
"action": "jimSetValue",
"parameter": {
"target": "#s-Input_6",
"value": ""
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
}
})
.on("focusout", ".s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 .focusout", function(event, data) {
var jEvent, jFirer, cases;
if(data === undefined) { data = event; }
jEvent = jimEvent(event);
jFirer = jEvent.getEventFirer();
if(jFirer.is("#s-Input_6")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimChangeStyle",
"parameter": [ {
"#s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 #s-Input_6 .valign": {
"attributes": {
"vertical-align": "middle",
"line-height": "11pt"
}
}
},{
"#s-8a638ee1-d936-47c6-b4d7-1fa17ca84294 #s-Input_6 input": {
"attributes": {
"color": "#C0C0C0",
"text-align": "center",
"text-decoration": "none",
"font-family": "Roboto-Regular",
"font-size": "11pt"
}
}
} ]
},
{
"action": "jimMove",
"parameter": {
"target": "#s-Image_44",
"type": "movebyoffset",
"containment": true,
"top": 0,
"left": 114
}
},
{
"action": "jimSetValue",
"parameter": {
"target": "#s-Input_6",
"value": "Search"
}
}
]
}
]
}
];
event.data = data;
jEvent.launchCases(cases);
}
});
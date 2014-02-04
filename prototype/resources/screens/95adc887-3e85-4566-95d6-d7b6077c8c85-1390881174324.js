jQuery("#simulation")
.on("click", ".s-95adc887-3e85-4566-95d6-d7b6077c8c85 .click", function(event, data) {
var jEvent, jFirer, cases;
if(data === undefined) { data = event; }
jEvent = jimEvent(event);
jFirer = jEvent.getEventFirer();
if(jFirer.is("#s-Label_1")) {
cases = [
{
"blocks": [
{
"condition": {
"action": "jimOr",
"parameter": [ {
"action": "jimNotEquals",
"parameter": [ {
"target": "#s-Input_2"
},"sam" ]
},{
"action": "jimNotEquals",
"parameter": [ {
"target": "#s-Input_3"
},"sam" ]
} ]
},
"actions": [
{
"action": "jimShow",
"parameter": {
"target": "#s-Label_1",
"effect": {
"type": "shake",
"duration": 100
}
}
}
]
},
{
"actions": [
{
"action": "jimNavigation",
"parameter": {
"target": "screens/8a638ee1-d936-47c6-b4d7-1fa17ca84294",
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
}
});
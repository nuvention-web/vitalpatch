jQuery("#simulation")
.on("pageload", ".s-70bb128e-46f2-4626-8d71-4815e1caf146 .pageload", function(event, data) {
var jEvent, jFirer, cases;
if(data === undefined) { data = event; }
jEvent = jimEvent(event);
jFirer = jEvent.getEventFirer();
if(jFirer.is("#s-70bb128e-46f2-4626-8d71-4815e1caf146")) {
cases = [
{
"blocks": [
{
"actions": [
{
"action": "jimPause",
"parameter": {
"pause": 1000
}
},
{
"action": "jimNavigation",
"parameter": {
"target": "screens/95adc887-3e85-4566-95d6-d7b6077c8c85",
"transition": "fade"
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
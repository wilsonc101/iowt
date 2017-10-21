$('#thingModal').on('show.bs.modal', function(e) {
  var deviceId = e.relatedTarget.dataset.deviceid;
  var deviceName = e.relatedTarget.dataset.devicename;
  var deviceLocation = e.relatedTarget.dataset.devicelocation;
  var deviceNum = e.relatedTarget.dataset.devicenum;


  $(e.currentTarget).find('input[name="deviceId"]').val(deviceId);
  $(e.currentTarget).find('input[name="deviceName"]').val(deviceName);
  $(e.currentTarget).find('input[name="deviceLocation"]').val(deviceLocation);

});

function save_device_data(button) {
  var deviceId = $("#deviceId").val();
  var deviceLocation = $("#deviceLocation").val();
  var deviceName = $("#deviceName").val();
  var apiUrl = $(button).data("apiurl");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"device-id":deviceId,
                             "device-name":deviceName, 
                             "device-location":deviceLocation, 
                             "action":"update"}));

  $('#thingModal').modal('hide');
  location.reload();

};

$('#eventModal').on('show.bs.modal', function(e) {
  var creatureWeight = e.relatedTarget.dataset.creatureweight;
  var foodLevel = e.relatedTarget.dataset.foodlevel;
  var waterLevel = e.relatedTarget.dataset.waterlevel;

  $(e.currentTarget).find('input[name="creatureWeight"]').val(creatureWeight);

  var foodBar = document.getElementById("progbar-food");
  foodBar.style.width = foodLevel.concat("%");

  var waterBar = document.getElementById("progbar-water");
  waterBar.style.width = waterLevel.concat("%");
});

function event_delete(button) {
  var eventId = $(button).data("eventid");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, true);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"eventid":eventId, "action":"delete"}));
  location.reload();

};

function device_delete(button) {
  var deviceId = $(button).data("deviceid");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, true);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"deviceid":deviceId, "action":"delete"}));
  location.reload();

};

function device_disable(button) {
  var deviceId = $(button).data("deviceid");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, true);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"deviceid":deviceId, "action":"disable"}));
  location.reload();

};

function save_user_settings() {
  var newPassword = $("#inputPassword").val();
  var newEmail = $("#inputEmail").val();

  console.log(newPassword);
  console.log("here");

//  var xhttp = new XMLHttpRequest();
//  xhttp.open("POST", apiUrl, true);
// xhttp.setRequestHeader('Content-type', 'application/json');
//  xhttp.send(JSON.stringify({"newpassword":newPassword, "newEmail":newEmail, "action":"update"}));
//  location.reload();

};



$('#imageModal').on('show.bs.modal', function(e) {
  var image = e.relatedTarget.dataset.image;

  var eventImage = document.getElementById("full-image");
  eventImage.alt = image;
  eventImage.src = "https://robotika.co.uk/robotika.png";
});


$('#thingModal').on('show.bs.modal', function(e) {
  var deviceId = e.relatedTarget.dataset.deviceid;
  var deviceName = e.relatedTarget.dataset.devicename;
  var deviceLocation = e.relatedTarget.dataset.devicelocation;
  var deviceNum = e.relatedTarget.dataset.devicenum;

  $(e.currentTarget).find('input[name="deviceId"]').val(deviceId);
  $(e.currentTarget).find('input[name="deviceName"]').val(deviceName);
  $(e.currentTarget).find('input[name="deviceLocation"]').val(deviceLocation);

});

$('#thingModal').on('hidden.bs.modal', function() {
    $("#thingForm").validate().resetForm();
});


$('#adminthingModal').on('show.bs.modal', function(e) {
  var deviceId = e.relatedTarget.dataset.deviceid;
  var deviceOwner = e.relatedTarget.dataset.deviceowner;

  $(e.currentTarget).find('input[name="deviceId"]').val(deviceId);
  $(e.currentTarget).find('input[name="deviceOwner"]').val(deviceOwner);

});

function save_device_data(button) {
  var deviceId = $("#deviceId").val();
  var deviceLocation = $("#deviceLocation").val();
  var deviceName = $("#deviceName").val();
  var apiUrl = $(button).data("apiurl");

  var data_reg = /^[-_a-zA-Z0-9]+(\s+[-_a-zA-Z0-9]+)*$/;

  if (deviceName.length >= 1 && data_reg.test(deviceName) && deviceLocation.length >= 1 && data_reg.test(deviceLocation)) {

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

};


function admin_save_device_data(button) {
  var deviceId = $("#deviceId").val();
  var deviceOwner = $("#deviceOwner").val();
  var apiUrl = $(button).data("apiurl");

  var user_reg = /^([A-z0-9]{1,})$/;

  if (deviceOwner.length >= 4 && user_reg.test(deviceOwner)) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", apiUrl, false);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify({"device-id":deviceId,
                               "device-owner":deviceOwner, 
                               "action":"update"}));

    $('#thingModal').modal('hide');
    location.reload();
  };
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
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"eventid":eventId, "action":"delete"}));
  location.reload();

};

function device_delete(button) {
  var deviceId = $(button).data("deviceid");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"device-id":deviceId, "action":"delete"}));
  location.reload();

};

function device_disable(button) {
  var deviceId = $(button).data("deviceid");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"device-id":deviceId, "action":"disable"}));
  location.reload();

};

function device_enable(button) {
  var deviceId = $(button).data("deviceid");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"device-id":deviceId, "action":"enable"}));
  location.reload();

};

function user_enable(button) {
  var userName = $(button).data("username");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"username":userName, "action":"enableuser"}));
  location.reload();

};

function user_disable(button) {
  var userName = $(button).data("username");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"username":userName, "action":"disableuser"}));
  location.reload();

};

function user_delete(button) {
  var userName = $(button).data("username");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"username":userName, "action":"deleteuser"}));
  location.reload();

};

function save_user_settings() {
  var newEmail = $("#inputEmail").val();

  console.log(newEmail);
};

function reset_password(button) {
  var username = $(button).data("username");
  var apiUrl = $(button).data("url");

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", apiUrl, false);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.send(JSON.stringify({"username":username, "action":"resetpassword"}));

  document.cookie = 'access=;path=/;domain=.iowt.robotika.co.uk;expires=Thu, 01 Jan 1970 00:00:01 GMT;';

  $(button).prop("disabled",true);
  $("#passwordresetModal").modal();

};

$('#imageModal').on('show.bs.modal', function(e) {
  var image = e.relatedTarget.dataset.image;
  var imageUrl = e.relatedTarget.dataset.imageurl;

  var eventImage = document.getElementById("full-image");
  eventImage.alt = image;

  var xhttp = new XMLHttpRequest();

  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      eventImage.src = xhttp.responseText;
  }};

  xhttp.open("GET", imageUrl, false);
  xhttp.send();

});

$(function () {
  $('[data-toggle="popover"]').popover()
})

$("#passwordresetModal").on("hidden.bs.modal", function () {
  location.reload();
});

function signout() {
  document.cookie = 'access=;path=/;domain=.iowt.robotika.co.uk;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  location.reload();
};


function new_user_data(button) {
  var userName = $("#userName").val();
  var userEmail = $("#userEmail").val();
  var apiUrl = $(button).data("apiurl");

  var email_reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  var user_reg = /^([A-z0-9]{1,})$/;

  if (email_reg.test(userEmail) == true && userName.length >= 4 && user_reg.test(userName)) {
    console.log(userName);
    console.log(userEmail);

    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", apiUrl, false);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify({"user-username":userName,
                               "user-email":userEmail,
                               "action":"create"}));

    $('#newuserModal').modal('hide');
  };
};



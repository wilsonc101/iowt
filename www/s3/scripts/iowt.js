$('#myModal').on('show.bs.modal', function(e) {
  var deviceId = e.relatedTarget.dataset.deviceid;
  var deviceName = e.relatedTarget.dataset.devicename;
  var deviceLocation = e.relatedTarget.dataset.devicelocation;
  var deviceNum = e.relatedTarget.dataset.devicenum;


  $(e.currentTarget).find('input[name="deviceId"]').val(deviceId);
  $(e.currentTarget).find('input[name="deviceName"]').val(deviceName);
  $(e.currentTarget).find('input[name="deviceLocation"]').val(deviceLocation);

});

function save_device_data() {
  $select_value = $("#deviceLocation").val();
  console.log($select_value);
  $('#myModal').modal('hide');
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




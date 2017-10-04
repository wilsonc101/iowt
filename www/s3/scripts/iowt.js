$('#myModal').on('show.bs.modal', function(e) {
  var deviceId = e.relatedTarget.dataset.deviceid;
  var deviceName = e.relatedTarget.dataset.devicename;
  var deviceLocation = e.relatedTarget.dataset.devicelocation;


  $(e.currentTarget).find('input[name="deviceId"]').val(deviceId);
  $(e.currentTarget).find('input[name="deviceName"]').val(deviceName);
  $(e.currentTarget).find('input[name="deviceLocation"]').val(deviceLocation);
});

function save_device_data() {
  $select_value = $("#deviceLocation").val();
  console.log($select_value);
  $('#myModal').modal('hide');
};



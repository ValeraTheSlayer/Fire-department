//Set date range 
// console.log(moment().format('YYYY-MM-DD'));
$('#start_date').val(moment().subtract(30, 'days').format('YYYY-MM-DD'));
//$('#end_date').val(moment().format('YYYY-MM-DD'));
//$('#end_time').val(moment().format('HH:MM'));
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
    };
function setStartDateTime() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    $('#end_date').val(moment().format(yyyy+'-'+mm+'-'+dd));
    var h = today.getHours();
    var m = today.getMinutes();
    m = checkTime(m);
    $('#end_time').val(h + ":" + m);
    //console.log(m);
    var t = setTimeout(setStartDateTime, 1000);
};
setStartDateTime();
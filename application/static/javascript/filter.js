// Filter start here
var filterVar = {'page':1,'matched':'','camera':'', 'start_date':'','start_time':'','end_date':'','end_time':''}
//Radio button all matched not matched

$('input[type=radio][name=matched]').change(function(){
  filterVar['matched'] = this.value;
  set_table_content(filterVar);
});
// Select camera 
$('#camera_select').change(function(){
    filterVar['camera'] = this.value;
    set_table_content(filterVar);
});
//Start Date
//End Date
$('.insert_date').change(function(){
  var start_date = $('#start_date').val();
  var start_time = $('#start_time').val();
  var end_date = $('#end_date').val();
  var end_time = $('#end_time').val();
  filterVar['start_date'] = start_date;
  filterVar['start_time'] = start_time;
  filterVar['end_date'] = end_date;
  filterVar['end_time'] = end_time;
  set_table_content(filterVar);
});
/////////////////////////////////////////
// Pagination ///////////////////////////
/////////////////////////////////////////
$('#previous_page').click(function(){
    var pageNumber = $('#page_number').text();
    if(pageNumber!=1){
      pageNumber=parseInt(pageNumber)-1;
      $('#page_number').text(pageNumber);
      filterVar['page'] = pageNumber;
      set_table_content(filterVar);
    };
  });
  $('#next_page').click(function(){
    var pageNumber = $('#page_number').text();
    pageNumber=parseInt(pageNumber)+1;
    $('#page_number').text(pageNumber);
    filterVar['page'] = pageNumber;
    set_table_content(filterVar);
  });
  ////////////////////////////////////
  // Filter RESET
  ////////////////////////////////////
  $('#filter_reset').click(function(){
    
    $('#matched_all').prop('checked',true);
    $('#camera_select').val('');
    $('#start_date').val(moment().subtract(30, 'days').format('YYYY-MM-DD'));
    $('#start_time').val('00:00');
    $('#end_date').val(moment().format('YYYY-MM-DD'));
    $('#end_time').val(moment().format('HH:MM'));

    filterVar = {'page':1,'matched':'','camera':'', 'start_date':'','start_time':'','end_date':'','end_time':''}
    set_table_content(filterVar);
  });
// Ajax to DRF auto refresh table content
function set_table_content(filterVar) {
        var urlFilter = $.param( filterVar );
        $.ajax({
            method: "GET",
            url: '/api/croplist/?'+urlFilter,
            success: function(data) {
                $("tbody").empty();
                $.each(data, function (key, value) {
                    var unique_id = value.unique_id;
                    var red_id = value.red_id;
                    var insert_date = value.insert_date;
                    var camera = value.camera;
                    var camera_name = value.camera_name;
                    var crop_id = value.crop_id;
                    var file_id = camera+"_"+unique_id+"_"+crop_id;
                    if (red_id == null){
                        $("tbody").append(
                            "<tr class='text-center'><td class='align-middle'><img id='"+ value.id +"' src='/static/crops/"+ file_id +".jpg' class='main_croplist_image' alt='crops'></td><td class='align-middle'><p>-------</p></td><td class='align-middle'><p>" + insert_date.replace('T', ' ') + "</p></td><td class='align-middle'><p>" + camera_name + "</p></td></tr>"
                         )
                    } else {
                        $("tbody").append(
                            "<tr class='text-center'><td class='align-middle'><img id='"+ value.id +"' src='/static/crops/"+ file_id +".jpg' class='main_croplist_image' alt='crops'></td><td class='align-middle'><img class='main_croplist_image' src='/static/black_list/"+ red_id+".jpg' alt='black_list'></td><td class='align-middle'><p>" + insert_date.replace('T', ' ') + "</p></td><td class='align-middle'><p>" + camera_name + "</p></td></tr>"
                         )
                    };

                })
            },
            error: function(data) {
                console.log("error")
            }
        })
    };

set_table_content(filterVar);   
//setInterval( function() {set_table_content(filterVar)} , 1000);

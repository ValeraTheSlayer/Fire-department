 $(function() {

    $( '#table' ).on( 'click', 'tr', function () {
       var unique_image_id = $(this).children('td').children('img').attr('id');
       location.href = "/main_page/detail_view/" + unique_image_id
    });

    $('input[name="datetimes"]').daterangepicker({
      timePicker: true,
      timePicker24Hour: true,
      startDate: moment().subtract(10, 'days'),
      endDate: moment(),
      locale: {
        format: 'DD/MM/YY HH:MM',
        "applyLabel": "Ввод",
        "cancelLabel": "Отмена",
        "fromLabel": "От",
        "toLabel": "До",
        "daysOfWeek": [
             "Вс",
             "Пн",
             "Вт",
             "Ср",
             "Чт",
             "Пт",
             "Сб"
         ],
         "monthNames": [
             "Январь",
             "Февраль",
             "Март",
             "Апрель",
             "Май",
             "Июнь",
             "Июль",
             "Август",
             "Cентябрь",
             "Октябрь",
             "Ноябрь",
             "Декабрь"
         ],
        "firstDay": 1

      }
    });

  });

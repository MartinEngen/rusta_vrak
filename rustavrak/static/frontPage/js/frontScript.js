/**
 * Created by Lawliet on 10/10/2016.
 */
    $(document).ready(( function() {

        $("#datepickerFinish").datepicker({
            minDate: 0
        });
        $("#datepickerStart").datepicker({
            minDate: 0,
            onSelect: function(dateText, inst){
                var date = $("#datepickerStart").datepicker('getDate');
                date.setDate(date.getDate()+1);
             $("#datepickerFinish").datepicker("option","minDate", date);
            }
        });


    }));

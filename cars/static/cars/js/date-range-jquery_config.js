/**
 * Created by Mello on 2/13/2017.
 */
/**
 * Created by Mello on 2/11/2017.
 */
$(function(){




    function FormatDate(date){
        var year = date.getFullYear();
        var month = (1 + date.getMonth()).toString();
        month = month.length > 1 ? month : '0' + month;
        var day = date.getDate().toString();
        day = day.length > 1 ? day : '0' + day;
        return day + '.' + month + '.' + year;
    }


    //var current_date = FormatDate(new Date());


    $('#date-range').dateRangePicker(
        {
            inline:true,
            container: '#date-range12-container',
            alwaysOpen:true,
            format: "DD.MM.YYYY",
            separator: ' til ',
            language: 'no',
            startOfWeek: 'monday',// or monday
            startDate: FormatDate(new Date()), // The current date, formatted.
            maxDays: 30,
            getValue: function()
            {
                if ($('#datepickerStart').val() && $('#datepickerFinish').val() )
                    return $('#datepickerStart').val() + ' til ' + $('#datepickerFinish').val();
                else
                    return '';
            },
            setValue: function(s,s1,s2)
            {
                $('#datepickerStart').val(s1);
                $('#datepickerFinish').val(s2);
                updateDetails();
            },

            beforeShowDay: function(t)
            {
                var formatted_date = FormatDate(t);
                var valid = !(booked_dates.indexOf(formatted_date) >= 0);  //disable saturday and sunday
                var _class = '';
                var _tooltip = valid ? '' : 'Opptatt';
                return [valid,_class,_tooltip];
            }
        });

});
/**
 * Created by Mello on 20.09.2016.
 */







function countDays(firstDate,secondDate){
    var startDay = new Date(firstDate);
    var endDay = new Date(secondDate);
    var a = moment([startDay.getYear(), startDay.getMonth(), startDay.getDate()]);
    var b = moment([endDay.getYear(), endDay.getMonth(), endDay.getDate()]);
    console.log(b.diff(a, 'days')+1);   // =1

    return b.diff(a, 'days');
}


function price_calculator(days, start_price){
    var final_price = 0;

    function round5(x)
    {
        return (x % 5) >= 2.5 ? parseInt(x / 5) * 5 + 5 : parseInt(x / 5) * 5;
    }

    if(days <=29){
        var discount_calculated = 1;
        var amount_of_discounts = Math.floor(days / 5);
        var discount = 0.825; //17.5% discount for each chunk

        console.log("Discounts: " + amount_of_discounts);

        for(var i =0; i<amount_of_discounts;i++){
            discount_calculated *= discount;
        }
        console.log(start_price*days*discount_calculated);
        final_price = round5(start_price*days*discount_calculated);

    }
    else{
        if(start_price == 250){
            final_price = 2500;
        }
        else{
            final_price = 2750;
        }
    }

    return final_price


}


function updateDetails(){
    var start = $('#datepickerStart').datepicker('getDate');
    var end = $('#datepickerFinish').datepicker('getDate');
    var days = 0;
    var price = 0;
    var free_length = 0;




    days = countDays(start, end);
    if (days < 0 || days > 30){

    }
    else{
        free_length = days * 50;
        price = price_calculator(days, 250);
        $("#days_booked").html("Antall dager: " + days);
        $("#total_price").html("Total pris: " + price);
        $("#days_booked").html("Antall dager: " + days);
    }

}



$('#datepickerStart').datepicker().on("input change", function (e) {
    updateDetails();
});


$('#datepickerFinish').datepicker().on("input change", function (e) {
    updateDetails();
});

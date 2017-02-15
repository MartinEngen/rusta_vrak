/**
 * Created by Mello on 2/13/2017.
 */




function countDays(firstDate,secondDate){
    var startDay = new Date(firstDate);
    var endDay = new Date(secondDate);
    var millisecondsPerDay = 1000 * 60 * 60 * 24;

    var millisBetween = startDay.getTime() - endDay.getTime();
    var days = millisBetween / millisecondsPerDay;
    // Round down.
    alert( Math.floor(days));
}





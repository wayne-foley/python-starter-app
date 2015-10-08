
var vcap = "{'foo':'bar'}"//@Html.Raw(ViewBag.Json);
var services = ["filesystem-1.0", "harbor-1.0", "memcached-1.4", "mongodb-2.4", "mysql-5.5", "postgresql-9.1", "rabbitmq3-3.1", "mssql2014"];

$(document).ready(function() {

    $(".collapsediv").hide();
    $.each(services, function( i, v ) {
        var escaped_id = v.replace( /(:|\.|\[|\]|,)/g, "\\$1" );
        if(vcap[v]){
            $("#buttons").append("<button id='"+escaped_id+"' class='btn btn-success togglebtn' type='button'>"+v+"</button>");
            $("#"+escaped_id+"_div").find("div.off").hide();
            $("#"+escaped_id+"_div").find("div.on").append("<pre>"+JSON.stringify((vcap[v])[0],null, "\t")+"</pre>");
        }
        else{
            $("#buttons").append("<button id='"+escaped_id+"' class='btn btn-default togglebtn' type='button'>"+v+"</button>");
            $("#"+escaped_id+"_div").find("div.on").hide();
        }
    });

    $('.togglebtn').bind('click', function () {
        $(".collapsediv").hide();
        var target_id = this.id;
        $("#" + target_id + "_div").slideDown();

    });
});
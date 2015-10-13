
var vcap = "";


var services = ["filesystem", "harbor", "memcached", "mongodb", "mysql", "postgresql", "rabbitmq3", "mssql2014"];
var serviceEnabled = [0,0,0,0,0,0,0,0];


$(document).ready(function() {
		
	$(".nav-tabs a").click(function(){
        $(this).tab('show');
    });
	
	$.get( "/vcap_services", function( data ) {
		var obj = $.parseJSON(data);
		
		
		services.forEach(function(value, index, array) {
			if(obj[value] != null) {
				
				$("#als-service-buttons").append("<button id='"+value+"' class='btn btn-success togglebtn' type='button'>"+value+"</button>");
	            $("#"+value+"_div").find("div.off").hide();
	            $("#"+value+"_div").find("div.on").append("<pre>"+JSON.stringify(obj[value][0],null, "\t")+"</pre>");
		            
				console.log(value + ' found');
				serviceObjs = obj[value];
				
				for ( i = 0; i < serviceObjs.length; i++) {
					serviceEnabled[index] = 1;
					label = serviceObjs[i]['label'];
					console.log(label);
					name = serviceObjs[i]['name'];
					console.log(name);
					creds = serviceObjs[i]['credentials'];
				}
				
			}
			else {
				console.log(value + " not found");
				$("#als-service-buttons").append("<button id='"+value+"' class='btn btn-default togglebtn' type='button'>"+value+"</button>");
	            $("#"+value+"_div").find("div.on").hide();
			}
		});

		// check for user defined services
		$("#found_userdefined_services").hide();
		
		if(obj['user-provided'] != null) {
			$("#found_userdefined_services").append("<pre>"+JSON.stringify(obj['user-provided'],null, "\t")+"</pre>")
			$("#found_userdefined_services").show();
		}
		
		//collapsed_div behavior
  		$('.togglebtn').bind('click', function () {
        	$(".collapsediv").hide();
        	var target_id = this.id;
        	$("#" + target_id + "_div").slideDown();

    	});

	});
    $(".collapsediv").hide();
    /*
    $.each(services, function( i, v ) {
        //var escaped_id = v.replace( /(:|\.|\[|\]|,)/g, "\\$1" );
        var escaped_id = v;
        if(serviceEnabled[i]){
            $("#buttons").append("<button id='"+escaped_id+"' class='btn btn-success togglebtn' type='button'>"+v+"</button>");
            $("#"+escaped_id+"_div").find("div.off").hide();
            $("#"+escaped_id+"_div").find("div.on").append("<pre>"+JSON.stringify((vcap[v])[0],null, "\t")+"</pre>");
        }
        else{
            $("#buttons").append("<button id='"+escaped_id+"' class='btn btn-default togglebtn' type='button'>"+v+"</button>");
            $("#"+escaped_id+"_div").find("div.on").hide();
        }
    });
	*/
    
  
});
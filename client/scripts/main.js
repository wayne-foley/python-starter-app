
var vcap = "";


var services = ["filesystem", "harbor", "memcached", "mongodb", "mysql", "postgresql", "rabbitmq3", "mssql2014"];
var serviceEnabled = [0,0,0,0,0,0,0,0];


$(document).ready(function() {
	$(".collapsediv").hide();
	
	$.get( "/vcap_services", function( data ) {
		if(data){
			var obj = $.parseJSON(data);
		}
		else{
			var obj = {};
		}
		services.forEach(function(value, index, array) {
			console.log(obj[value]);
			console.log(data[value]);
			if(obj && obj[value] != null) {
				
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

		 //Populate user-provided services
        if(obj['user-provided'] != null) {
            var user_provided = obj['user_provided'];
            $("#userprovided-services-howto_div").hide();

            user_provided.forEach( function(v,i) {
                upName = v['name'];
                $("#userprovided-service-buttons").append("<button id='"+upName+"' class='btn btn-success togglebtn udbtn' type='button'>"+upName+"</button>");
                $("#userprovided_divs").append("<div class='collapsediv well on' id='"+upName+"_div'></div>");
                $("#"+upName+"_div").hide();
                $("#"+upName+"_div").append("<pre>"+JSON.stringify(v,null, "\t")+"</pre>");

            });
        }

        //collapsed_div behavior for standard services
  		$('.togglebtn').bind('click', function () {
        	$(".collapsediv").hide();
        	var target_id = this.id;
        	$("#" + target_id + "_div").slideDown();

    	});

		});

	 
});
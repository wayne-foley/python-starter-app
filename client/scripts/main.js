
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
		
		
		if(obj['user-provided'] != null) {
			
			$("#userprovided-service-buttons").append("<button id='userprovided-services-howto' class='btn btn-default togglebtn' type='button'>user-provided services how-to</button>");
			
			var userprovided_brokers = obj['user-provided']
			userprovided_brokers.forEach( function(v,i) {
				upName = v['name'];
				$("#userprovided-service-buttons").append("<button id='"+upName+"' class='btn btn-success togglebtn udbtn' type='button'>"+upName+"</button>");
				$("#userprovided_divs").append("<div class='collapsediv well on' id='"+upName+"_div'></div>");
				$("#"+upName+"_div").hide();
				$("#"+upName+"_div").append("<pre>"+JSON.stringify(v,null, "\t")+"</pre>");
				
			}); 
			
			
		}
		
		$("#userprovided_testform").hide();
		//collapsed_div behavior for standard services
  		$('.togglebtn').bind('click', function () {
  			$("#userprovided_testform").hide();
        	$(".collapsediv").hide();
        	var target_id = this.id;
        	$("#" + target_id + "_div").slideDown();

    	});

		//collapsed_div behavior for user provided services
  		$('.udbtn').bind('click', function () {
        	
        	$("#userprovided_testform").show();	

    	});



	});
    $(".collapsediv").hide();
    $("#userprovided-services-howto_div").show();
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
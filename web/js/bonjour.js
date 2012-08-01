    var tab_map = {
    	0: "devices",
    	1: "statistics",
    };
    
    $(function() {
    
    $("#tabs").tabs({
	    ajaxOptions: {
		    error: function(xhr, status, index, anchor) {
			    $(anchor.hash).html("Error loading tab.");
		    }
	    }
    });

	var selected = null;

	$("#tabs").bind("tabsload", function(event, ui) {
		// Stop previously selected tab
		if (selected != null) {
			var func = window[tab_map[selected] + "_stop"];
			func();
		}

		// Init selected tab
		var new_selected = $("#tabs").tabs("option", "selected");
		var func = window[tab_map[new_selected] + "_init"];
		selected = new_selected;
		//func();
	});

	$("#about").dialog({ autoOpen: false });
	$("#support").dialog({ autoOpen: false });

	$( "#accordion" ).accordion();

    });
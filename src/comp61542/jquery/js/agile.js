/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
    $(window).scroll(function() {
        if ($(this).scrollTop() > 200){
            $("#menu").addClass("fixnav");
        }
        else  if ($(this).scrollTop() < 200){
            $("#menu").removeClass("fixnav");
        }
    });
    
    $(document).ready(function(){
		$("#authorBarButton").click(function () {
			$("#year-suboptions,#statistics-suboptions").hide();
			$("#author-suboptions").slideDown(200);
			
			$("#authorBarButton").css("background-color","#4E0275");
			$("#statisticsBarButton,#yearBarButton").css("background-color","transparent");
			
			$("#authorBarButton h3").css("color","#fff");
			$("#statisticsBarButton h3,yearBarButton h3").css("color","#000000");
        });
		
		$("#yearBarButton").click(function () {
			$("#author-suboptions,#statistics-suboptions").hide();
			$("#year-suboptions").slideDown(200);
			
			$("#yearBarButton").css("background-color","#4E0275");
			$("#statisticsBarButton,#authorBarButton").css("background-color","transparent");
			
			$("#yearBarButton h3").css("color","#fff");
			$("#statisticsBarButton h3,#authorBarButton h3").css("color","#000000");
        });
		
		$("#statisticsBarButton").click(function () {
			$("#author-suboptions,#year-suboptions").hide();
			$("#statistics-suboptions").slideDown(200);
			
			$("#statisticsBarButton").css("background-color","#4E0275");
			$("#authorBarButton,#yearBarButton").css("background-color","transparent");
			
			$("#statisticsBarButton h3").css("color","#fff");
			$("#authorBarButton h3,#yearBarButton h3").css("color","#000000");
        });
		
	});


/**
 * home.js
 */

/* ----------------------------------------------------------------------------
 * global variables
 */
var g_graph;
var g_linkForce;
var g_timer;


/* ----------------------------------------------------------------------------
 * Main Driver Code
 */
$(document).ready(function(){
	let elData = sweepELData();
	let gData = parseTimeline(elData['visdata']);
	setTravelTime(elData['yymmdd'], elData['hhmm']);
	
	drawGalaxy(gData);

	writeTimeline(elData['yymmdd'], zeroPad(elData['hhmm'], 1000));
	
	setTimeTravel();
});


/* ----------------------------------------------------------------------------
 * Controller에서 model에 심어와  EL을 이용해 임시 저장한 데이터를 Body로부터 긁어오고 삭제하는 함수.
 */
function sweepELData(){
	let yymmdd = $('#yymmdd').html(); 
	let hhmm = $('#hhmm').html();
	
	let visdata = JSON.parse($('#visData').html());
	$('#searchWord').html("");
	$('#visData').html("");
	
	return {'yymmdd':yymmdd, 'hhmm':hhmm, 'visdata':visdata};
}



/* ----------------------------------------------------------------------------
 * 현재 보고 있는 정보의 날짜와 시각을 표현 
 */
function setTravelTime(yymmdd, hhmm){
	$('#travelDay').html(yymmddFormat(yymmdd));
	$('#travelTime').html(hhmmFormat(hhmm));
}


/* ----------------------------------------------------------------------------
 * 과거 타임라인과 미래 타임라인을 표현
 */
function writeTimeline(yymmdd, hhmm){
	let parcel = {
		'yymmdd' : yymmdd,
		'hhmm' : hhmm
	}
	
	$.ajax({
        url: 'apis/getPastTimeline',
        type: 'post',
        dataType: 'json',
        data: JSON.stringify(parcel),
        contentType: 'application/json',
        success: function(data){
        	console.log("success: " + 'apis/getPastTimeline');
        	
        	let past = data.past;
        	let idx = 1;
        	for (let i = past.length-1; i >= 0; i--){
        		let selector = ".time-past " + ".travel-" + idx + " ";
        		let dateSelector = selector + ".tr-day";
        		let timeSelector = selector + ".tr-time";
        		$(dateSelector).html(yymmddFormat(""+past[i].yymmdd));
        		$(timeSelector).html(hhmmFormat(""+past[i].hhmm));
        		idx++;
        	}

        	let future = data.future;
        	for (let i = 0; i < future.length; i++){
        		let selector = ".time-future " + ".travel-" + (i+1) + " ";
        		let dateSelector = selector + ".tr-day";
        		let timeSelector = selector + ".tr-time";
        		$(dateSelector).html(yymmddFormat(""+future[i].yymmdd));
        		$(timeSelector).html(hhmmFormat(""+future[i].hhmm));
        	}
        },
        error: function(equest,status,error) {
        	console.error("fail: " + 'apis/getPastTimeline');
        }
    });
}


/* ----------------------------------------------------------------------------
 * 시간여행 기능 활성화
 */
function setTimeTravel() {
	let arrWormHole = $(".timeline ul li span").parent();
	arrWormHole.each((i, hole) => $(hole).click(function(){
		$('#warpDiv').css("display", "inherit");
		g_timer = setInterval(function(){
			let opacity = $('#warpDiv').css("opacity")
			console.log(opacity);
			if (opacity >= 0.3) {
				clearInterval(g_timer);
			} else {
				$('#warpDiv').css("opacity", parseFloat(opacity) + 0.005);
			}
		}, 10);
		let yymmdd = $(hole).find('.tr-day').html().split("/").join("");
		let hhmm = $(hole).find('.tr-time').html().split(":").join("");
		
		$(hole).addClass("warp-target");
		
		$('#warpDate').val(yymmdd);
		$('#warpTime').val(hhmm);
		$('#warp').submit();
	}));
}

/**
 * page-test.js
 */

var g_graph;
var g_linkForce;

$(document).ready(function(){
	// 최신 정보로 키워드 은하계 그리기
	initGalaxy('apis/getLastTimeline', false)
	
	// Button
	$('#btnPrev').click(function(){
		var toGoNum= Math.abs($('#posNum').val() - 2);
		pagenation(toGoNum);
	});
	
	$('#btnNext').click(function(){
		var originNum = $('#posNum').val();
		if (originNum >= 0)
			return;
		toGoNum = Math.abs(originNum);
		pagenation(toGoNum);
	});
	
	
	$('#btnGo').click(function(){
		var toGoNum = $('#toGoNum').val() - 1;
		if (toGoNum > 0)
			return;
		toGoNum = Math.abs(toGoNum);
		pagenation(toGoNum);
	});
});


function initGalaxy(){
	$.ajax({
        url: 'apis/getLastTimeline',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function(data){
        	console.log("success: " + 'apis/getLastTimeline');
        	$('#posNum').val(0);
        	let gData = parseTimeline(data);
        	drawGalaxy(gData);
        },
        error: function(equest,status,error) {
        	console.error("fail: " + 'apis/getLastTimeline');
        }
    });
}


function pagenation(toGoNum) {
	parcel = {'pos' : toGoNum};
	$.ajax({
        url: 'apis/getTimelineByPos',
        type: 'post',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(parcel),
        success: function(data){
        	console.log("success: apis/getTimelineByPos");
        	$('#posNum').val(1 - toGoNum);
        	let gData = parseTimeline(data);
        	reDrawGalaxy(gData);
        },
        error: function(equest,status,error) {
        	console.error("fail: apis/getTimelineByPos");
        }
    });
}


function parseTimeline(data){  		
	
	// visdata 가져오기
	let visdata = JSON.parse(data['visdata']);
	console.log(visdata);
	
	// 노드 정보 불러오기
	let nodes = visdata['nodes'];
	
	// 디스턴스 매트릭스 가져오고 매트릭스 형태로 변환하기
	let dmatrix = visdata['dmatrix'];
	let dlines = dmatrix.split("\n");
	dlines.pop();
	let mtrx = []
	for (j in dlines) {
		let dcols = dlines[j].split(",");
		mtrx[j] = dcols;
	}
	let len = mtrx.length;
	
	// 노드 JSON 만들기 
	let distThreshold = 0.7
	let minmax = getNodeMinMax(nodes);
	let min = minmax['min'];
	let max = minmax['max'];
	let nodesJson = [];
	let nodeVals = []
	nodes.forEach(function(d, i){
		// 충분히 강한 링크가 있는 노드들만 추가하기
		let bNodeAdd = false;
		for (j=0; j<i; j++){
			if (mtrx[i+1][j+1] <= distThreshold){
				bNodeAdd = true;
				break;
			}
		}
		if (!bNodeAdd){
			for (j=i; j<len; j++){
				if (j+2 == len)
					break;
				
				if (mtrx[j+2][i+1] <= distThreshold){
					bNodeAdd = true;
					break;
				}
			}
		}
		
		// 링크 검사가 끝난 노드만 추가
		if (bNodeAdd){
			let val = Math.max(
				Math.min(
					Math.sqrt(((d['val'] - min) / (max - min))*100)*4
					, 20
				)
				, 5
			);

			node = { 
				"id" : d['id'],
				"word" : d['word'],
				"group" : d['group'],
				"val" : val
			}
			nodesJson.push(node);
			nodeVals.push(val);
//			console.log(node);
		}
	});
	
	
	// 링크 JSON 리스트 만들기
	let linkJson = [];
	for (j = 1; j < len; j++){
		let tempLinks = []
		for (k = 1; k < j; k++){
			dist = mtrx[j][k];
			
			// 3d-force 수치에 맞게 distance 값 설정
			if (dist > distThreshold)
				continue;
			else
				dist = Math.pow(dist*5, 4);
			
				
			let forward = {
				"source" : nodes[j-1]['id'], "target" : nodes[k-1]['id'], 
				"group" : nodes[k-1]['gorup'], "dist" : dist
			};
			let reverse = {
				"source" : nodes[k-1]['id'], "target" : nodes[j-1]['id'], 
				"group" : nodes[j-1]['gorup'], "dist" : dist
			};
				
			if (nodeVals[j-1] < nodeVals[k-1]){
				tempLinks.push(forward);
			} else if (nodeVals[j-1] > nodeVals[k-1]){
				tempLinks.push(reverse)
			} else {
				tempLinks.push(forward);
				tempLinks.push(reverse);
			}
		}
		tempLinks.forEach(function(d, k){
			linkJson.push(d);
		});
	}
	
	return {nodes : nodesJson, links : linkJson};
}


function getNodeMinMax(nodes){
	let min = 100;
	let max = 0;
	nodes.forEach(function(d, i){
		min = Math.min(min, d['val']);
		max = Math.max(max, d['val']);
	});
	
	return {"min" : min, "max" : max}
}


function drawGalaxy(gData){
	g_graph = ForceGraph3D()(document.getElementById('3d-graph')) 	   
	.nodeAutoColorBy('group')      
    .nodeThreeObject(node => {
		const obj = new THREE.Mesh(
        	new THREE.SphereGeometry(10),
        	new THREE.MeshBasicMaterial(
    			{depthWrite: false, transparent: true, opacity: 0}
        	)
      	);          
		const sprite = new SpriteText(node.word);
			sprite.color = node.color;
 	    	sprite.textHeight = node.val;
 	    	obj.add(sprite);
 	    return obj;
    })
	.linkOpacity(0.08)		
	//.linkDirectionalParticles(3)
    .graphData(gData);

	//g_graph.d3Force('charge').strength(-500);

	const g_linkForce = g_graph
    	.d3Force('link')
    	.distance(link => link.dist);
}


function reDrawGalaxy(gData){
	let {nodes, links} = g_graph.graphData();
	links = links.filter(l => false);
	nodeIds = nodes.map(node => node.id);
	nodeIds.forEach((d, i) => nodes.slice(d.id, 1));
	
	g_graph.graphData(gData);
}

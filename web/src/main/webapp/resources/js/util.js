/**
 * util.js
 */

HashMap = function(){
	this.map = new Array();
}

HashMap.prototype = {
	put: function(key, value){
		this.map[key] = value;
	},
	get: function(key){
		return this.map[key];
	},
	length: function(){
		return Object.keys(this.map).length
	},
	keys: function(){
		return Object.keys(this.map)
	}
}


function zeroPad(nr, base){
  var  len = (String(base).length - String(nr).length)+1;
  return len > 0? new Array(len).join('0')+nr : nr;
}


function yymmddFormat(yymmdd){
	return "20" + yymmdd.slice(0, 2) + "/" + yymmdd.slice(2, 4) + "/" 
		+ yymmdd.slice(4, 6);
}


function hhmmFormat(hhmm){
	return zeroPad(Math.floor(parseInt(hhmm)/100), 10) + ":" 
		+ zeroPad(parseInt(hhmm)%100, 10);
}

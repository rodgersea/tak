
console.log('test1');

function Sector_Update() {
	console.log('test');
	var route_list = "{{ areas }}";
	for (i=0; i<route_list.length; i++) {
		console.log(route_list);
	}
	
	var area = document.getElementById("area_id");
	var sectors = [];
	var options = '';
	for (let i=0; i<route_list.length; i++) {
		if (route_list[i].area = area) {
			sectors.push(route_list[i].sector);
		}
	}
	console.log(sectors);
};

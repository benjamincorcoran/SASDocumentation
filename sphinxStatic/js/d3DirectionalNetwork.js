function createNetworkGraph(json){

	var width = 500,
			height = 500;


	var pJSON = JSON.parse(json)
	var nodes = []
	var links = pJSON.links

	var color = d3.scale.category10();
	
	links.forEach(function(link) {
		link.source = nodes[link.source] || 
				(nodes[link.source] = {name: link.source, 
									   lib:pJSON.nodes.find(x => x.id === link.source).lib,
									   ds:pJSON.nodes.find(x => x.id === link.source).ds});
		link.target = nodes[link.target] || 
				(nodes[link.target] = {name: link.target, 
					lib:pJSON.nodes.find(x => x.id === link.target).lib,
					ds:pJSON.nodes.find(x => x.id === link.target).ds});
		link.value = +link.value;
	});
		
	

	var force = d3.layout.force()
		.nodes(d3.values(nodes))
		.links(links)
		.size([width, height])
		.linkDistance(60)
		.charge(-300)
		.on("tick", tick)
		.start();

	var svg = d3.select("#dataNetwork").append("svg")
		.attr("width", width)
		.attr("height", height);

	// build the arrow.
	svg.append("svg:defs").selectAll("marker")
		.data(["end"])      // Different link/path types can be defined here
		.enter().append("svg:marker")    // This section adds in the arrows
		.attr("id", String)
		.attr("viewBox", "0 -5 10 10")
		.attr("refX", 15)
		.attr("refY", -1.5)
		.attr("markerWidth", 6)
		.attr("markerHeight", 6)
		.attr("orient", "auto")
		.append("svg:path")
		.attr("d", "M0,-5L10,0L0,5");

	// add the links and the arrows
	var path = svg.append("svg:g").selectAll("path")
		.data(force.links())
		.enter().append("svg:path")
	//    .attr("class", function(d) { return "link " + d.type; })
		.attr("class", "link")
		.attr("marker-end", "url(#end)");

	// define the nodes
	var node = svg.selectAll(".node")
		.data(force.nodes())
		.enter().append("g")
		.attr("class", "node")
		
		.on("click", click)
		.on("dblclick", dblclick)
		.call(force.drag);

	// add the nodes
	node.append("circle")
		.attr("r", 5)
		.style("fill",function(d) { return color(d.lib); });

	// add the text 
	node.append("text")
		.attr("x", 12)
		.attr("dy", ".35em")
		.text(function(d) { return d.ds; });

	// add the curvy lines
	function tick(e) {
		var k = 6*e.alpha
		path.attr("d", function(d) {
		
			var sourcey = d.source.y-=k;
			var targety = d.target.y+=k;
			return "M" + 
				d.source.x + "," + 
				sourcey + "L" + 
				d.target.x + "," + 
				targety;
		});

		node
			.attr("transform", function(d) {
			return "translate(" + d.x + "," + d.y + ")"; });
	}

	var legend = svg.selectAll(".legend")
    .data(color.domain())
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

	legend.append("rect")
		.attr("x", width - 18)
		.attr("width", 18)
		.attr("height", 18)
		.style("fill", color);

	legend.append("text")
		.attr("x", width - 24)
		.attr("y", 9)
		.attr("dy", ".35em")
		.style("text-anchor", "end")
		.text(function(d) { return d; });


	// action to take on mouse click
	function click() {
	//	d3.select(this).select("text").transition()
		//	.duration(750)
			//.attr("x", 22)
			//.style("fill", "steelblue")
			//.style("stroke", "lightsteelblue")
			//.style("stroke-width", ".5px")
			//.style("font", "20px sans-serif");
		//d3.select(this).select("circle").transition()
		//	.duration(750)
		//	.attr("r", 16)
		//	.style("fill", "lightsteelblue");
	}

	// action to take on mouse double click
	function dblclick() {
		//d3.select(this).select("circle").transition()
			//.duration(750)
			//.attr("r", 6)
			//.style("fill", "#ccc");
		//d3.select(this).select("text").transition()
			//.duration(750)
			//.attr("x", 12)
			//.style("stroke", "none")
			//.style("fill", "black")
			//.style("stroke", "none")
			//.style("font", "10px sans-serif");
	}
};

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}
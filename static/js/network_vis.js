var container = document.getElementById('network');

fetch('pieces/network-data').then(data => data.json())
    .then(json => {
      
      // provide the data in the vis format
      var data = {
          nodes: json.nodes,
          edges: json.edges
      };
      var options = {
        height: "100%",
      }
  
      // initialize your network!
      var network = new vis.Network(container, data, options);

      network.on("doubleClick", function(properties) {
        if(!properties.nodes.length) return;
        
        window.open(`pieces/${properties.nodes[0]}`, '_blank')
      
      })
})
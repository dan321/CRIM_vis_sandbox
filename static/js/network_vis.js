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
        label: undefined,
        arrows:  {
            to: {enabled: true, scaleFactor:10, type:'arrow'}
        }
      }
  
      // initialize your network!
      var network = new vis.Network(container, data, options);

})
let container = document.querySelector("#heatmap");
let alert = document.querySelector("#alert");
let loader = document.querySelector("#loader");
const heatmapData = JSON.parse(document.getElementById('heatmap_data').textContent);

console.log(JSON.stringify(heatmapData));


TimelinesChart()(container)
                .data(heatmapData)
                .xTickFormat(n => `measure ${+n}`)
                .timeFormat('%Q')
                .zQualitative(true)
                .leftMargin(180)
                .onSegmentClick(d => {
                    console.log(d);
                    window.open(encodeURI(d.label), '_blank');
                })
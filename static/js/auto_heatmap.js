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
                    window.open(d.url);
                })

// Get relationship data for an individual observer
function getPersonRelationshipData(person, personRelationshipArray, pieceType) {

    // Determine which part of the json is required based on the pieceType
    let jsonPart;
    if (pieceType === "Model") {
        jsonPart = "model_observation";
    } else if (pieceType === "Mass") {
        jsonPart = "derivative_observation";
    }

    // Create an array of heatmap data for a specific observer
    var personHeatmapData = [];

    personRelationshipArray.forEach(relationship => {

        let relationshipID = parseInt(relationship.id);
        let measureRanges = extractMeasureRangeFromEma(relationship[jsonPart].ema);

        let relationshipType = `${relationship.relationship_type}`;
        let additionalTypeInformation = `: ${relationship.model_observation.piece.piece_id} → ${relationship.derivative_observation.piece.piece_id}`;
        // relationshipType = relationshipType + additionalTypeInformation;


        let rangeData = measureRanges.map(rangePair => {
            return {
                timeRange: rangePair,
                val: relationshipType,
            }
        });

        personHeatmapData.push(
            {
                label: relationshipID,
                data: rangeData,
            })
    }); // end forEach

    return {
        group: person,
        data: personHeatmapData
    };
}

function getPersonObservationData(person, personObservationArray) {

    // Create an array of heatmap data for a specific observer
    var personHeatmapData = [];

    personObservationArray.forEach(observation => {

        let observationID = parseInt(observation.id);
        let measureRanges = extractMeasureRangeFromEma(observation.ema);
        let observationType = observation.musical_type;

        let rangeData = measureRanges.map(rangePair => {
            return {
                timeRange: rangePair,
                val: observationType,
            }
        });

        personHeatmapData.push(
            {
                label: observationID,
                data: rangeData,
            })
    }); // end forEach

    return {
        group: person,
        data: personHeatmapData
    };

}


function getPieceTypeFromID(pieceID) {
    if (pieceID.includes("Mass")) {
        return "Mass"
    } else if (pieceID.includes("Model")) {
        return "Model";
    } else {
        return "Other";
    }
}


function showAlert(alertText) {
    loader.className = "d-none";
    alert.innerHTML = alertText;
    alert.className = "container alert alert-info";
}
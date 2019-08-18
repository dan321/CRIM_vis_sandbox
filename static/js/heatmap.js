let container = document.querySelector("#heatmap");
let pieceID = container.dataset.id;
let relationshipURL = `https://crimproject.org/pieces/${pieceID}/relationships/?format=json`
let observationURL = `https://crimproject.org/pieces/${pieceID}/observations/?format=json`
let pageTitle = document.querySelector("#page-title")
let heatmapType
let heatmapSelect = document.querySelector('#heatmap-select')
let alert = document.querySelector("#alert")
let loader = document.querySelector("#loader")


// Where possible get the chart type from the container
if (container.dataset.type) {
    heatmapType = container.dataset.type
} else {
    heatmapType = heatmapSelect.options[heatmapSelect.selectedIndex].value;
}

// Generate correct heatmap type on initial load
if (heatmapType === "relationships") {
    createRelationshipHeatmap();
} else if (heatmapType === "observations") {
    createObservationHeatmap();
}


// If there is a dropdown, add a listener to it
if (heatmapSelect !== null) {
    document.querySelector('#heatmap-select').addEventListener('change', function () {
        heatmapType = getHeatmapType();
        alert.innerHTML = "";
        alert.className = "";
        loader.className = "mx-auto d-block mb-4";

        if (heatmapType === "relationships") {
            createRelationshipHeatmap();
        } else if (heatmapType === "observations") {
            createObservationHeatmap();
        }
    })
}


function createRelationshipHeatmap() {
    fetch(relationshipURL)
        .then(data => data.json())
        .then(jsonData => {


            // Get piece type. This is important because heatmaps for Masses and Models
            // will differ in what they show.
            // A model heatmap will show passages that have been borrowed for use in Masses
            // A Mass heatmap will show passages that have been borrowed from Models, or even other Masses

            let pieceType = getPieceTypeFromID(pieceID);
            let jsonModelDerivativeChoice;



            if (pieceType === "Model") {
                jsonModelDerivativeChoice = "relationships_as_model";
            } else if (pieceType === "Mass") {
                jsonModelDerivativeChoice = "relationships_as_derivative";
            }


            if (jsonData[jsonModelDerivativeChoice].length === 0) {
                showAlert("There are no relationships to show")
                return
            }

            // We need to group the relationships by observer
            let groupedChartData = _(jsonData[jsonModelDerivativeChoice]).groupBy(relationship => {
                return relationship.observer.name
            });


            // Extract relevant data for each person
            var combinedHeatmapData = [];
            for (var person in groupedChartData) {
                let personData = getPersonRelationshipData(person, groupedChartData[person], pieceType);
                combinedHeatmapData.push(personData);
            };


            container.innerHTML = ""
            loader.className = "d-none"

            // Plot heatmap
            TimelinesChart()(container)
                .data(combinedHeatmapData)
                .xTickFormat(n => `measure ${+n}`)
                .timeFormat('%Q')
                .zQualitative(true)
                .leftMargin(180)
                .onSegmentClick(d => {
                    window.location = `https://crimproject.org/relationships/${d.label}/`
                }) // end Timelines Chart
        }
        );

}




function createObservationHeatmap() {
    fetch(observationURL)
        .then(data => data.json())
        .then(jsonData => {


            if (jsonData.observations.length === 0) {
                showAlert("There are no observations to show")
                return
            }

            // We need to group the relationships by observer
            let groupedChartData = _(jsonData.observations).groupBy(observation => {
                return observation.observer.name
            });

            // Extract relevant data for each person
            var combinedHeatmapData = [];
            for (var person in groupedChartData) {
                let personData = getPersonObservationData(person, groupedChartData[person]);
                combinedHeatmapData.push(personData);
            };

            container.innerHTML = ""
            loader.className = "d-none"


            // Plot heatmap
            TimelinesChart()(container)
                .data(combinedHeatmapData)
                .xTickFormat(n => `measure ${+n}`)
                .timeFormat('%Q')
                .zQualitative(true)
                .leftMargin(180)
                .onSegmentClick(d => {
                    window.location = `https://crimproject.org/observations/${d.label}/`
                })
        }
        );
}




// HELPER FUNCTIONS
function extractMeasureRangeFromEma(ema) {

    let emaString = ema.split("/")[0];
    let emaRanges = emaString.split(',');

    let emaRangePairs = emaRanges.map(range => {
        let rangePair = range.split('-');
        rangePair = rangePair.map(el => parseInt(el));

        if (rangePair.length === 1) {
            return [
                rangePair[0],
                rangePair[0]
            ];

        } else if (rangePair.length === 2) {
            return rangePair;
        }
    } // end emaRanges.map
    );
    return emaRangePairs;
};

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
    var personHeatmapData = []

    personRelationshipArray.forEach(relationship => {

        let relationshipID = parseInt(relationship.id);
        let measureRanges = extractMeasureRangeFromEma(relationship[jsonPart].ema);

        let relationshipType = `${relationship.relationship_type}`;
        let additionalTypeInformation = `: ${relationship.model_observation.piece.piece_id} → ${relationship.derivative_observation.piece.piece_id}`
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
    }) // end forEach

    return {
        group: person,
        data: personHeatmapData
    };
}

function getPersonObservationData(person, personObservationArray) {

    // Create an array of heatmap data for a specific observer
    var personHeatmapData = []

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
    }) // end forEach

    return {
        group: person,
        data: personHeatmapData
    };

}


function getPieceTypeFromID(pieceID) {
    if (pieceID.includes("Mass")) {
        return "Mass"
    } else if (pieceID.includes("Model")) {
        return "Model"
    } else {
        "Other"
    }
}


function showAlert(alertText) {
    loader.className = "d-none"
    alert.innerHTML = alertText;
    alert.className = "container alert alert-info"
}
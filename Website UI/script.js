Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:8080/Classify_image"; //Use this if you are NOT using nginx.
        // var url="/api/Classify_image"; // Use this if  you are using nginx.

        $.post(url, {
            image_data: imageData
        },function(data, status) {
            /* 
            Below is a sample response if you have two faces in an image lets say virat and roger together.
            Most of the time if there is one person in the image you will get only one element in below array
            data = [
                {
                    class: "viral_kohli",
                    class_probability: [1.05, 12.67, 22.00, 4.5, 91.56],
                    class_dictionary: {
                        lionel_messi: 0,
                        maria_sharapova: 1,
                        roger_federer: 2,
                        serena_williams: 3,
                        virat_kohli: 4
                    }
                },
                {
                    class: "roder_federer",
                    class_probability: [7.02, 23.7, 52.00, 6.1, 1.62],
                    class_dictionary: {
                        lionel_messi: 0,
                        maria_sharapova: 1,
                        roger_federer: 2,
                        serena_williams: 3,
                        virat_kohli: 4
                    }
                }
            ]
            */
            console.log(data);
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            // let players = ["lionel_messi", "maria_sharapova", "roger_federer", "serena_williams", "virat_kohli"];
            
            let match = [];
            let bestScore = -1;
            let k=0;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match[k++] = data[i];
                    bestScore = maxScoreForThisClass;
                    
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                // $("#divClassTable").show();

                let imagesHtml = '';
                for (let i = 0; i < match.length; i++) {
                    imagesHtml += $(`[data-player="${match[i].class}"`).html();
                }
                $("#resultHolder").html(imagesHtml);

                // let classDictionary = match.class_dictionary;
                // for(let personName in classDictionary) {
                //     let index = classDictionary[personName];
                //     let probabilityScore = match.class_probability[index];
                //     let elementName = "#Score_" + personName;
                //     $(elementName).html(probabilityScore);
                // }

            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});
$(document).ready(function () {    
    // Get the name of the selected whiskey
    // $('.whiskey_select :selected').text());
    
    // Get the id of the selected whiskey
    // $('.whiskey_select').val());
    
    // Handle events
    $(".whiskey_select").on("select2:select", function (evt) { prepareSliders(); });
    document.getElementById("submitRating").onclick = submitRatings;
    
    // Configuration for select box
    getWhiskeyList().success( function(data) {
        $(".whiskey_select").select2({
            placeholder: "Select a whiskey",
            allowClear: true,
            data: data
        });
    });

    // Configuration for sliders
    var overall = document.getElementById('overall');
    var flavorProfiles = ['sweet', 'sour', 'heat', 'smooth', 'finish', 'crisp', 'leather', 'wood', 'smoke', 'citrus', 'floral', 'fruit']

    createHorizontalSlider("overall")
    flavorProfiles.forEach(createVerticalSlider)


    // Configuration for Ratings table
    $("#table_list").jqGrid({
        url: "https://whiskey.bythenums.com/main/whiskey/getAllRatings",
        datatype: "json",
        mtype: 'GET',
        height: 400,
        autowidth: true,
        shrinkToFit: true,
        rowNum: 20,
        rowList: [10, 20, 30],
        colNames:[ 'Whiskey', 'User', 'Rating', 'Sweet', 'Sour', 'Heat', 'Smooth', 'Finish', 'Crisp', 'Leather', 'Wood', 'Smoke', 'Citrus', 'Floral', 'Fruit', 'Notes' ],
        colModel:[
            {name:'whiskeyId.name',index:'whiskeyId.name', editable: true, width:50, sorttype:"text",search:true},
            {name:'userId.email',index:'userId.email', editable: true, width:20, sorttype:"text",search:true},
            {name:'rating',index:'rating', editable: true, width:8, sorttype:"float",search:true},
            {name:'sweet',index:'sweet', editable: true, width:8, sorttype:"float",search:false},
            {name:'sour',index:'sour', editable: true, width:8, sorttype:"float",search:false},
            {name:'heat',index:'heat', editable: true, width:8, sorttype:"float",search:false},
            {name:'smooth',index:'smooth', editable: true, width:10, sorttype:"float",search:false},
            {name:'finish',index:'finish', editable: true, width:8, sorttype:"float",search:false},
            {name:'crisp',index:'crisp', editable: true, width:8, sorttype:"float",search:false},
            {name:'leather',index:'leather', editable: true, width:10, sorttype:"float",search:false},
            {name:'wood',index:'wood', editable: true, width:8, sorttype:"float",search:false},
            {name:'smoke',index:'smoke', editable: true, width:8, sorttype:"float",search:false},
            {name:'citrus',index:'citrus', editable: true, width:8, sorttype:"float",search:false},
            {name:'floral',index:'floral', editable: true, width:8, sorttype:"float",search:false},
            {name:'fruit',index:'fruit', editable: true, width:8, sorttype:"float",search:false},
            {name:'notes',index:'notes', editable: true, width:50, sorttype:"text",search:false},

        ],
        pager: "#pager_list",
        viewrecords: true,
        caption: "Whiskey Ratings",
        add: true,
        edit: true,
        addtext: 'Add',
        edittext: 'Edit',
        hidegrid: false,
        editurl: "https://whiskey.bythenums.com/main/whiskey/rating",
    });

    // Setup buttons
    $("#table_list").jqGrid('navGrid', '#pager_list',
            {edit: true,
             add: true,
             del: true,
             search: true}
    );

    // Add responsive to jqGrid
    $(window).bind('resize', function () {
        var width = $('.jqGrid_wrapper').width();
        $('#table_list').setGridWidth(width);
    });
    
    function getWhiskeyList() {
        var baseUrl='https://whiskey.bythenums.com/main/whiskey/getAllWhiskies'
        
        return $.ajax({
            url: baseUrl,
            dataType: 'json',
            data: { page: 1,
                    rows: 500,
                    sort: 'name',
                    namesOnly: true }
        });
    }
    
    function prepareSliders() {
        getUserRating($('.whiskey_select').val()).success( function(data) {
            if (data != null) {
                updateSliderValue("overall", data["rating"]);
                flavorProfiles.forEach(function (item) {updateSliderValue(item,data[item])});
                document.getElementById("notes").value = data["notes"];
            }
            else{
                alert("You have not yet rated this whiskey.")
            }
        });
    }
    
    function getUserRating(whiskeyId) {
        var baseUrl='https://whiskey.bythenums.com/main/whiskey/rating'
        
        return $.ajax({
            url: baseUrl,
            dataType: 'json',
            data: { whiskeyId: whiskeyId }
        });
    }
    
    function createVerticalSlider(flavorProfile) {
        noUiSlider.create(document.getElementById(flavorProfile),{
            start: 1,
            connect: 'lower',
            orientation: 'vertical',
            direction: 'rtl',
            range: {
                'max':  5,
                'min':  0
            },
            tooltips: [wNumb({ decimals: 1 })],
        });
    }
    
    function createHorizontalSlider(flavorProfile) {
        noUiSlider.create(document.getElementById(flavorProfile),{
            start: 1,
            connect: 'lower',
            orientation: 'horizontal',
            range: {
                'max':  5,
                'min':  0
            },
            tooltips: [wNumb({ decimals: 1 })],
        });
    }
    
    function updateSliderValue(flavorProfile, value) {
        console.log("Updating slider " + flavorProfile + " to " + value)
        document.getElementById(flavorProfile).noUiSlider.set(value);
    }
    
    function updateUserRating() {
        //code
    }
    
    function submitRatings() {
        alert("Pushed button")
    }
});
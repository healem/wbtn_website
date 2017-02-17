$(document).ready(function () {

    // Configuration for select box
    $(".whiskey_select").select2({
        placeholder: "Select a whiskey",
        allowClear: true
    });


    // Configuration for slider
    var basic_slider = document.getElementById('basic_slider');
    var basic_slider2 = document.getElementById('basic_slider2');

    noUiSlider.create(basic_slider,{
        start: 0,
        connect: 'lower',
        orientation: 'vertical',
        direction: 'rtl',
        range: {
            'max':  5,
            'min':  0
        },
        tooltips: [wNumb({ decimals: 1 })],
    });
    
    noUiSlider.create(basic_slider2,{
        start: 0,
        connect: 'lower',
        orientation: 'vertical',
        direction: 'rtl',
        range: {
            'min':  0,
            'max':  5
        },
        tooltips: [wNumb({ decimals: 1 })],
    });


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
            {name:'whiskeyId.name',index:'whiskeyId.name', editable: true, width:10, sorttype:"text",search:true},
            {name:'userId.email',index:'userId.email', editable: true, width:10, sorttype:"text",search:true},
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
});
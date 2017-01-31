$(document).ready(function () {

    // Configuration for user table
    $("#table_list").jqGrid({
        url: "https://whiskey.bythenums.com/main/whiskey/getAllRatings",
        datatype: "json",
        mtype: 'GET',
        height: 400,
        autowidth: true,
        shrinkToFit: true,
        rowNum: 20,
        rowList: [10, 20, 30],
        colNames:[ 'WhiskeyId', 'UserId', 'Rating', 'Sweet', 'Sour', 'Heat', 'Smooth', 'Finish', 'Crisp', 'Leather', 'Wood', 'Smoke', 'Citrus', 'Floral', 'Fruit', 'Notes' ],
        colModel:[
            {name:'whiskeyId',index:'whiskeyId', editable: true, width:10, sorttype:"int",search:true},
            {name:'userId',index:'userId', editable: true, width:10, sorttype:"int",search:true},
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
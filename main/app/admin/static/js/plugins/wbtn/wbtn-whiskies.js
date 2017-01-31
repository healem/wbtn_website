$(document).ready(function () {

    // Configuration for user table
    $("#table_list").jqGrid({
        url: "https://whiskey.bythenums.com/main/whiskey/getAllWhiskies",
        datatype: "json",
        mtype: 'GET',
        height: 400,
        autowidth: true,
        shrinkToFit: true,
        rowNum: 20,
        rowList: [10, 20, 30],
        colNames:['Name','Price', 'Proof', 'Style','Age','Icon', 'Url'],
        colModel:[
            {name:'name',index:'name', editable: true, width:60, sorttype:"text",search:true, key:true},
            {name:'price',index:'price', editable: true, width:20, sorttype:"float",search:true},
            {name:'proof',index:'proof', editable: true, width:20, sorttype:"float",search:true},
            {name:'style',index:'style', editable: true, width:50, sorttype:"text",search:true},
            {name:'age',index:'age', editable: true, width:20, sorttype:"int",search:true},
            {name:'icon',index:'icon', editable: false, width:80, sorttype:"text",search:false},
            {name:'url',index:'url', editable: true, width:60, sorttype:"text",search:false},
        ],
        pager: "#pager_list",
        viewrecords: true,
        caption: "Whiskies",
        add: true,
        edit: true,
        addtext: 'Add',
        edittext: 'Edit',
        hidegrid: false,
        editurl: "https://whiskey.bythenums.com/main/whiskey/whiskey",
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
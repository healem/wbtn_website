$(document).ready(function () {

    // Configuration for user table
    $("#table_list").jqGrid({
        url: "https://whiskey.bythenums.com/main/users/getAllWhiskies",
        datatype: "json",
        mtype: 'GET',
        height: 400,
        autowidth: true,
        shrinkToFit: true,
        rowNum: 20,
        rowList: [10, 20, 30],
        colNames:['Name','Price', 'Proof', 'Style','Age','Icon'],
        colModel:[
            {name:'name',index:'name', editable: true, width:40, sorttype:"text",search:true, key:true},
            {name:'price',index:'price', editable: false, width:40, sorttype:"text",search:true},
            {name:'proof',index:'proof', editable: false, width:50, sorttype:"text",search:true},
            {name:'style',index:'proof', editable: false, width:50, sorttype:"text",search:true},
            {name:'age',index:'proof', editable: false, width:50, sorttype:"text",search:true},
            {name:'icon',index:'proof', editable: false, width:50, sorttype:"text",search:true},
        ],
        pager: "#pager_list",
        viewrecords: true,
        caption: "Whiskies",
        add: true,
        edit: true,
        addtext: 'Add',
        edittext: 'Edit',
        hidegrid: false,
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
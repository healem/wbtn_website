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
        colNames:['Name','Price', 'Proof', 'Style','Age','Icon', 'Url'],
        colModel:[
            {name:'name',index:'name', editable: true, width:40, sorttype:"text",search:true, key:true},
            {name:'price',index:'price', editable: true, width:40, sorttype:"text",search:true},
            {name:'proof',index:'proof', editable: true, width:50, sorttype:"text",search:true},
            {name:'style',index:'style', editable: true, width:50, sorttype:"text",search:true},
            {name:'age',index:'age', editable: true, width:50, sorttype:"text",search:true},
            {name:'icon',index:'icon', editable: true, width:50, sorttype:"text",search:true},
            {name:'url',index:'url', editable: true, width:50, sorttype:"text",search:true},
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
    
    // delete whiskey
    function deleteWhiskey(rowid) {
        var localData = $(this).jqGrid("getLocalRow", rowid);
        
        var baseUrl='https://whiskey.bythenums.com/main'
    
        $.ajax({
            url: baseUrl + '/whiskey/deleteWhiskey',
            dataType: 'text',
            data: { name: rowid },
            success: function(data){
                if (data == 'OK') {
                    console.log("Successful delete");
                }
                else{
                    console.log("Failed delete whiskey: ", data);
                    alert('failed to delete whiskey: ' + data.responseText);
                }
            },
            error: function(data){
                console.log("Failed delete whiskey: ", data);
                alert('ERROR: failed to delete whiskey: ' + data.responseText);
            }
        });
    }

    // Setup buttons
    $("#table_list").jqGrid('navGrid', '#pager_list',
            {edit: true,
             add: true,
             del: true, delfunc: deleteWhiskey,
             search: true}
    );

    // Add responsive to jqGrid
    $(window).bind('resize', function () {
        var width = $('.jqGrid_wrapper').width();
        $('#table_list').setGridWidth(width);
    });
});
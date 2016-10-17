$(document).ready(function () {


    // Examle data for jqGrid
    var mydata = [
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"},
        {firstname: "First", lastname: "Last", email: "test@email.com", normal: "True", blogger: "False", college: "False", admin: "True"}
    ];


    // Configuration for user table
    $("#table_list").jqGrid({
        url: "https://whiskey.bythenums.com/main/users/getAllUsers",
        datatype: "json",
        mtype: 'GET',
        height: 450,
        autowidth: true,
        shrinkToFit: true,
        rowNum: 20,
        rowList: [10, 20, 30],
        colNames:['Firstname','Lastname', 'Email', 'Normal','Blogger','College','Admin'],
        colModel:[
            {name:'firstName',index:'firstName', editable: false, width:40, sorttype:"text",search:true},
            {name:'lastName',index:'lastName', editable: false, width:40, sorttype:"text",search:true},
            {name:'email',index:'email', editable: false, width:50, sorttype:"text",search:true},
            {name:'userRater',index:'userRater', editable: true, width:20, sortable:false,search:false,
                edittype:'checkbox', editoptions: { value:"True:False"}, formatter:'checkbox', formatoptions : {disabled:false}},
            {name:'blogWriter',index:'blogWriter', editable: true, width:20, sortable:false,search:false,
                edittype:'checkbox', editoptions: { value:"True:False"}, formatter:'checkbox', formatoptions : {disabled:false}},
            {name:'collegeRater',index:'collegeRater', editable: true, width:20,sortable:false,search:false,
                edittype:'checkbox', editoptions: { value:"True:False"}, formatter:'checkbox', formatoptions : {disabled:false}},
            {name:'whiskeyAdmin',index:'whiskeyAdmin', editable: true, width:20, sortable:false,search:false,
                edittype:'checkbox', editoptions: { value:"True:False"}, formatter:'checkbox', formatoptions : {disabled:false}}
        ],
        pager: "#pager_list",
        viewrecords: true,
        caption: "Users",
        add: true,
        edit: true,
        addtext: 'Add',
        edittext: 'Edit',
        hidegrid: false,
    });

    // Add selection
    $("#table_list").setSelection(4, true);

    // Setup buttons
    $("#table_list").jqGrid('navGrid', '#pager_list',
            {edit: true, add: true, del: true, search: true},
            {height: 200, reloadAfterSubmit: true}
    );

    // Add responsive to jqGrid
    $(window).bind('resize', function () {
        var width = $('.jqGrid_wrapper').width();
        $('#table_list').setGridWidth(width);
    });
});
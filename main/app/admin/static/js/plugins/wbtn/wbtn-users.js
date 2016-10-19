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
        height: 400,
        autowidth: true,
        shrinkToFit: true,
        rowNum: 20,
        rowList: [10, 20, 30],
        colNames:['Firstname','Lastname', 'Email', 'Normal','Blogger','College','Admin'],
        colModel:[
            {name:'firstName',index:'firstName', editable: false, width:40, sorttype:"text",search:true},
            {name:'lastName',index:'lastName', editable: false, width:40, sorttype:"text",search:true},
            {name:'email',index:'email', editable: false, width:50, sorttype:"text",search:true, key:true},
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
        beforeSelectRow: function (rowid, e) {
            var $self = $(this),
                iCol = $.jgrid.getCellIndex($(e.target).closest("td")[0]),
                cm = $self.jqGrid("getGridParam", "colModel"),
                localData = $self.jqGrid("getLocalRow", rowid);
            if (cm[iCol].name === "userRater") {
                var cbValue = false;
                if ($(e.target).is(":checked")) {
                    cbValue = true;
                }
                return updateUser(rowid, "userRater", cbValue);
            }
            if (cm[iCol].name === "blogWriter") {
                var cbValue = false;
                if ($(e.target).is(":checked")) {
                    cbValue = true;
                }
                return updateUser(rowid, "blogWriter", cbValue);
            }
            if (cm[iCol].name === "collegeRater") {
                var cbValue = false;
                if ($(e.target).is(":checked")) {
                    cbValue = true;
                }
                return updateUser(rowid, "collegeRater", cbValue);
            }
            if (cm[iCol].name === "whiskeyAdmin") {
                var cbValue = false;
                if ($(e.target).is(":checked")) {
                    cbValue = true;
                }
                return updateUser(rowid, "whiskeyAdmin", cbValue);
            }
    
            return true; // allow selection
        },
    });

    // submit change
    function updateUser(email, permissionName, permissionValue) {
        var baseUrl='https://whiskey.bythenums.com/main'
    
        $.ajax({
            url: baseUrl + '/users/updateUser',
            dataType: 'text',
            data: { permissionName: permissionName,
                    email: email,
                    permissionValue: permissionValue},
            success: function(data){
                if (data == 'OK') {
                    console.log("Successful update");
                }
                else{
                    console.log("Failed Update user permissions: ", data);
                    alert('failed to update user permissions: ' + data.responseText);
                }
            },
            error: function(data){
                console.log("Failed Update user permissions: ", data);
                alert('ERROR: failed to update user permissions: ' + data.responseText);
            }
        });
    }
    
    // delete user
    function deleteUser(rowid) {
        var localData = $(this).jqGrid("getLocalRow", rowid);
        
        var baseUrl='https://whiskey.bythenums.com/main'
    
        $.ajax({
            url: baseUrl + '/users/deleteUser',
            dataType: 'text',
            data: { email: rowid },
            success: function(data){
                if (data == 'OK') {
                    console.log("Successful delete");
                }
                else{
                    console.log("Failed delete user: ", data);
                    alert('failed to delete user: ' + data.responseText);
                }
            },
            error: function(data){
                console.log("Failed delete user: ", data);
                alert('ERROR: failed to delete user: ' + data.responseText);
            }
        });
    }

    // Setup buttons
    $("#table_list").jqGrid('navGrid', '#pager_list',
            {edit: false,
             add: false,
             del: true, delfunc: deleteUser,
             search: true}
    );

    // Add responsive to jqGrid
    $(window).bind('resize', function () {
        var width = $('.jqGrid_wrapper').width();
        $('#table_list').setGridWidth(width);
    });
});
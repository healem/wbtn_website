// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
  console.log('statusChangeCallback');
  console.log(response);
  // The response object is returned with a status field that lets the
  // app know the current login status of the person.
  // Full docs on the response object can be found in the documentation
  // for FB.getLoginStatus().
  if (response.status === 'connected') {
    // Logged into your app and Facebook.
    var accessToken = response.authResponse.accessToken;
    testAPI(accessToken);
  } else if (response.status === 'not_authorized') {
    // The person is logged into Facebook, but not your app.
    document.getElementById('status').innerHTML = 'Please log ' +
      'into this app.';
  } else {
    // The person is not logged into Facebook, so we're not sure if
    // they are logged into this app or not.
    document.getElementById('status').innerHTML = 'Please log ' +
      'into Facebook.';
  }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
  FB.getLoginStatus(function(response) {
    statusChangeCallback(response);
  });
}

window.fbAsyncInit = function() {
FB.init({
  appId      : '125580131179623',
  cookie     : true,  // enable cookies to allow the server to access 
                      // the session
  xfbml      : true,  // parse social plugins on this page
  version    : 'v2.7' // use graph api version 2.7
});

// Now that we've initialized the JavaScript SDK, we call 
// FB.getLoginStatus().  This function gets the state of the
// person visiting this page and can return one of three states to
// the callback you provide.  They can be:
//
// 1. Logged into your app ('connected')
// 2. Logged into Facebook, but not your app ('not_authorized')
// 3. Not logged into Facebook and can't tell if they are logged into
//    your app or not.
//
// These three cases are handled in the callback function.

FB.getLoginStatus(function(response) {
  statusChangeCallback(response);
});

};

// Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function testAPI(accessToken) {
  console.log('Welcome!  Fetching your information.... ');
  FB.api('/me?fields=email, name', function(response) {
    console.log('Successful login for: ' + response.name + " at email " + response.email);
    document.getElementById('status').innerHTML =
      'Thanks for logging in, ' + response.name + " at email " + response.email + '!';
      
    window.localStorage.setItem('current-username', response.name);
    
    submitWBTN(accessToken, response.email);
  });
}

// Submit to server
function submitWBTN(token, email) {
    tryLogin(token, email)
}
    
function tryLogin(token, email) {
    var baseUrl='https://whiskey.bythenums.com/main'
    
    $.ajax({
        url: baseUrl + '/auth/login',
        dataType: 'text',
        data: { token: token,
                provider: 1},
        success: function(data){
            if (data == 'OK') {
                console.log("Successful wbtn login: ", data);
                window.location = "https://whiskey.bythenums.com/main/"
            }
            else {
                console.log("Failed wbtn login: ", data);
                tryRegister(token, email);
            }
        },
        error: function(data){
            console.log("Failed wbtn login: ", data);
            document.getElementById('status').innerHTML =
            '<div class="alert alert-danger">Login failed with message: ' + data.responseText + '<p> Please try again later.</div>';
        }
    });
}

function tryRegister(token, email) {
    var baseUrl='https://whiskey.bythenums.com/main'
    
    $.ajax({
        url: baseUrl + '/auth/register',
        dataType: 'text',
        data: { token: token,
                email: email,
                provider: 1},
        success: function(data){
            if (data == 'OK') {
                console.log("Successful wbtn register: ", data);
                window.location = "https://whiskey.bythenums.com/main/"
            }
            else{
                console.log("Failed wbtn register: ", data);
                document.getElementById('status').innerHTML =
                '<div class="alert alert-danger">Auto-registration failed with message: ' + data.responseText + '<p>Please try manual registration at <a href="/main/register"><i class="fa fa-th-large"></i> <span class="nav-label">Register</span></a></div>';
            }
        },
        error: function(data){
            console.log("Failed wbtn register: ", data);
            document.getElementById('status').innerHTML =
            '<div class="alert alert-danger">Auto-registration failed with message: ' + data.responseText + '<p>Please try manual registration at <a href="/main/register"><i class="fa fa-th-large"></i> <span class="nav-label">Register</span></a></div>';
        }
    });
}
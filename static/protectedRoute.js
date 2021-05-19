const authenticated = sessionStorage.getItem('authenticated');

if (!authenticated) {
   location.replace("./static/login.html");
};

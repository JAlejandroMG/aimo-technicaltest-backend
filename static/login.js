const login = document.getElementById('login');
if(login) {
   login.addEventListener('submit', (event) => {
      event.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      const userLogin = {username: username, password: password};
      postLogin(userLogin);
   })
}



const postLogin = (userLogin) => {
   const urlLogin = "http://127.0.0.1:8000/v1/login";
   const headers = {'Content-Type': 'application/json;charset=utf8', 'Accept': 'application/json'};
   fetch(urlLogin, {
      mode: 'no-cors',
      method: `POST`,
      headers: headers,
      body: JSON.stringify(userLogin)
   })
   .then(response => {
      console.log(response)
      console.log(response.body)
      return response.json() //****//
   })
   .then(data => {
      console.log(data)
      showLogin(data)
   })
   .catch(error => console.log(error));



   const showLogin = (data) => {
      console.log("Entrando a registrar el token...")
      sessionStorage.setItem('authenticated', JSON.stringify({token: data.token}));
      location.replace('../index.html');
   };
};

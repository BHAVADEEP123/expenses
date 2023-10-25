const userNameField = document.querySelector("#userNameField");
const invalidFeedBackField = document.querySelector(".invalid-feedback");
const emailField = document.querySelector("#emailField");
const validEmail = document.querySelector(".valid-email");
const invalidEmail = document.querySelector(".invalid-email");
const passwordField = document.querySelector("#passwordField");
const validFeedBackField = document.querySelector(".valid-feedback");
const weekPass = document.querySelector(".weak-pass");
const strongPass = document.querySelector(".strong-pass");
const toggleMode = document.querySelector(".toggleMode");
const submitBtn = document.querySelector(".submit-btn");
var flagUser = 1;
var flagEmail = 1;

toggleMode.addEventListener("click",(e)=>{
    if(toggleMode.textContent==="SHOW"){
        toggleMode.textContent="HIDE";
        passwordField.setAttribute("type","text");
    }
    else{
        toggleMode.textContent="SHOW";
        passwordField.setAttribute("type","password");
    }
});

userNameField.addEventListener("keyup", (e) => {
    console.log(flagEmail+" "+flagUser);
    const userNameVar = e.target.value;
    userNameField.classList.remove("is-invalid");
    invalidFeedBackField.style.display = "none";
    validFeedBackField.style.display = "none";
    if (userNameVar.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: userNameVar}),
            method: "POST",
        }).then(res => res.json())
            .then(data => {
                console.log('data', data);
                if(data.username_error){
                    userNameField.classList.add("is-invalid");
                    invalidFeedBackField.style.display = "block";
                    validFeedBackField.style.display = "none";
                    invalidFeedBackField.innerHTML=`<p>${data.username_error}</p>`;
                    submitBtn.disabled = true;
                    flagUser=0;
                }
                else{
                    if(flagEmail){
                        submitBtn.removeAttribute("disabled");
                    }
                    flagUser=1;
                    userNameField.classList.remove("is-invalid");
                    invalidFeedBackField.style.display = "none";
                    validFeedBackField.style.display = "block";
                    validFeedBackField.innerHTML = `<p>Looks Great</p>`
                }
            });
    }
    else{
        if(flagEmail){
            submitBtn.removeAttribute("disabled");
        }
    }

});

passwordField.addEventListener("keyup",(e)=>{
    console.log("password checker");
    strongPass.style.display = "none";
    weekPass.style.display = "none";
    const passwordVar = e.target.value.trim();
    if(passwordVar.length>0){
        console.log('pass',passwordVar);
        fetch('/authentication/password-strength',{
            body: JSON.stringify({password: passwordVar}),
            method: "POST",
        }).then(res=>res.json())
        .then(data=> {
            console.log('data',data);
            if(data.weak){
                strongPass.style.display = "none";
                weekPass.style.display = "block";
            }
            else{
                strongPass.style.display = "block";
                weekPass.style.display = "none";
            }
        });
    }
});

emailField.addEventListener("keyup",(e)=>{
    console.log(flagEmail+" "+flagUser);
    const emailVar = e.target.value;
    emailField.classList.remove("is-invalid");
    invalidEmail.style.display = "none";
    validEmail.style.display = "none";
    if (emailVar.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVar}),
            method: "POST",
        }).then(res => res.json())
            .then(data => {
                console.log('data', data);
                if(data.email_error){
                    emailField.classList.add("is-invalid");
                    invalidEmail.style.display = "block";
                    validEmail.style.display = "none";
                    invalidEmail.innerHTML=`<p>${data.email_error}</p>`;
                    submitBtn.disabled = true;
                    flagEmail=0;
                }
                else{
                    if(flagUser){
                        submitBtn.removeAttribute("disabled");
                    }
                    flagEmail=1;
                    emailField.classList.remove("is-invalid");
                    invalidEmail.style.display = "none";
                    validEmail.style.display = "block";
                    validEmail.innerHTML = `<p>Valid</p>`
                }
            });
    }
    else{
        if(flagUser){
            submitBtn.removeAttribute("disabled");
        }
    }

});



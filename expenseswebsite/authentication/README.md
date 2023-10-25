FOR EMAIL VERIFICATION:
    1) Sending email:
        1) GIVE CREDENTIALS IN settings.py
        2) make email body where ever you want to send 
            which goes like this: 
            from django.core.mail import EmailMessage

            email = EmailMessage(
                "Hello",
                "Body goes here",
                "from@example.com",
                ["to1@example.com", "to2@example.com"],
                ["bcc@example.com"],
                reply_to=["another@example.com"],
                headers={"Message-ID": "foo"},
            )
            REF: https://docs.djangoproject.com/en/4.2/topics/email/
        3) after writing use a command to send : email.send (fail_silently = False)
        4) Now in the body of the above mentioned email we need to send a link by which clicking will make user active
        5) Making that link:   
            It can be done in many ways but make sure that some info about user is present in that link so that we can retrive user Id or user pk to make him an active user in backend
        6) Finally we can send the link 

    2) Activating the user when he clicks link in the mail
        1) Now this is a get request.
        2) Now when the request is recieved then we get id from the request and check the user activity and make his is_active as true
        3) Now we redirect him to login page when the get request is processed
    
    3) Login
        1) When the user logins using post request we check his creds and let him enter the main page.
        2) When creds are wrong or user is not active we send him to login page with appropriate message
    4) Logout
        1) When the user submits the logout button then he will be logged out with auth.logout(request) and redirected to login page.
        2) We need to make sure that no one can enter main page directly
        3) if so we will redirect him to the login page using :
            from django.contrib.auth.decorators import login_required
            @login_required(login_url='/authentication/login')

            This will prevent a user to directly enter the main page.
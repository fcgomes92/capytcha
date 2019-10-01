* Create an APPLICATION inside the API Admin
* Send the CLIENT_TOKEN to the new user (ask them to store it)
* Two main endpoints:
    * /captcha/get  :   get a new image + sound + token
    - Request:
        - Headers:
            - Authorization: Bearer <CLIENT_TOKEN>
    - Response:
        - Body:
            ```json
            {
                "user_token": "<JWT Token>",
                "image": "<image binary>",
                "audio": "<audio binary>"
            }
            ```
        
    * /captcha/check :   check the given text sent by the user
    - Request:
        - Headers:
            - Authorization: Bearer <CLIENT_TOKEN>
            - Body (JSON):
                ```json
                {
                    "user_token": "<JWT Token>",
                    "value": "<user input response based on the image / audio provided>"
                }
                ```
    - Response:
        - Body: 
            ```json
            {
                "valid": "true | false"
            }
            ```
            
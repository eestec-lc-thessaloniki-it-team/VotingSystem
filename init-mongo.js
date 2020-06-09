db.createUser(
    {
        user : "my_user"
        pwd  : "my_password"
        roles : [
            {
                role : "readWrite",
                db   :  "lcThessalonikiVoting"
            }
        ]
    }
)

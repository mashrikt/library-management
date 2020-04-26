# Library Management
> RESTful API for Library Management

## Getting Started


### Prerequisites

- Docker
- Docker Compose


### Installing

Clone the project and then cd into the project directory from the terminal. Run the following command.
```
$ docker-compose up --build
```

## Running the tests

On another terminal, run the following commands.

```
$ docker-compose exec web bash
# pytest -v
```

## About

This project is an implementation of a very simple library management system. 

It has two types of users: admin and member. Admin's have the authority to add Authors and Books and also approve 
requests from member's request to Borrow books. Admin users can also add other admins. There is also an admin endpoint 
to download CSV data of the list of Borrowed books.

## Relevant API endpoints
Detail Endpoint Documentation is in the `/docs/` endpoint.

#### /api/v1/auth/registration/
Register User Endpoint. Anyone can register as a `member`, but an `admin` user can only add other admins.


Sample Request
```json
{
    "email": "library@member.com",
    "password1": "mysecretpassword8283[p,..",
    "password2": "mysecretpassword8283[p,..",
    "user_type": "member"
}
```


#### /api/v1/auth/login/
Login Endpoint

Sample Request
```json
{
    "email": "library@member.com",
    "password": "mysecretpassword8283[p,.."
}
```

Sample Response
```json
{
    "token": "JWT_TOKEN",
    "user": {
        "id": 1,
        "first_name": "Library",
        "last_name": "Member",
        "email": "library@member.com",
        "user_type": "member",
        "image": "http://something/media/profile_pictures/16498.jpg"
    }
}
```


#### /api/v1/auth/user/
User Profile Endpoint

Sample Request
```json
{
    "id": 1,
    "first_name": "Library",
    "last_name": "Member",
    "email": "a@a.com",
    "user_type": "library@member.com",
    "image": "http://something/media/profile_pictures/16498.jpg"
}
```


#### /api/v1/authors/
Author List Create Endpoint (only admin user's can create)

Sample Request
```json
[
    {
        "id": 1,
        "name": "Sir Arthur Conna Doyle"
    },
    {
        "id": 2,
        "name": "J.K. Rowling"
    }
]
```


#### /api/v1/authors/{author_id}/
Author Retrieve Update Destroy Endpoint (only admin user's can edit/delete Authors)

Sample Request
```json
[
    {
        "id": 1,
        "name": "Sir Arthur Conna Doyle"
    },
    {
        "id": 2,
        "name": "J.K. Rowling"
    }
]
```


#### /api/v1/books/
Books List Create Endpoint (only admin user's can create)

Sample Request
```json
[
    {
        "id": 1,
        "name": "Sherlock Holmes",
        "author": [
            {
                "id": 1,
                "name": "Sir Arthur Conna Doyle"
            }
        ]
    },
    {
        "id": 2,
        "name": "Harry Potter",
        "author": [
            {
                "id": 2,
                "name": "J.K. Rowling"
            }
        ]
    }
]
```


#### /api/v1/books/{book_id}/
Book Retrieve Update Destroy Endpoint (only admin user's can edit/delete Authors)

Sample Request
```json
{
    "id": 1,
    "name": "Sherlock Holmes",
    "author": [
        {
            "id": 1,
            "name": "Sir Arthur Conna Doyle",
            "dob": "1859-05-22",
            "description": ""
        }
    ],
    "description": "",
    "count": 20
}
```


#### /api/v1/books/{book_id}/borrow/
Endpoint to request to borrow a book


Sample Request
```json
{}
```

Sample Response
```json
{
    "id": 5
}
```


#### /api/v1/borrow/
List of Borrow (only admin access)


Sample Request
```json
[
    {
        "id": 1,
        "book": {
            "id": 2,
            "name": "Harry Potter",
            "author": [
                {
                    "id": 2,
                    "name": "J.K. Rowling"
                }
            ]
        },
        "user": {
            "id": 2,
            "first_name": "Library",
            "last_name": "Man",
            "email": "lib@man.com",
            "user_type": "member",
            "image": null
        },
        "created_at": "2020-04-26T19:41:14.472073Z",
        "updated_at": "2020-04-26T20:09:58.412439Z",
        "status": "request",
        "note": "",
        "created_by": 1,
        "updated_by": 1
    }
]
```


#### /api/v1/borrow/{borrow_id}/
Borrow Retrieve Update Destroy (only admin access)

Sample Request
```json

{
    "id": 1,
    "book": {
        "id": 2,
        "name": "Harry Potter",
        "author": [
            {
                "id": 2,
                "name": "J.K. Rowling"
            }
        ]
    },
    "user": {
        "id": 2,
        "first_name": "Library",
        "last_name": "Man",
        "email": "lib@man.com",
        "user_type": "member",
        "image": null
    },
    "created_at": "2020-04-26T19:41:14.472073Z",
    "updated_at": "2020-04-26T20:09:58.412439Z",
    "status": "request",
    "note": "",
    "created_by": 1,
    "updated_by": 1
}

```

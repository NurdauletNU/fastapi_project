from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from src.auth.routers import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from .errors import (
    create_exception_handler,
    InvalidCredentials,
    TagAlreadyExists,
    BookNotFound,
    UserAlreadyExists,
    UserNotFound,
    InsufficientPermission,
    AccessTokenRequired,
    InvalidToken,
    RefreshTokenRequired,
    RevokedToken
)




version = "v1"


app=FastAPI(
    title='Bookly',
    description='A REST API for a book review web service',
    version=version,

)



app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, 
                             initial_detail = {"message": "User with email already exists",
                                               "error_code": "user exists "})
)


app.add_exception_handler(
    UserNotFound,
    create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, 
                             initial_detail = {"message": "User not found",
                                               "error_code": "user not found "})
)



app.add_exception_handler(
    BookNotFound,
    create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, 
                             initial_detail = {"message": "Book not found",
                                               "error_code": "book not found "})
)


app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, 
                             initial_detail = {"message": "Invalid email or password",
                                               "error_code": "invalid_email_or_password"})
)


app.add_exception_handler(
    InvalidToken,
    create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, 
                             initial_detail = {"message": "Token is invalid or expired",
                                               "resolution": "Please get new an access token",
                                               "error_code": "invalid_token"})
)


app.add_exception_handler(
    RevokedToken,
    create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, 
                             initial_detail = {"message": "Token is invalid or has been revoked",
                                               "error_code": "invalid_revoked"})
)


app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, 
                             initial_detail = {"message": "Please provide a valid access token",
                                               "resolution": "Please get new an access token",
                                               "error_code": "access_token_required"})
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, 
                             initial_detail = {"message": "Please provide a valid access token",
                                               "resolution": "Please get new a refresh token",
                                               "error_code": "access_token_required"})
)


@app.exception_handler(500)
async def internal_server_error(request, exc):

    return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "server_error",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=['reviews'])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=['tags'])
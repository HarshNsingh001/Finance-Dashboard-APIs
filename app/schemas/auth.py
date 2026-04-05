from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):

    name: str = Field(..., min_length=2, max_length=100, examples=["John Doe"])
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, max_length=128, examples=["securepass123"])


class LoginRequest(BaseModel):

    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["securepass123"])


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Token expiry in minutes")

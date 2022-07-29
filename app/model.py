from pydantic import BaseModel, Field, EmailStr

class AlertSchema(BaseModel):
    alert_id: int = Field(default=None, title="The id of the alert")
    status: str = Field(default="", title="The status of the alert: created/deleted/triggered")
    targetPrice: float = Field(gt=0, title="The target price at which the alert will get triggered")
    class Config:
        schema_extra = {
                "example": {
                    "status": "created",
                    "targetPrice": 24000.78
                    }
                }

class UserSchema(BaseModel):
    username: str
    email: EmailStr 
    password: str 
    class Config:
        schema_extra = {
            "example": {
                "username": "Arjun Somvanshi",
                "email": "arjunsomvanshi@gmail.com",
                "password": "usuallyStrongPassword"
            }
        }
class LoginSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "arjunsomvanshi@gmail.com",
                "password": "usuallyStrongPassword"
            }
        }
    

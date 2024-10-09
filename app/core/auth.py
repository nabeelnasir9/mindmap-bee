from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from jose import JWTError

# Define HTTPBearer scheme for token-based authentication
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    try:
        # Extract token from credentials and decode the JWT
        token = credentials.credentials
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user_id  # You can return a more complete user object if desired
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired")

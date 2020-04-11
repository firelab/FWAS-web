from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from starlette.status import HTTP_401_UNAUTHORIZED

from fwas.auth import get_user_id_from_token
from fwas.crud import get_user
from fwas.database import Database, database
from fwas.serialize import UserInDb

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token",)


async def get_db():
    yield database


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Database = Depends(get_db),
) -> UserInDb:

    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    user_id = get_user_id_from_token(token)
    user = await get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid user token."
        )

    return user

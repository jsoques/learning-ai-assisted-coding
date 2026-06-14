from __future__ import annotations

import base64
import uuid

from fastapi import Cookie, Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasic, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.framework.auth.jwt import SECRET_KEY, ALGORITHM, decode_token, verify_password
from src.framework.db.models import UserModel
from src.framework.db.session import get_db

basic_scheme = HTTPBasic(auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


def _resolve_user(
    credentials: HTTPAuthorizationCredentials | None,
    basic_creds: HTTPAuthorizationCredentials | None,
    db: Session,
) -> UserModel | None:
    if credentials:
        payload = decode_token(credentials.credentials)
        if payload and payload.get("type") == "access":
            user = db.query(UserModel).filter(UserModel.id == payload.get("sub")).first()
            if user:
                return user
    if basic_creds:
        user = db.query(UserModel).filter(UserModel.email == basic_creds.username).first()
        if user and verify_password(basic_creds.password, user.hashed_password):
            return user
    return None


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    basic_creds: HTTPAuthorizationCredentials | None = Depends(basic_scheme),
    db: Session = Depends(get_db),
) -> UserModel:
    user = _resolve_user(credentials, basic_creds, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated",
                            headers={"WWW-Authenticate": "Basic"})
    return user


def require_admin(user: UserModel = Depends(get_current_user)) -> UserModel:
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


def optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    basic_creds: HTTPAuthorizationCredentials | None = Depends(basic_scheme),
    db: Session = Depends(get_db),
) -> UserModel | None:
    return _resolve_user(credentials, basic_creds, db)

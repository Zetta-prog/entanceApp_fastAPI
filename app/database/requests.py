from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from dotenv import load_dotenv

import hashlib
import os


load_dotenv()
path = os.getenv('DB_PATH')

engine = create_async_engine(path)
async_session = async_sessionmaker(bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    username: Mapped[str] = mapped_column(unique=True, primary_key=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def add_user(username: str, password: str, email: str):
    hashed_form_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    async with async_session() as session:
        data = await session.get(User, username)
        if data:
            return {'registration':False, 'error':'was_registered'}
        else:
            try:
                user = User(username=username, password=hashed_form_pass, email=email)
                session.add(user)
                await session.commit()
                return {'registration':True}
            except Exception:
                return {'registration':False, 'error':'email'}

async def chek_user(username: str, password: str):
    hashed_form_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    async with async_session() as session:
        data = await session.get(User, username)
        if data and data.password == hashed_form_pass:
            return {'login':True}
        else:
            return {'login':False}

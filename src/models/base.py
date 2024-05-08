from typing import Any
from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declared_attr, DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(self) -> str:
        """
        Define the table name for the SQLAlchemy model.
        :return: A string representing the table name.
        :rtype: str
        """
        return self.__name__.lower()

    async def save(self, db_session: AsyncSession):
        """
        Save the current object to the database.

        Args:
            db_session (AsyncSession): The asynchronous database session to use for the save operation.

        Returns:
            None: If the save operation is successful.

        Raises:
            HTTPException: If there is an error during the save operation. The exception will have a status code of 422 and the detail will be the representation of the SQLAlchemyError.

        """
        try:
            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def delete(self, db_session: AsyncSession):
        """
        Delete the current object from the database.

        :param db_session: The async session to use for the deletion.
        :type db_session: AsyncSession
        :raises HTTPException: If there is an error during the deletion.
        :return: None
        """
        try:
            db_session.delete(self)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def update(self, db_session: AsyncSession, **kwargs):
        """
        Update the attributes of the current object with the given keyword arguments.

        Args:
            db_session (AsyncSession): The async session to use for the update operation.
            **kwargs: The keyword arguments representing the attributes to update.

        Raises:
            HTTPException: If there is an error during the update operation. The exception will have a status code of 422 and the detail will be the representation of the SQLAlchemyError.

        Returns:
            None
        """
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)
            await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=repr(ex)
            ) from ex

    async def save_or_update(self, db_session: AsyncSession):
        """
        Save or update the current object in the database session.

        Args:
            self: The current object.
            db_session (AsyncSession): The asynchronous database session to use for saving or updating.

        Returns:
            None if the save or update operation is successful.

        Raises:
            IntegrityError: If there is an integrity error during the save or update operation, specifically if there is a UniqueViolationError.
            HTTPException: If there is an error during the save or update operation. The exception will have a status code of 422 and the detail will be the representation of the encountered exception.
        """
        try:
            db_session.add(self)
            return await db_session.commit()
        except IntegrityError as exception:
            if isinstance(exception.orig, UniqueViolationError):
                return await db_session.merge(self)
            else:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=repr(exception),
                ) from exception
        finally:
            await db_session.close()

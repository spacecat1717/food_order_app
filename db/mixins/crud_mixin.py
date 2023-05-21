from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDMixin(object):
    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """
        Create operation for each model

        :param session: DB async session instance
        :param kwargs: model fields
        :return: instance of the model
        """
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    @classmethod
    async def get_by_id(cls, session: AsyncSession, identifier: int):
        """
        Get object by its ID
        :param session: DB async session instance
        :param identifier: id of the model to get
        :return: instance of the model
        """
        return await session.get(cls, identifier)

    @classmethod
    async def get_by_name(cls, session: AsyncSession, name: str):
        """
        Get model by its name
        :param session: DB async session instance
        :param name: model's name(str)
        :return: instance of the model
        """
        query = select(cls).where(cls.name == name)
        result = await session.execute(query)
        return result.scalars().first()

    async def update(self, session: AsyncSession, **kwargs):
        """

        :param session: DB async session instance
        :param kwargs: model fields
        :return: None
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        await session.commit()

    async def delete(self, session: AsyncSession):
        """

        :param session: DB async session instance
        :return: None
        """
        await session.delete(self)
        await session.commit()

    @classmethod
    async def get_all(cls, session: AsyncSession):
        """

        :param session:  DB async session instance
        :return: queryset (all models)
        """
        query = select(cls)
        result = await session.execute(query)
        return result.unique().scalars().all()

from domain.repositories.user.user_repository import UserRepository

class GetUserByUserIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def call(self, user_id: str) -> dict:
        try:
            user = await self.user_repository.get_user_by_user_id(user_id)


            if user.is_success():
                return user.result_value()
            
            return None

        except ValueError as e:
            return None
        except Exception as e:
            return None
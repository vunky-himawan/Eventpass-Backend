from domain.repositories.user.user_repository import UserRepository

class GetUserByUsernameUseCase:
    def __init__(self,
                 user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def call(self, username: str) -> dict:
        try:
            user = await self.user_repository.get_user_by_username(username)

            if user.is_success():
                return user.result_value()
            
            return None

        except ValueError as e:
            print(f"ValueError: {e}")
        except Exception as e:
            print(f"Exception: {e}")
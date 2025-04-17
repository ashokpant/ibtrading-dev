from typing import Optional
from ibtrading.repo.user_repo import UserRepository
from ibtrading.model.user_model import UserModel

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, username: str)-> Optional[UserModel]:
        return self.user_repo.get_by_username(username)

    def create_user(self, username:str, full_name:str, role:str, hashed_password:str):
        user = UserModel(
            username=username,
            full_name=full_name,
            role=role,
            hashed_password=hashed_password
        )
        return self.user_repo.create_user(user)

    def update_user(self, user: UserModel) -> Optional[UserModel]:
        return self.user_repo.update_user(user)

    def delete_user(self, user: UserModel) -> bool:
        return self.user_repo.delete(user)

    def list_users(self) -> list[UserModel]:
        return self.user_repo.list_all()
    
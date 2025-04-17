# test_auth_user_service.py
from ibtrading.repo.datasource import DataSource
from ibtrading.repo.user_repo import UserRepository
from ibtrading.service.user_service import UserService
from ibtrading.service.auth_service import AuthService

# Setup DB and services
db = DataSource().get_session()
user_service = UserService(UserRepository(db))
auth_service = AuthService()

# 🔐 Create a test user
new_user = user_service.create_user(
    username="djdipesh",
    full_name="Dipesh Ghimire",
    role="admin",
    hashed_password=auth_service.hash_password("dipesh123")
)
print("User created:", new_user)

# 🔑 Try login via AuthService
login_response = auth_service.login("djdipesh", "dipesh123")
print("Login success:", login_response.session.access_token if not login_response.error else login_response.message)

# 🔎 Retrieve existing user
user = user_service.get_user("djdipesh")
print("User fetched:", user)

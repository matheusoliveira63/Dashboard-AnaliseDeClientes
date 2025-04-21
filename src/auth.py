from flask_login import UserMixin, LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Configuração segura com fallback
users = {}
try:
    username = os.getenv('USER_LOGIN', 'admin')  # Valor padrão 'admin' se não existir
    password = os.getenv('USER_PASSWORD', 'admin123')  # Valor padrão 'admin123'
    users[username] = {'password': password}
except Exception as e:
    print(f"Erro ao carregar credenciais: {str(e)}")
    # Fallback básico para desenvolvimento
    users['admin'] = {'password': 'admin123'}

def init_auth(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return User(user_id)
        return None
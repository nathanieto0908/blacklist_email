class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///blacklist.db'  # Cambiar a RDS en despliegue
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'static-secret-key'
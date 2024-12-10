import configparser

class Config:
 #   def __init__(self):
 #       self.config = configparser.ConfigParser()
 #       self.config.read('config.properties')

    def __init__(self, database_provider):
        self.config = configparser.ConfigParser()
        self.config.read('config.properties')
        self.database_provider = database_provider

    def get_property(self, property_name):
        try:
            return self.config.get('sqlite', property_name)
        except configparser.NoOptionError:
            print(f"Error: Option '{property_name}' not found in section 'DEFAULT'.")
            return None
        
    @property
    def api_key(self):
        return self.get_property('api.key')
    
    @property
    def database_name(self):
        if self.database_provider == 'sqlite':
            return self.get_property('database.name')
        elif self.database_provider == 'postgresql':
            return self.config.get('postgresql', 'database.name')
        elif self.database_provider == 'mysql':
            return self.config.get('mysql', 'database.name')
        elif self.database_provider == 'oracle':
            return self.config.get('oracle', 'database.service_name')
        
    @property
    def postgresql_config(self):
        if self.database_type == 'postgresql':
            return {
                'host': self.config.get('postgresql', 'database.host'),
                'port': self.config.get('postgresql', 'database.port'),
                'username': self.config.get('postgresql', 'database.username'),
                'password': self.config.get('postgresql', 'database.password'),
                'database': self.config.get('postgresql', 'database.name')
            }
        else:
            return None

    @property
    def mysql_config(self):
        if self.database_type == 'mysql':
            return {
                'host': self.config.get('mysql', 'database.host'),
                'port': self.config.get('mysql', 'database.port'),
                'username': self.config.get('mysql', 'database.username'),
                'password': self.config.get('mysql', 'database.password'),
                'database': self.config.get('mysql', 'database.name')
            }
        else:
            return None

    @property
    def oracle_config(self):
        if self.database_type == 'oracle':
            return {
                'host': self.config.get('oracle', 'database.host'),
                'port': self.config.get('oracle', 'database.port'),
                'username': self.config.get('oracle', 'database.username'),
                'password': self.config.get('oracle', 'database.password'),
                'sid': self.config.get('oracle', 'database.sid'),
                'service_name': self.config.get('oracle', 'database.service_name')
            }
        else:
            return None
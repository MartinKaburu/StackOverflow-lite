'''Drop database module
'''
from app import CONNECTION

cursor = CONNECTION.cursor()
sql = 'DROP DATABASE %s;'
cursor.execute(sql,APP.config['DATABASE_NAME'])
CONNECTION.commit()
cursor.close()

from database.models import bot_users, db, meetings

db.create_tables([bot_users, meetings])

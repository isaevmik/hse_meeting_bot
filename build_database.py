from database.models import db, bot_users, meetings

db.create_tables([bot_users, meetings])

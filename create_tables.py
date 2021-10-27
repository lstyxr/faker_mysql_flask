from my_faker import db

# 在 db.create_all 之间要有导入数据模型类，这样才能建立这些表
from my_faker.models import Plan, SubPlan, User

db.create_all()
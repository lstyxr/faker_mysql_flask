from datetime import datetime
from sqlalchemy.orm import backref

from my_faker import db

# 1. 用户表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    hash_password = db.Column(db.String(120), nullable=False)
    plans = db.relationship("Plan", backref="user", lazy="dynamic")  # 与 Plan 类建立关联
    subplans = db.relationship("SubPlan", backref="user", lazy="dynamic")  # 与 SubPlan 类关联，自想


# 2.总计划表
class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_at = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 与用户 user.id 约束
    sub_plans = db.relationship("SubPlan", backref="plan", lazy="dynamic")  # 与子计划类 SubPlan 建立关联

    @property
    def get_subplan_done_count(self):
        return self.sub_plans.filter_by(is_done=True).count()
    
    @property
    def get_all_subplan_count(self):
        return self.sub_plans.count()
    
    @property
    def get_done_percent(self):
        if self.get_all_subplan_count != 0:
            return int(self.get_subplan_done_count / self.get_all_subplan_count) * 100
        else:
            return 0


# 3.子计划表
class SubPlan(db.Model):
    __tablename__ = 'sub_plan'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.now)
    finish_time = db.Column(db.DateTime, default=datetime.now)
    is_done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 与用户 user.id 约束
    plan_id = db.Column(db.Integer, db.ForeignKey("plan.id"))  # 与总计划 plan.id 约束

    # 关联删除
    # plan = db.relationship('Plan', cascade='delete', overlaps='sub_plans')

    def change_status(self):
        if self.is_done is True:
            self.is_done = False
        else:
            self.is_done = True
        self.finish_time = datetime.now()
        db.session.add(self)
        db.session.commit()
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask('test_faker')
app.secret_key = 'test_faker'
app.debug = True

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from my_faker import commands


from faker import Faker
from my_faker.models import Plan, SubPlan, User

faker = Faker('zh_CN')

# 外键
# 生成 总 -> 子 计划，注意与 user 表的外键，
# 在 user 表中要有 id=1 的记录才能成功插入记录
# 否则提示：(1452, 'Cannot add or update a child row: a foreign key constraint fails (`faker_test`.`plan`, CONSTRAINT `plan_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`))')
# 提示：通过查看错误信息，我们可以得到，plan 这张表中有个字段 user_id,
# 是以 user 表中的 id 字段为 foreign key(外键)，而我们插入语句的 user_id 值要包含在 user 表中，这样才能成功
# 当一个表中的一个字段，以另一张表的字段为外键，插入数据时相对应的数值必须存在。
def gen_faker_plan(count=10):
    for i in range(count):
        plan = Plan(body=faker.sentence(nb_words=10), user_id=1)
        db.session.add(plan)
        db.session.commit()
        plan_id = plan.id

        for j in range(10):
            subplan = SubPlan(body=faker.text(max_nb_chars=35), plan_id=plan_id, user_id=1)
            db.session.add(subplan)
    
    db.session.commit()

# 自定义命令在 __init__ 中定义
@app.cli.command()
@click.option('--count', default=10, help='创建数量')
def genplan(count):
    click.echo('正在生成中......')
    gen_faker_plan(count)
    click.echo('生成完毕！')
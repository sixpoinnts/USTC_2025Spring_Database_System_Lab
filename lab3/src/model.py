# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 教师
class Teacher(db.Model):
    __tablename__ = 'teacher'

    T_ID = db.Column(db.String(5), primary_key=True)

    T_Name = db.Column(db.String(256))
    T_sexual = db.Column(db.Integer)
    T_type = db.Column(db.Integer)

# 论文
class Paper(db.Model):
    __tablename__ = 'paper'

    P_ID = db.Column(db.Integer, primary_key=True)
    P_Name = db.Column(db.String(256))
    P_Url = db.Column(db.String(256))
    P_Year = db.Column(db.Date)
    P_Type = db.Column(db.Integer)
    P_Level = db.Column(db.Integer)

# 课程
class Class(db.Model):
    __tablename__ = 'class'

    C_ID = db.Column(db.String(256), primary_key=True)
    C_Name = db.Column(db.String(256))
    C_Sum = db.Column(db.Integer)
    C_Type = db.Column(db.Integer)

# 项目
class Project(db.Model):
    __tablename__ = 'project'

    Pr_ID = db.Column(db.String(256), primary_key=True)
    Pr_Name = db.Column(db.String(256))
    Pr_Source = db.Column(db.String(256))
    Pr_Type = db.Column(db.Integer)
    Pr_Summoney = db.Column(db.Float, default=0)
    Pr_From = db.Column(db.Integer)
    Pr_End = db.Column(db.Integer)

# 发表论文
class PublishPaper(db.Model):
    __tablename__ = 'publish_paper'

    P_ID = db.Column(db.ForeignKey('paper.P_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    T_ID = db.Column(db.ForeignKey('teacher.T_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)

    P_Rank = db.Column(db.Integer)  
    P_Contact = db.Column(db.SmallInteger)

# 承担项目
class OwnProject(db.Model):
    __tablename__ = 'own_project'

    Pr_ID = db.Column(db.ForeignKey('project.Pr_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    T_ID = db.Column(db.ForeignKey('teacher.T_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)

    Pr_Rank = db.Column(db.Integer)
    Pr_money = db.Column(db.Float)

# 主讲课程
class TeachClass(db.Model):
    __tablename__ = 'teach_class'

    C_ID = db.Column(db.ForeignKey('class.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    T_ID = db.Column(db.ForeignKey('teacher.T_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)

    C_Year = db.Column(db.Integer)
    C_Semester = db.Column(db.Integer)
    C_hours = db.Column(db.Integer)
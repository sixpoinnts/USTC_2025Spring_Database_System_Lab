from flask import Flask, render_template, request, abort
import config
import numpy as np
import datetime
import sqlalchemy
from db_init import db, db2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from model import Teacher, Paper, Class, Project, PublishPaper, OwnProject, TeachClass
import time
import pdfkit
from flask import send_file, make_response

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

cursor = db2.cursor()

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

# 教师管理
@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    labels = ['工号', '姓名', '性别', '职称']
    result_query = db.session.query(Teacher)
    result = result_query.all()

    # 定义性别映射关系
    gender_mapping = {
        1: '男',
        2: '女'
    }

    # 定义职称映射关系
    Type_mapping = {
        1: '博士后',
        2: '助教',
        3: '讲师',
        4: '副教授',
        5: '特任教授',
        6: '教授',
        7: '助理研究员',
        8: '特任副研究员',
        9: '副研究员',
        10: '特任研究员',
        11: '研究员'
    }

    # 定义一个函数来转换性别数字为文字
    def format_teacher_data(teachers):
        formatted = []
        for t in teachers:
            gender = gender_mapping.get(t.T_sexual, '未知')
            Type = Type_mapping.get(t.T_type, '未知')
            formatted.append({
                'T_ID': t.T_ID,
                'T_Name': t.T_Name,
                'T_sexual': gender,
                'T_type': Type
            })
        return formatted

    formatted_result = format_teacher_data(result)

    if request.method == 'GET':
        return render_template('teacher.html', labels=labels, content=formatted_result)
    else:
        if request.form.get('type') == 'query':
            teacher_id = request.form.get('id')
            teacher_name = request.form.get('name')
            teacher_sexual = request.form.get('sexual')
            teacher_type = request.form.get('t_type')

            if teacher_id != "":
                result_query = result_query.filter(Teacher.T_ID == teacher_id)
            if teacher_name != "":
                result_query = result_query.filter(Teacher.T_Name == teacher_name)
            if teacher_sexual != "":
                result_query = result_query.filter(Teacher.T_sexual == teacher_sexual)
            if teacher_type != "":
                result_query = result_query.filter(Teacher.T_type == teacher_type)

            result = result_query.all()
            # return render_template('teacher.html', labels=labels, content=result)
            formatted_result = format_teacher_data(result)
            return render_template('teacher.html', labels=labels, content=formatted_result)

        elif request.form.get('type') == 'update':
            old_num = request.form.get('key')
            teacher_name = request.form.get('teacher_name')
            teacher_sexual = request.form.get('teacher_sexual')
            teacher_type = request.form.get('teacher_type')
            teacher_result = db.session.query(Teacher).filter_by(T_ID=old_num).first()
            teacher_result.T_Name = teacher_name
            teacher_result.T_sexual = teacher_sexual
            teacher_result.T_type = teacher_type
            db.session.commit()

        elif request.form.get('type') == 'delete':
            old_num = request.form.get('key')

            teacherNotExist = db.session.query(PublishPaper).filter_by(T_ID=old_num).scalar() is None
            if teacherNotExist != 1:
                error_title = '删除错误'
                error_message = '教师在存在关联论文'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            teacherNotExist = db.session.query(OwnProject).filter_by(T_ID=old_num).scalar() is None
            if teacherNotExist != 1:
                error_title = '删除错误'
                error_message = '教师在存在关联项目'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            teacherNotExist = db.session.query(TeachClass).filter_by(T_ID=old_num).scalar() is None
            if teacherNotExist != 1:
                error_title = '删除错误'
                error_message = '教师在存在主讲课程'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            teacher_result = db.session.query(Teacher).filter_by(T_ID=old_num).first()
            db.session.delete(teacher_result)
            db.session.commit()

        elif request.form.get('type') == 'insert':
            teacher_id = request.form.get('id')
            teacher_name = request.form.get('name')
            teacher_sexual = request.form.get('sexual')
            teacher_type = request.form.get('t_type')

            newteacher = Teacher(
                T_ID=teacher_id,
                T_Name=teacher_name,
                T_sexual=teacher_sexual,
                T_type=teacher_type
            )

            db.session.add(newteacher)
            db.session.commit()

    result = db.session.query(Teacher).all()

    # return render_template('teacher.html', labels=labels, content=result)
    formatted_result = format_teacher_data(result)
    return render_template('teacher.html', labels=labels, content=formatted_result)

# 论文
@app.route('/paper', methods=['GET', 'POST'])
def paper():
    labels1 = ['序号', '论文名称', '发表源', '发表年份', '类型', '级别']
    labels2 = ['序号', '作者ID', '排名', '是否通讯作者']
    result_query1 = db.session.query(Paper)
    result_query2 = db.session.query(Paper, PublishPaper).filter(Paper.P_ID == PublishPaper.P_ID)
    result1 = result_query1.all()
    result2 = result_query2.all()

    # 定义论文类型映射关系
    Type_mapping = {
        1: 'full paper',
        2: 'short paper',
        3: 'poster paper',
        4: 'semo paper'
    }

    # 定义论文级别映射关系
    Level_mapping = {
        1: 'CCF-A',
        2: 'CCF-B',
        3: 'CCF-C',
        4: '中文 CCF-A',
        5: '中文 CCF-B',
        6: '无级别'
    }

    # 定义是否为通讯作者映射关系
    contact_mapping = {
        0: '否',
        1: '是'
    }

    def format_paper_data(papers):
        formatted = []
        for p in papers:
            Type = Type_mapping.get(p.P_Type, '未知')
            Level = Level_mapping.get(p.P_Level, '未知')
            formatted.append({
                'P_ID': p.P_ID,
                'P_Name': p.P_Name,
                'P_Url': p.P_Url,
                'P_Year':p.P_Year,
                'P_Type':Type,
                'P_Level':Level
            })
        return formatted
    
    def format_publishpaper_data(publishpapers):
        formatted = []
        for p in publishpapers:
            contact = contact_mapping.get(p.PublishPaper.P_Contact, '未知')
            formatted.append({
                'P_ID': p.PublishPaper.P_ID,
                'T_ID': p.PublishPaper.T_ID,
                'P_Rank': p.PublishPaper.P_Rank,
                'P_Contact':contact
            })
        return formatted

    formatted_result1 = format_paper_data(result1)
    formatted_result2 = format_publishpaper_data(result2)

    if request.method == 'GET':
        # return render_template('paper.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
        return render_template('paper.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)
    else:
        if request.form.get('type') == 'query1':
            paperId = request.form.get('paperId')
            paperName = request.form.get('name')
            paperUrl = request.form.get('url')
            paperYear = request.form.get('year')
            paperType = request.form.get('p_type')
            paperLevel = request.form.get('level')

            if paperId != '':
                result_query1 = result_query1.filter(Paper.P_ID == paperId)
            if paperName != '':
                result_query1 = result_query1.filter(Paper.P_Name == paperName)
            if paperUrl != '':
                result_query1 = result_query1.filter(Paper.P_Url == paperUrl)
            if paperYear:
                result_query1 = result_query1.filter(Paper.P_Year == paperYear)
            if paperType:
                result_query1 = result_query1.filter(Paper.P_Type == paperType)
            if paperLevel:
                result_query1 = result_query1.filter(Paper.P_Level == paperLevel)

            result1 = result_query1.all()
            # return render_template('paper.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result1 = format_paper_data(result1)
            formatted_result2 = format_publishpaper_data(result2)
            return render_template('paper.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

        elif request.form.get('type') == 'query2':
            paperId = request.form.get('paperId')
            teacherId = request.form.get('teacherId')
            rank = request.form.get('rank')
            is_contact = request.form.get('is_contact')

            if paperId != '':
                result_query2 = result_query2.filter(PublishPaper.P_ID== paperId)
            if teacherId != '':
                result_query2 = result_query2.filter(PublishPaper.T_ID == teacherId)
            if rank:
                result_query2 = result_query2.filter(PublishPaper.P_Rank == rank)
            if is_contact:
                result_query2 = result_query2.filter(PublishPaper.P_Contact == is_contact)

            result2 = result_query2.all()
            # return render_template('paper.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result1 = format_paper_data(result1)
            formatted_result2 = format_publishpaper_data(result2)
            return render_template('paper.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)


        elif request.form.get('type') == 'update1':
            paperId = request.form.get('key')
            paperName = request.form.get('name')
            paperUrl = request.form.get('url')
            paperYear = request.form.get('year')
            paperType = request.form.get('p_type')
            paperLevel = request.form.get('level')
            Paper_result = db.session.query(Paper).filter_by(P_ID=paperId).first()
            Paper_result.P_Name = paperName
            Paper_result.P_Url = paperUrl
            Paper_result.P_Year = paperYear
            Paper_result.P_Type = paperType
            Paper_result.P_Level = paperLevel
            db.session.commit()

        elif request.form.get('type') == 'update2':
            paperId = request.form.get('key')
            teacherId = request.form.get('teacherId')
            rank = request.form.get('rank')
            is_contact = request.form.get('is_contact')

            # 检查同一论文下是否存在相同排名（排除当前记录自身）
            same_rank = db.session.query(PublishPaper).filter(
                PublishPaper.P_ID == paperId,
                PublishPaper.P_Rank == rank,
                PublishPaper.P_ID != paperId  # 排除当前记录（更新时）
            ).first()

            if same_rank:
                return render_template('404.html', error_message='同一论文中排名不能重复！')
            
           # 2. 验证通讯作者唯一性
            if is_contact == '1' and PublishPaper.P_Contact != '1':
                # 如果从非通讯作者改为通讯作者，检查是否已有通讯作者
                has_contact = db.session.query(PublishPaper).filter(
                    PublishPaper.P_ID == paperId,
                    PublishPaper.P_Contact == 1,
                    PublishPaper.id != PublishPaper.id  # 排除当前记录
                ).first()
                if has_contact:
                    return render_template('error.html', error_message='一篇论文只能有一位通讯作者！')

            PublishPaper_result = db.session.query(PublishPaper).filter_by(P_ID=paperId).first()
            PublishPaper_result.T_ID = teacherId
            PublishPaper_result.P_Rank = rank
            PublishPaper_result.P_Contact = is_contact

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            paperId = request.form.get('key')
            paper_result = db.session.query(Paper).filter_by(P_ID=paperId).first()
            publishpaper_result = db.session.query(PublishPaper).filter_by(P_ID=paperId).first()

            publishpaperNotExist = db.session.query(PublishPaper).filter_by(P_ID=paperId).scalar() is None

            if publishpaperNotExist != 1:
                db.session.delete(publishpaper_result)
                db.session.commit()

            db.session.delete(paper_result)
            db.session.commit()

        elif request.form.get('type') == 'delete2':
            paperId = request.form.get('key')
            publishpaper_result = db.session.query(PublishPaper).filter_by(P_ID=paperId).first()

            db.session.delete(publishpaper_result)
            db.session.commit()

        elif request.form.get('type') == 'insert2':
            paperId = request.form.get('paperId')
            teacherId = request.form.get('teacherId')
            rank = request.form.get('rank')
            is_contact = request.form.get('is_contact')

            # 1. 验证排名唯一性
            existing_rank = db.session.query(PublishPaper).filter(
                PublishPaper.P_ID == paperId,
                PublishPaper.P_Rank == rank
            ).first()

            if existing_rank:
                return render_template('404.html', message='同一论文中排名不能重复！')
            
            # 2. 验证通讯作者唯一性
            if is_contact == '1':
                has_contact = db.session.query(PublishPaper).filter(
                    PublishPaper.P_ID == paperId,
                    PublishPaper.P_Contact == 1
                ).first()
                if has_contact:
                    return render_template('404.html', message='一篇论文只能有一位通讯作者！')
                
            newPublishPaper = PublishPaper(
                P_ID=paperId,
                T_ID=teacherId,
                P_Rank=rank,
                P_Contact = is_contact
            )

            db.session.add(newPublishPaper)
            db.session.commit()

            result2 = db.session.query(Paper, PublishPaper).filter(Paper.P_ID == PublishPaper.P_ID).all()
            # return render_template('paper.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result1 = format_paper_data(result1)
            formatted_result2 = format_publishpaper_data(result2)
            return render_template('paper.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

        elif request.form.get('type') == 'insert1':
            paperId = request.form.get('paperId')
            paperName = request.form.get('name')
            paperUrl = request.form.get('url')
            paperYear = request.form.get('year')
            paperType = request.form.get('p_type')
            paperLevel = request.form.get('level')

            newPaper = Paper(
                P_ID=paperId,
                P_Name=paperName,
                P_Url=paperUrl,
                P_Year=paperYear,
                P_Type=paperType,
                P_Level=paperType
            )

            db.session.add(newPaper)
            db.session.commit()

    result1 = db.session.query(Paper).all()
    formatted_result1 = format_paper_data(result1)
    formatted_result2 = format_publishpaper_data(result2)
    return render_template('paper.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

# 项目
@app.route('/project', methods=['GET', 'POST'])
def project():
    labels1 = ['项目号', '项目名称', '项目来源',  '项目类型', '总经费', '开始年份', '结束年份']
    labels2 = ['项目号', '教师ID', '排名', '承担经费']
    result_query1 = db.session.query(Project)
    result_query2 = db.session.query(Project,OwnProject).filter(Project.Pr_ID == OwnProject.Pr_ID)
    result1 = result_query1.all()
    result2 = result_query2.all()

    # 定义项目类型映射关系
    Type_mapping = {
        1: '国家级项目',
        2: '省部级项目',
        3: '市厅级项目',
        4: '企业合作级项目',
        5: '其他类型项目'
    }

    def format_Project_data(projects):
        formatted = []
        for p in projects:
            Type = Type_mapping.get(p.Pr_Type, '未知')
            formatted.append({
                'Pr_ID': p.Pr_ID,
                'Pr_Name': p.Pr_Name,
                'Pr_Source': p.Pr_Source,
                'Pr_Type': Type,
                'Pr_Summoney': p.Pr_Summoney,
                'Pr_From': p.Pr_From,
                'Pr_End': p.Pr_End
            })
        return formatted

    formatted_result = format_Project_data(result1)

    if request.method == 'GET':
        # return render_template('project.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
        return render_template('project.html', labels1=labels1, labels2=labels2, content1=formatted_result, content2=result2)
    else:
        # 查询
        if request.form.get('type') == 'query1':
            projectId = request.form.get('projectId')
            projectName = request.form.get('name')
            projectSource = request.form.get('source')
            projectSum = request.form.get('Summoney')
            projectFrom = request.form.get('beginyear')
            projectEnd = request.form.get('endyear')
            projectType = request.form.get('Type')

            if projectId != '':
                result_query1 = result_query1.filter(Project.Pr_ID == projectId)
            if projectName != '':
                result_query1 = result_query1.filter(Project.Pr_Name == projectName)
            if projectSource != '':
                result_query1 = result_query1.filter(Project.Pr_Source == projectSource)
            if projectSum != '':
                result_query1 = result_query1.filter(Project.Pr_Summoney == projectSum)
            if projectFrom != '':
                result_query1 = result_query1.filter(Project.Pr_From == projectFrom)
            if projectEnd != '':
                result_query1 = result_query1.filter(Project.Pr_End == projectEnd)
            if projectType != '':
                result_query1 = result_query1.filter(Project.Pr_Type == projectType)

            result1 = result_query1.all()
            # return render_template('project.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result = format_Project_data(result1)
            return render_template('project.html', labels1=labels1, labels2=labels2, content1=formatted_result, content2=result2)

        elif request.form.get('type') == 'query2':
            projectId = request.form.get('projectId')
            teacherId = request.form.get('teacherId')
            rank = request.form.get('rank')
            money = request.form.get('money')

            if projectId != '':
                result_query2 = result_query2.filter(OwnProject.Pr_ID== projectId)
            if teacherId != '':
                result_query2 = result_query2.filter(OwnProject.T_ID == teacherId)
            if rank != '':
                result_query2 = result_query2.filter(OwnProject.Pr_Rank == rank)
            if money != '':
                result_query2 = result_query2.filter(OwnProject.Pr_money == money)

            result2 = result_query2.all()
            # return render_template('project.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result = format_Project_data(result1)
            return render_template('project.html', labels1=labels1, labels2=labels2, content1=formatted_result, content2=result2)

        elif request.form.get('type') == 'update1':
            projectId = request.form.get('key')
            projectName = request.form.get('name')
            projectSource = request.form.get('source')
            projectFrom = request.form.get('beginyear')
            projectEnd = request.form.get('endyear')
            projectType = request.form.get('Type')

            Project_result = db.session.query(Project).filter_by(Pr_ID=projectId).first()
            Project_result.Pr_Name = projectName
            Project_result.Pr_Source = projectSource
            Project_result.Pr_From = projectFrom
            Project_result.Pr_End = projectEnd
            Project_result.Pr_Type = projectType
            db.session.commit()

        elif request.form.get('type') == 'update2':
            projectId = request.form.get('key')
            teacherId = request.form.get('teacherId')
            rank = request.form.get('rank')
            money = request.form.get('money')

            # 检查同一项目下是否存在相同排名（排除当前记录自身）
            same_rank = db.session.query(OwnProject).filter(
                OwnProject.Pr_ID == projectId,
                OwnProject.Pr_Rank == rank,
                OwnProject.Pr_ID != projectId  # 排除当前记录（更新时）
            ).first()

            if same_rank:
                return render_template('404.html', error_message='同一论文中排名不能重复！')
            
            # 更新总经费 
            oldmoney = db.session.query(OwnProject).filter_by(Pr_ID=projectId).first().Pr_money
            projectSum = db.session.query(Project).filter_by(Pr_ID=projectId).first().Pr_Summoney
            projectSum = projectSum + float(money) - oldmoney

            Project_result = db.session.query(Project).filter_by(Pr_ID=projectId).first()
            Project_result.Pr_Summoney = projectSum

            OwnProject_result = db.session.query(OwnProject).filter_by(Pr_ID=projectId).first()
            OwnProject_result.T_ID = teacherId
            OwnProject_result.Pr_Rank = rank
            OwnProject_result.Pr_money = money

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            projectId = request.form.get('key')
            project_result = db.session.query(Project).filter_by(Pr_ID=projectId).first()
            ownproject_result = db.session.query(OwnProject).filter_by(Pr_ID=projectId).first()

            ownprojectNotExist = db.session.query(OwnProject).filter_by(Pr_ID=projectId).scalar() is None

            if ownprojectNotExist != 1:
                db.session.delete(ownproject_result)
                db.session.commit()

            db.session.delete(project_result)
            db.session.commit()

        elif request.form.get('type') == 'delete2':
            projectId = request.form.get('key')
            ownproject_result = db.session.query(OwnProject).filter_by(Pr_ID=projectId).first()

            # 删除时更新总经费
            projectSum = db.session.query(Project).filter_by(Pr_ID=projectId).first().Pr_Summoney
            money = db.session.query(OwnProject).filter_by(Pr_ID=projectId).first().Pr_money
            projectSum = projectSum - money
            Project_result = db.session.query(Project).filter_by(Pr_ID=projectId).first()
            Project_result.Pr_Summoney = projectSum

            db.session.delete(ownproject_result)
            db.session.commit()

        elif request.form.get('type') == 'insert2':
            projectId = request.form.get('projectId')
            teacherId = request.form.get('teacherId')
            rank = request.form.get('rank')
            money = request.form.get('money')

            # 1. 验证排名唯一性
            existing_rank = db.session.query(OwnProject).filter(
                OwnProject.Pr_ID == projectId,
                OwnProject.Pr_Rank == rank
            ).first()

            if existing_rank:
                error_title = '更新错误'
                error_message = '排名不能相同'
                return render_template('404.html', error_title=error_title, error_message=error_message)
            
            # # 2. 将项目经费添加到经费总额
            projectSum = db.session.query(Project).filter_by(Pr_ID=projectId).first().Pr_Summoney
            projectSum = projectSum + float(money)
            Project_result = db.session.query(Project).filter_by(Pr_ID=projectId).first()
            Project_result.Pr_Summoney = projectSum

            newOwnProject = OwnProject(
                Pr_ID=projectId,
                T_ID=teacherId,
                Pr_Rank=rank,
                Pr_money = money
            )

            db.session.add(newOwnProject)
            db.session.commit()

            result2 = db.session.query(Project, OwnProject).filter(Project.Pr_ID == OwnProject.Pr_ID).all()
            # return render_template('project.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result = format_Project_data(result1)
            return render_template('project.html', labels1=labels1, labels2=labels2, content1=formatted_result, content2=result2)

        elif request.form.get('type') == 'insert1':
            projectId = request.form.get('projectId')
            projectName = request.form.get('name')
            projectSource = request.form.get('source')
            projectFrom = request.form.get('beginyear')
            projectEnd = request.form.get('endyear')
            projectType = request.form.get('Type')

            newProject = Project(
                Pr_ID=projectId,
                Pr_Name=projectName,
                Pr_Source=projectSource,
                Pr_Type=projectType,
                Pr_From=projectFrom,
                Pr_End=projectEnd
            )

            db.session.add(newProject)
            db.session.commit()

    result1 = db.session.query(Project).all()
    # return render_template('project.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
    formatted_result = format_Project_data(result1)
    return render_template('project.html', labels1=labels1, labels2=labels2, content1=formatted_result, content2=result2)

# 课程
@app.route('/class', methods=['GET', 'POST'])
def classes():
    labels1 = ['课程号', '课程名称', '学时数',  '课程性质']
    labels2 = ['课程号', '教师ID', '年份', '学期', '承担学时']
    result_query1 = db.session.query(Class)
    result_query2 = db.session.query(Class,TeachClass).filter(Class.C_ID == TeachClass.C_ID)
    result1 = result_query1.all()
    result2 = result_query2.all()

    # 定义课程性质映射关系
    Type_mapping = {
        1: '本科生课程',
        2: '研究生课程'
    }

    # 定义学期映射关系
    semester_mapping = {
        1: '春季学期',
        2: '夏季学期',
        3: '秋季学期'
    }

    def format_class_data(classes):
        formatted = []
        for c in classes:
            Type = Type_mapping.get(c.C_Type, '未知')
            formatted.append({
                'C_ID': c.C_ID,
                'C_Name': c.C_Name,
                'C_Sum': c.C_Sum,
                'C_Type':Type
            })
        return formatted
    
    def format_teachclass_data(teachclasses):
        formatted = []
        for c in teachclasses:
            semester = semester_mapping.get(c.TeachClass.C_Semester, '未知')
            formatted.append({
                'C_ID': c.TeachClass.C_ID,
                'T_ID': c.TeachClass.T_ID,  
                'C_Year': c.TeachClass.C_Year,
                'C_Semester': semester,
                'C_hours': c.TeachClass.C_hours
            })
        return formatted

    formatted_result1 = format_class_data(result1)
    formatted_result2 = format_teachclass_data(result2)

    if request.method == 'GET':
        return render_template('class.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

    else:
        if request.form.get('type') == 'query1':
            classId = request.form.get('classId')
            className = request.form.get('name')
            classSum = request.form.get('sumhours')
            classType = request.form.get('Type')

            if classId != '':
                result_query1 = result_query1.filter(Class.C_ID == classId)
            if className != '':
                result_query1 = result_query1.filter(Class.C_Name == className)
            if classSum != '':
                result_query1 = result_query1.filter(Class.C_Sum == classSum)
            if classType != '':
                result_query1 = result_query1.filter(Class.C_Type == classType)

            result1 = result_query1.all()
            formatted_result1 = format_class_data(result1)
            formatted_result2 = format_teachclass_data(result2)
            return render_template('class.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

        elif request.form.get('type') == 'query2':
            classId = request.form.get('classId')
            teacherId = request.form.get('teacherId')
            year = request.form.get('year')
            semester = request.form.get('semester')
            hours = request.form.get('hours')

            if classId != '':
                result_query2 = result_query2.filter(TeachClass.C_ID== classId)
            if teacherId != '':
                result_query2 = result_query2.filter(TeachClass.T_ID == teacherId)
            if year != '':
                result_query2 = result_query2.filter(TeachClass.C_Year == year)
            if semester != '':
                result_query2 = result_query2.filter(TeachClass.C_Semester == semester)
            if hours != '':
                result_query2 = result_query2.filter(TeachClass.C_hours == hours)

            result2 = result_query2.all()
            formatted_result1 = format_class_data(result1)
            formatted_result2 = format_teachclass_data(result2)
            return render_template('class.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

        elif request.form.get('type') == 'update1':
            classId = request.form.get('key')
            className = request.form.get('name')
            classSum = request.form.get('sumhours')
            classType = request.form.get('Type')
            Class_result = db.session.query(Class).filter_by(C_ID=classId).first()
            Class_result.C_Name = className
            Class_result.C_Sum = classSum
            Class_result.C_Type = classType
            db.session.commit()

        elif request.form.get('type') == 'update2':
            classId = request.form.get('key')
            teacherId = request.form.get('teacherId')
            year = request.form.get('year')
            semester = request.form.get('semester')
            hours = request.form.get('hours')
            
            # 一个课程中所有教师主讲课程的总额等于总学时
            course = db.session.query(Class).filter_by(C_ID=classId).first()
            if not course:
                return render_template('404.html', error_message='课程不存在！')
            
            # # 获取当前课程的教师承担学时总额
            # total_assigned_hours = db.session.query(func.sum(TeachClass.C_hours)).filter(
            #     TeachClass.C_ID == classId
            # ).scalar() or 0
            # # 如果当前记录存在，需要减去当前记录的学时
            # current_record = db.session.query(TeachClass).filter_by(C_ID=classId).first()
            # if current_record:
            #     total_assigned_hours -= current_record.C_hours
            # # 加上新的学时值
            # total_assigned_hours += int(hours)
            # if total_assigned_hours != int(course.C_Sum):
            #     return render_template('404.html', error_message=f'教师承担学时总额({total_assigned_hours})不等于课程总学时({course.C_Sum})！')

            # 查询当前记录
            teach_class_record = db.session.query(TeachClass).filter_by(
                C_ID=classId, T_ID=teacherId, C_Year=year, C_Semester=semester
            ).first()
            if not teach_class_record:
                return render_template('404.html', error_message='记录不存在，无法更新！')
            
            # 计算当前学期其他教师已分配的学时（排除当前记录）
            total_assigned_hours = db.session.query(func.sum(TeachClass.C_hours)).filter(
                TeachClass.C_ID == classId,
                TeachClass.C_Year == year,
                TeachClass.C_Semester == semester,
                db.or_(
                    TeachClass.T_ID != teacherId,
                    db.and_(TeachClass.C_Year != year, TeachClass.C_Semester != semester)
                )
            ).scalar() or 0

            total_assigned_hours += int(hours)

            # 判断是否超过每学期的总学时
            # if total_assigned_hours > course.C_Sum:
            if total_assigned_hours != course.C_Sum:
                error_message=f'学期 {year} 第 {semester} 学期教师承担学时总额({total_assigned_hours})多于课程每学期总学时({course.C_Sum})！'
                return render_template('404.html', error_message = error_message)
            
            # 更新TeachClass记录
            TeachClass_result = db.session.query(TeachClass).filter_by(C_ID=classId).first()
            TeachClass_result.T_ID = teacherId
            TeachClass_result.C_Year = year
            TeachClass_result.C_Semester = semester
            TeachClass_result.C_hours = hours

            db.session.commit()

        elif request.form.get('type') == 'delete1':
            classId = request.form.get('key')
            class_result = db.session.query(Class).filter_by(C_ID=classId).first()
            teachclass_result = db.session.query(TeachClass).filter_by(C_ID=classId).first()

            teachclassNotExist = db.session.query(TeachClass).filter_by(C_ID=classId).scalar() is None

            if teachclassNotExist != 1:
                db.session.delete(teachclass_result)
                db.session.commit()

            db.session.delete(class_result)
            db.session.commit()

        elif request.form.get('type') == 'delete2':
            classId = request.form.get('key')
            teachclass_result = db.session.query(TeachClass).filter_by(C_ID=classId).first()

            db.session.delete(teachclass_result)
            db.session.commit()

        elif request.form.get('type') == 'insert2':
            classId = request.form.get('classId')
            teacherId = request.form.get('teacherId')
            year = request.form.get('year')
            semester = request.form.get('semester')
            hours = request.form.get('hours')

            # # 验证一门课程中所有教师主讲学时总额等于课程总学时
            course = db.session.query(Class).filter_by(C_ID=classId).first()
            if not course:
                return render_template('404.html', error_message='课程不存在！')
            
            # total_assigned_hours = db.session.query(func.sum(TeachClass.C_hours)).filter(
            #     TeachClass.C_ID == classId
            # ).scalar() or 0
            # total_assigned_hours += float(hours)
            # if total_assigned_hours != float(course.C_Sum):
            #     return render_template('404.html', message=f'教师承担学时总额({total_assigned_hours})不等于课程总学时({course.C_Sum})！')
            
            # 计算当前学期已分配的学时
            total_assigned_hours = db.session.query(func.sum(TeachClass.C_hours)).filter(
                TeachClass.C_ID == classId,
                TeachClass.C_Year == year,
                TeachClass.C_Semester == semester
            ).scalar() or 0

            total_assigned_hours += int(hours)

            # 判断是否超过每学期的总学时
            # if total_assigned_hours > course.C_Sum:
            if total_assigned_hours != course.C_Sum:
                error_message=f'学期 {year} 第 {semester} 学期教师承担学时总额({total_assigned_hours})不等于课程每学期总学时({course.C_Sum})！'
                return render_template('404.html', error_message=error_message)

            newTeachClass = TeachClass(
                C_ID=classId,
                T_ID=teacherId,
                C_Year=year,
                C_Semester = semester,
                C_hours = hours
            )

            db.session.add(newTeachClass)
            db.session.commit()

            result2 = db.session.query(Class, TeachClass).filter(Class.C_ID == TeachClass.C_ID).all()
            # return render_template('class.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
            formatted_result1 = format_class_data(result1)
            formatted_result2 = format_teachclass_data(result2)
            return render_template('class.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

        elif request.form.get('type') == 'insert1':
            classId = request.form.get('classId')
            className = request.form.get('name')
            classSum = request.form.get('sumhours')
            classType = request.form.get('Type')

            newClass = Class(
                C_ID=classId,
                C_Name=className,
                C_Sum=classSum,
                C_Type=classType
            )

            db.session.add(newClass)
            db.session.commit()

    result1 = db.session.query(Class).all()
    # return render_template('class.html', labels1=labels1, labels2=labels2, content1=result1, content2=result2)
    formatted_result1 = format_class_data(result1)
    formatted_result2 = format_teachclass_data(result2)
    return render_template('class.html', labels1=labels1, labels2=labels2, content1=formatted_result1, content2=formatted_result2)

# 查询
@app.route('/search', methods=['GET', 'POST'])
def search():
    labels_teacher = ['工号', '姓名', '性别', '职称']
    result_query_teacher = db.session.query(Teacher)
    result_teacher = result_query_teacher.all()

    labels_paper = ['教师ID', '论文名称', '发表源', '发表年份', '类型', '级别','排名', '是否通讯作者']
    result_query_paper = db.session.query(Paper, PublishPaper).filter(Paper.P_ID == PublishPaper.P_ID)
    result_paper = result_query_paper.all()

    labels_project = ['教师ID', '项目名称', '项目来源',  '项目类型', '总经费', '开始年份', '结束年份', '承担经费']
    result_query_project = db.session.query(Project,OwnProject).filter(Project.Pr_ID == OwnProject.Pr_ID)
    result_project = result_query_project.all()

    labels_class = ['课程号', '教师ID', '课程名称', '学时数',  '课程性质', '年份', '学期', '承担学时']
    result_query_class = db.session.query(Class,TeachClass).filter(Class.C_ID == TeachClass.C_ID)
    result_class = result_query_class.all()

    # 定义性别映射关系
    gender_mapping = {
        1: '男',
        2: '女'
    }

    # 定义职称映射关系
    Teacher_Type_mapping = {
        1: '博士后',
        2: '助教',
        3: '讲师',
        4: '副教授',
        5: '特任教授',
        6: '教授',
        7: '助理研究员',
        8: '特任副研究员',
        9: '副研究员',
        10: '特任研究员',
        11: '研究员'
    }

    # 定义论文类型映射关系
    Paper_Type_mapping = {
        1: 'full paper',
        2: 'short paper',
        3: 'poster paper',
        4: 'semo paper'
    }

    # 定义论文级别映射关系
    Level_mapping = {
        1: 'CCF-A',
        2: 'CCF-B',
        3: 'CCF-C',
        4: '中文 CCF-A',
        5: '中文 CCF-B',
        6: '无级别'
    }

    # 定义是否为通讯作者映射关系
    contact_mapping = {
        0: '否',
        1: '是'
    }

    # 定义项目类型映射关系
    Project_Type_mapping = {
        1: '国家级项目',
        2: '省部级项目',
        3: '市厅级项目',
        4: '企业合作级项目',
        5: '其他类型项目'
    }

    # 定义课程性质映射关系
    Class_Type_mapping = {
        1: '本科生课程',
        2: '研究生课程'
    }

    # 定义学期映射关系
    semester_mapping = {
        1: '春季学期',
        2: '夏季学期',
        3: '秋季学期'
    }

    def format_teacher_data(teachers):
        formatted = []
        for t in teachers:
            gender = gender_mapping.get(t.T_sexual, '未知')
            Type = Teacher_Type_mapping.get(t.T_type, '未知')
            formatted.append({
                'T_ID': t.T_ID,
                'T_Name': t.T_Name,
                'T_sexual': gender,
                'T_type': Type
            })
        return formatted
    
    def format_paper_data(papers):
        formatted = []
        for p in papers:
            Type = Paper_Type_mapping.get(p.Paper.P_Type, '未知')
            Level = Level_mapping.get(p.Paper.P_Level, '未知')
            contact = contact_mapping.get(p.PublishPaper.P_Contact, '未知')
            formatted.append({
                'P_ID': p.Paper.P_ID,
                'T_ID': p.PublishPaper.T_ID,
                'P_Name': p.Paper.P_Name,
                'P_Url': p.Paper.P_Url,
                'P_Year':p.Paper.P_Year,
                'P_Type': Type,
                'P_Level': Level,
                'P_Rank':p.PublishPaper.P_Rank,
                'P_Contact':contact
            })
        return formatted
    
    def format_project_data(projects):
        formatted = []
        for p in projects:
            Type = Project_Type_mapping.get(p.Project.Pr_Type, '未知')
            formatted.append({
                'Pr_ID': p.Project.Pr_ID,
                'T_ID': p.OwnProject.T_ID,
                'Pr_Name': p.Project.Pr_Name,
                'Pr_Source': p.Project.Pr_Source,
                'Pr_Type': Type,
                'Pr_Summoney': p.Project.Pr_Summoney,
                'Pr_From': p.Project.Pr_From,
                'Pr_End': p.Project.Pr_End,
                'Pr_Rank': p.OwnProject.Pr_Rank,
                'Pr_money': p.OwnProject.Pr_money
            })
        return formatted
    
    def format_class_data(classes):
        formatted = []
        for c in classes:
            Type = Class_Type_mapping.get(c.Class.C_Type, '未知')
            semester = semester_mapping.get(c.TeachClass.C_Semester, '未知')
            formatted.append({
                'C_ID': c.Class.C_ID,
                'T_ID': c.TeachClass.T_ID, 
                'C_Name': c.Class.C_Name,
                'C_Sum': c.Class.C_Sum,
                'C_Type':Type,
                'C_Year': c.TeachClass.C_Year,
                'C_Semester': semester,
                'C_hours': c.TeachClass.C_hours
            })
        return formatted

    formatted_teacher_result = format_teacher_data(result_teacher)
    formatted_paper_result = format_paper_data(result_paper)
    formatted_project_result = format_project_data(result_project)
    formatted_class_result = format_class_data(result_class)

    if request.method == 'GET':
        return render_template('search.html', labels_teacher=labels_teacher, labels_paper=labels_paper, labels_project=labels_project, labels_class=labels_class,
                               content1=formatted_teacher_result, content2=formatted_paper_result, content3=formatted_project_result, content4=formatted_class_result)
    else:
        if request.form.get('type') == 'query':
            teacher_id = request.form.get('id')
            fromyear = request.form.get('fromyear')
            endyear = request.form.get('endyear')

            # 教师id查询：
            if teacher_id:
                result_query_teacher = result_query_teacher.filter(Teacher.T_ID == teacher_id)
                result_query_paper = result_query_paper.filter(PublishPaper.T_ID == teacher_id)
                result_query_project = result_query_project.filter(OwnProject.T_ID == teacher_id)
                result_query_class = result_query_class.filter(TeachClass.T_ID == teacher_id)
            
            # 根据年份范围筛选
            if fromyear and endyear:
                try:
                    # 论文年份查询
                    from_date = f"{int(fromyear)}-01-01"
                    to_date = f"{int(endyear)}-12-31"
                    result_query_paper = result_query_paper.filter(
                        Paper.P_Year.between(from_date, to_date)
                    )

                    # 项目年份查询
                    result_query_project = result_query_project.filter(
                        (Project.Pr_From <= endyear) & (Project.Pr_End >= fromyear)
                    )

                    # 授课年份查询
                    result_query_class = result_query_class.filter(
                        TeachClass.C_Year.between(fromyear, endyear)
                    )

                except ValueError:
                    pass  # 忽略非法年份输入
        
            result_teacher = result_query_teacher.all()
            result_paper = result_query_paper.all()
            result_project = result_query_project.all()
            result_class = result_query_class.all()
            
            formatted_teacher_result = format_teacher_data(result_teacher)
            formatted_paper_result = format_paper_data(result_paper)
            formatted_project_result = format_project_data(result_project)
            formatted_class_result = format_class_data(result_class)
            return render_template('search.html', labels_teacher=labels_teacher, labels_paper=labels_paper, labels_project=labels_project, labels_class=labels_class,
                               content1=formatted_teacher_result, content2=formatted_paper_result, content3=formatted_project_result, content4=formatted_class_result)
        
        elif request.form.get('type') == 'export':
            # 导出查询结果到pdf文件
            teacher_id = request.form.get('id')
            fromyear = request.form.get('fromyear')
            endyear = request.form.get('endyear')

            # 教师id查询：
            if teacher_id:
                result_query_teacher = result_query_teacher.filter(Teacher.T_ID == teacher_id)
                result_query_paper = result_query_paper.filter(PublishPaper.T_ID == teacher_id)
                result_query_project = result_query_project.filter(OwnProject.T_ID == teacher_id)
                result_query_class = result_query_class.filter(TeachClass.T_ID == teacher_id)
            
            # 根据年份范围筛选
            if fromyear and endyear:
                try:
                    # 论文年份查询
                    from_date = f"{int(fromyear)}-01-01"
                    to_date = f"{int(endyear)}-12-31"
                    result_query_paper = result_query_paper.filter(
                        Paper.P_Year.between(from_date, to_date)
                    )

                    # 项目年份查询
                    result_query_project = result_query_project.filter(
                        (Project.Pr_From <= endyear) & (Project.Pr_End >= fromyear)
                    )

                    # 授课年份查询
                    result_query_class = result_query_class.filter(
                        TeachClass.C_Year.between(fromyear, endyear)
                    )

                except ValueError:
                    pass  # 忽略非法年份输入
        
            result_teacher = result_query_teacher.all()
            result_paper = result_query_paper.all()
            result_project = result_query_project.all()
            result_class = result_query_class.all()
            
            formatted_teacher_result = format_teacher_data(result_teacher)
            formatted_paper_result = format_paper_data(result_paper)
            formatted_project_result = format_project_data(result_project)
            formatted_class_result = format_class_data(result_class)
            
            # 渲染模板
            rendered = render_template('export.html',
                                    content1=formatted_teacher_result,
                                    content2=formatted_paper_result,
                                    content3=formatted_project_result,
                                    content4=formatted_class_result,
                                    fromyear=fromyear,
                                    endyear=endyear)
            
            # 手动指定 wkhtmltopdf 路径
            config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

            pdf_file_path = 'output.pdf'

            # 生成 PDF
            pdfkit.from_string(rendered, pdf_file_path, configuration=config)

            # 构造响应
            print(f'PDF文件已生成：{pdf_file_path}')
            return rendered
            

    formatted_teacher_result = format_teacher_data(result_teacher)
    formatted_paper_result = format_paper_data(result_paper)
    formatted_project_result = format_project_data(result_project)
    formatted_class_result = format_class_data(result_class)
    return render_template('search.html', labels_teacher=labels_teacher, labels_paper=labels_paper, labels_project=labels_project, labels_class=labels_class,
                               content1=formatted_teacher_result, content2=formatted_paper_result, content3=formatted_project_result, content4=formatted_class_result)

    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
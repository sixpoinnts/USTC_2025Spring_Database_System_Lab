@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    labels = ['工号', '姓名', '性别', '职称']

    result_query = db.session.query(Teacher)
    result = result_query.all()

    # 定义一个函数来转换性别数字为文字
    def format_teacher_data(teachers):
        formatted = []
        for t in teachers:
            gender = '男' if t.T_sexual == 1 else '女' if t.T_sexual == 2 else '未知'
            formatted.append({
                'T_ID': t.T_ID,
                'T_Name': t.T_Name,
                'T_sexual': gender,
                'T_type': t.T_type
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
                result_query = result_query.filter(Teacher.T_sexual == int(teacher_sexual))
            if teacher_type != "":
                result_query = result_query.filter(Teacher.T_type == teacher_type)

            filtered = result_query.all()
            formatted_result = format_teacher_data(filtered)
            return render_template('teacher.html', labels=labels, content=formatted_result)

        elif request.form.get('type') == 'update':
            old_num = request.form.get('key')
            teacher_name = request.form.get('teacher_name')
            teacher_sexual = request.form.get('teacher_sexual')
            teacher_type = request.form.get('teacher_type')
            teacher_result = db.session.query(Teacher).filter_by(T_ID=old_num).first()
            teacher_result.T_Name = teacher_name
            teacher_result.T_sexual = int(teacher_sexual)
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
                T_sexual=int(teacher_sexual),
                T_type=teacher_type
            )

            db.session.add(newteacher)
            db.session.commit()

    result = db.session.query(Teacher).all()
    formatted_result = format_teacher_data(result)

    return render_template('teacher.html', labels=labels, content=formatted_result)
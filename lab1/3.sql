-- Active: 1744980885228@@127.0.0.1@3306@lab1

# 3 我们假设 Book 表有一些书具有超级 ID，它们以字符串“00”开头。这些超级 ID 不允许修改，
#   同时也不允许其它书的 ID 修改为超级 ID。请设计一个存储过程，实现对Book 表的 ID 的修
#   改，但是以字符串“00”开头的超级 ID 不允许修改，同时也不允许任何 ID 修改成“00”开头的
#   超级 ID（本题要求不得使用外键定义时的 on update cascade 选项，因为该选项不是所有 DBMS 都支持）。

DELIMITER //
DROP PROCEDURE IF EXISTS CHANGE_BOOKID;
CREATE PROCEDURE CHANGE_BOOKID(IN old_id char(8), IN new_id char(8), OUT state int)
BEGIN
    # state = 0 成功
    # state = 1 旧ID是超级ID, 不允许修改
    # state = 2 不允许修改为超级 ID
    # state = 3  ID 不存在
    # state = 4 其他错误
    DECLARE s INT DEFAULT 0;
    DECLARE count_book INT DEFAULT 0;

    DEClARE	CONTINUE HANDLER FOR 1451 SET s = 4; # 违反外键约束
    DEClARE	CONTINUE HANDLER FOR 1452 SET s = 4; # 插入无效的外键值
    
    # 首先判断是否为超级ID
    # 旧ID是否为超级ID
    IF old_id LIKE '00%' THEN
        SET s = 1; # 状态1：旧ID是超级ID
    # 新ID是否为超级ID
    ELSEIF new_id LIKE '00%' THEN
        SET s = 2; # 状态2：不允许修改为超级 ID
    END IF;

    # 查找book中是否有id=old_book_id的记录
    SELECT COUNT(book.id) FROM book WHERE book.id=old_id INTO count_book;
    IF count_book = 0 THEN
        SET s = 3;
    END IF;

    IF s = 0 THEN
        SET	FOREIGN_KEY_CHECKS = 0; # 临时禁用外键约束检查

        UPDATE	Book	SET ID = new_id	WHERE ID = old_id;
        UPDATE	Borrow	SET Book_ID = new_id	WHERE Book_ID = old_id;
        
        SET FOREIGN_KEY_CHECKS = 1;
    END IF;
    SET state = s;
END //
DELIMITER;

CALL CHANGE_BOOKID('b12','b21', @state);
CALL CHANGE_BOOKID('b21','b12', @state);
CALL CHANGE_BOOKID('00b00001','abc', @state);
CALL CHANGE_BOOKID('b12','00b00003', @state);
SELECT @state;
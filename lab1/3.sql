-- Active: 1744980885228@@127.0.0.1@3306@lab1

# 3 ���Ǽ��� Book ����һЩ����г��� ID���������ַ�����00����ͷ����Щ���� ID �������޸ģ�
#   ͬʱҲ������������� ID �޸�Ϊ���� ID�������һ���洢���̣�ʵ�ֶ�Book ��� ID ����
#   �ģ��������ַ�����00����ͷ�ĳ��� ID �������޸ģ�ͬʱҲ�������κ� ID �޸ĳɡ�00����ͷ��
#   ���� ID������Ҫ�󲻵�ʹ���������ʱ�� on update cascade ѡ���Ϊ��ѡ������� DBMS ��֧�֣���

DELIMITER //
DROP PROCEDURE IF EXISTS CHANGE_BOOKID;
CREATE PROCEDURE CHANGE_BOOKID(IN old_id char(8), IN new_id char(8), OUT state int)
BEGIN
    # state = 0 �ɹ�
    # state = 1 ��ID�ǳ���ID, �������޸�
    # state = 2 �������޸�Ϊ���� ID
    # state = 3  ID ������
    # state = 4 ��������
    DECLARE s INT DEFAULT 0;
    DECLARE count_book INT DEFAULT 0;

    DEClARE	CONTINUE HANDLER FOR 1451 SET s = 4; # Υ�����Լ��
    DEClARE	CONTINUE HANDLER FOR 1452 SET s = 4; # ������Ч�����ֵ
    
    # �����ж��Ƿ�Ϊ����ID
    # ��ID�Ƿ�Ϊ����ID
    IF old_id LIKE '00%' THEN
        SET s = 1; # ״̬1����ID�ǳ���ID
    # ��ID�Ƿ�Ϊ����ID
    ELSEIF new_id LIKE '00%' THEN
        SET s = 2; # ״̬2���������޸�Ϊ���� ID
    END IF;

    # ����book���Ƿ���id=old_book_id�ļ�¼
    SELECT COUNT(book.id) FROM book WHERE book.id=old_id INTO count_book;
    IF count_book = 0 THEN
        SET s = 3;
    END IF;

    IF s = 0 THEN
        SET	FOREIGN_KEY_CHECKS = 0; # ��ʱ�������Լ�����

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
-- Active: 1744980885228@@127.0.0.1@3306@lab1
# 4 ���һ����������ʵ�֣���һ���鱻���ʱ���Զ��� Book ������Ӧͼ��� status ��
# ��Ϊ 1 ���� times ��һ����ĳ���鱻�黹ʱ���Զ��� status ��Ϊ 0��

DELIMITER //
DROP TRIGGER IF EXISTS Book_Status_Borrow;
CREATE TRIGGER Book_Status_Borrow AFTER INSERT ON borrow FOR EACH ROW
BEGIN
    UPDATE Book SET status = 1, times = times + 1
    WHERE ID IN(SELECT Book_ID FROM borrow WHERE Return_Date is NULL);

END //
DELIMITER;

DELIMITER //
DROP TRIGGER IF EXISTS Book_Status_Return;
CREATE TRIGGER Book_Status_Return AFTER UPDATE ON borrow FOR EACH ROW
BEGIN
    UPDATE Book SET status = 0
    WHERE ID NOT IN(SELECT Book_ID FROM borrow WHERE Return_Date is NULL);

END //
DELIMITER;

update borrow SET `Return_Date` = '2024-05-23' WHERE `Book_ID` = 'b18' AND `Reader_ID` = 'r12'; 
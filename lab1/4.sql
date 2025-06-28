-- Active: 1744980885228@@127.0.0.1@3306@lab1
# 4 设计一个触发器，实现：当一本书被借出时，自动将 Book 表中相应图书的 status 修
# 改为 1 并将 times 加一；当某本书被归还时，自动将 status 改为 0。

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
-- Active: 1744980885228@@127.0.0.1@3306@lab1

# 1 查询读者 Rose 的读者号和地址
SELECT	ID, address
FROM 	reader
WHERE 	name = 'Rose';

# 2 查询读者 Rose 所借阅读书（包括已还和未还图书）的图书名和借期；
SELECT 	Book.name AS Book_name, Borrow_date
FROM 	Book, Reader, Borrow
WHERE 	Reader.ID = Borrow.Reader_ID AND 
		Borrow.Book_ID = Book.ID AND 
		Reader.name = 'Rose';

# 3 查询未借阅图书的读者姓名；
SELECT 	Reader.name AS Reader_name
FROM 	Reader
WHERE 	Reader.ID not in(SELECT Reader_ID FROM Borrow);

# 4 查询 Ullman 所写的书的书名和单价；
SELECT 	name, price
FROM	Book
WHERE 	author = 'Ullman';

# 5 查询读者“李林”借阅未还的图书的图书号和书名；
SELECT 	Book.ID, Book.name
FROM 	Book, Reader, Borrow
WHERE 	Reader.name = '李林' AND 
		Borrow.Reader_ID = Reader.ID AND
	  	Borrow.Book_ID = Book.ID AND 
		Return_Date is null;

# 6 查询借阅图书数目超过 3 本的读者姓名；
SELECT 	name 
FROM 	Reader 
WHERE 	ID 	IN(	SELECT Reader_ID 
			 	FROM Borrow, Reader
			 	WHERE Reader.ID = Borrow.Reader_ID
			 	GROUP BY Reader.ID 
				HAVING COUNT(Book_ID) > 3);


# 7 查询没有借阅读者“李林”所借的任何一本书的读者姓名和读者号；
SELECT 	Reader.name, Reader.ID
FROM 	Reader
WHERE 	ID 	NOT IN(
		SELECT 	Reader_ID
		FROM 	Borrow
		WHERE   Reader.ID = Borrow.Reader_ID AND
				Book_ID IN(	
					SELECT Book_ID
					FROM 	Borrow, Reader
					WHERE 	Reader.ID = Borrow.Reader_ID AND
							Reader.name = '李林'));

# 8 查询书名中包含“MySQL”的图书书名及图书号；
SELECT 	name, ID
FROM 	Book
WHERE   name LIKE '%MySQL%'; # LIKE 用于模糊查询，%表示任意字符

# 9 查询 2021 年借阅图书数目排名前 10 名的读者号、姓名、年龄以及借阅图书数；
SELECT 	Reader.ID, 
		Reader.name, 
		Reader.age, 
		COUNT(Borrow.Book_ID) AS Book_count
FROM 	Reader, Borrow  # 连接读者表和借阅表
WHERE 	Reader.ID = Borrow.Reader_ID AND
		Borrow.Borrow_Date >= '2021-01-01' AND
	  	Borrow.Borrow_Date <= '2021-12-31'
GROUP BY Reader.ID # 使用了聚合函数（COUNT（）），所以需要分组
ORDER BY Book_count DESC # 按照借阅图书数降序排列
LIMIT 10; # 限制结果为前 10 名

# 10 创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名和借期；
#    并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数；
DROP VIEW IF EXISTS Reader_Borrow_Message; # 删除视图（如果存在）
CREATE VIEW Reader_Borrow_Message AS(
	SELECT 	Reader.ID AS Reader_ID, 
			Reader.name AS Reader_name, 
			Book.ID AS Book_ID, 
			Book.name AS Book_name, 
			Borrow.Borrow_Date
	FROM 	Reader, Borrow, Book
	WHERE 	Reader.ID = Borrow.Reader_ID AND Borrow.Book_ID = Book.ID
);
# SELECT * FROM Reader_Borrow_Message;
SELECT 	Reader_ID, 
		COUNT(DISTINCT Book_ID) AS Different_Book_count # 去重统计
FROM 	Reader_Borrow_Message
WHERE 	YEAR(FROM_DAYS(TO_DAYS(NOW()) - TO_DAYS(Borrow_Date))) <= 1 # 计算借书时间在一年内
GROUP BY 	Reader_ID; # 按照读者号分组
DROP view Reader_Borrow_Message;
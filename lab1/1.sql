-- Active: 1744980885228@@127.0.0.1@3306
DROP DATABASE lab1;
CREATE database lab1;
use lab1;

CREATE table Book(
	ID char(8) not null,
    name varchar(10) not null,
    author varchar(10) default null,
    price float default null,
    status int default '0',
    times int default '0',
    primary key (ID)
);

CREATE table Reader(
	ID char(8) not null,
    name varchar(10) default null,
    age int default null,
    address varchar(20) default null,
    primary key (ID)
);

CREATE table Borrow(
	Book_ID char(8) not null,
    Reader_ID char(8) not null,
    Borrow_Date date default null,
    Return_Date date default null,
    primary key (Book_ID, Reader_ID),
    foreign key (Book_ID) references Book(ID),
    foreign key (Reader_ID) references Reader(ID)
); 

-- CREATE TABLE Borrow (
--     Book_ID CHAR(8) NOT NULL,
--     Reader_ID CHAR(8) NOT NULL,
--     Borrow_Date DATE DEFAULT NULL,
--     Return_Date DATE DEFAULT NULL,
--     PRIMARY KEY (Book_ID, Reader_ID)
-- );

-- ALTER TABLE Borrow
-- ADD CONSTRAINT book_id
-- FOREIGN KEY (Book_ID) REFERENCES Book(ID);

-- ALTER TABLE Borrow
-- ADD CONSTRAINT reader_id
-- FOREIGN KEY (Reader_ID) REFERENCES Reader(ID);

# 查看权限
# SHOW GRANTS FOR CURRENT_USER;

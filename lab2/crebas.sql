/*==============================================================*/
/* DBMS name:      SAP SQL Anywhere 17                          */
/* Created on:     2025/5/11 17:34:02                           */
/*==============================================================*/


if exists(select 1 from sys.sysforeignkey where role='FK_ACCOUNT_OPEN_ACCO_BANK') then
    alter table Account
       delete foreign key FK_ACCOUNT_OPEN_ACCO_BANK
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_CHECKING_INHERITAN_ACCOUNT') then
    alter table Checking_Account
       delete foreign key FK_CHECKING_INHERITAN_ACCOUNT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_DEPARTME_BUILD_BANK') then
    alter table Department
       delete foreign key FK_DEPARTME_BUILD_BANK
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_DEPARTME_INHERITAN_EMPLOYEE') then
    alter table "Department Manager"
       delete foreign key FK_DEPARTME_INHERITAN_EMPLOYEE
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_EMPLOYEE_WORK_BANK') then
    alter table Employee
       delete foreign key FK_EMPLOYEE_WORK_BANK
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_EMPLOYEE_WORK2_DEPARTME') then
    alter table Employee
       delete foreign key FK_EMPLOYEE_WORK2_DEPARTME
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_LOAN_GIVE_BANK') then
    alter table Loan
       delete foreign key FK_LOAN_GIVE_BANK
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_PAYMENT_EVERY_PAY_LOAN') then
    alter table PayMent
       delete foreign key FK_PAYMENT_EVERY_PAY_LOAN
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SAVINGS__INHERITAN_ACCOUNT') then
    alter table Savings_Account
       delete foreign key FK_SAVINGS__INHERITAN_ACCOUNT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SERVICE_SERVICE_EMPLOYEE') then
    alter table Service
       delete foreign key FK_SERVICE_SERVICE_EMPLOYEE
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_SERVICE_SERVICE2_CLIENT') then
    alter table Service
       delete foreign key FK_SERVICE_SERVICE2_CLIENT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_VISITDAT_VISITDATE_CLIENT') then
    alter table VisitDate1
       delete foreign key FK_VISITDAT_VISITDATE_CLIENT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_VISITDAT_VISITDATE_SAVINGS_') then
    alter table VisitDate1
       delete foreign key FK_VISITDAT_VISITDATE_SAVINGS_
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_VISITDAT_VISITDATE_CHECKING') then
    alter table VisitDate2
       delete foreign key FK_VISITDAT_VISITDATE_CHECKING
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_VISITDAT_VISITDATE_CLIENT') then
    alter table VisitDate2
       delete foreign key FK_VISITDAT_VISITDATE_CLIENT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_LEAD_LEAD_DEPARTME') then
    alter table lead
       delete foreign key FK_LEAD_LEAD_DEPARTME
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_LEAD_LEAD2_EMPLOYEE') then
    alter table lead
       delete foreign key FK_LEAD_LEAD2_EMPLOYEE
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_OWN_OWN_CLIENT') then
    alter table own
       delete foreign key FK_OWN_OWN_CLIENT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_OWN_OWN2_LOAN') then
    alter table own
       delete foreign key FK_OWN_OWN2_LOAN
end if;

drop index if exists Account.Open_Account_FK;

drop index if exists Account.Account_PK;

drop table if exists Account;

drop index if exists Bank.Bank_PK;

drop table if exists Bank;

drop index if exists Checking_Account.Checking_Account_PK;

drop table if exists Checking_Account;

drop index if exists Client.Client_PK;

drop table if exists Client;

drop index if exists Department.build_FK;

drop index if exists Department.Department_PK;

drop table if exists Department;

drop index if exists "Department Manager"."Department Manager_PK";

drop table if exists "Department Manager";

drop index if exists Employee.work2_FK;

drop index if exists Employee.Work_FK;

drop index if exists Employee.Employee_PK;

drop table if exists Employee;

drop index if exists Loan.give_FK;

drop index if exists Loan.Loan_PK;

drop table if exists Loan;

drop index if exists PayMent.Every_Pay_FK;

drop index if exists PayMent.PayMent_PK;

drop table if exists PayMent;

drop index if exists Savings_Account.Savings_Account_PK;

drop table if exists Savings_Account;

drop index if exists Service.Service2_FK;

drop index if exists Service.Service_FK;

drop index if exists Service.Service_PK;

drop table if exists Service;

drop index if exists VisitDate1.VisitDate2_FK;

drop index if exists VisitDate1.VisitDate1_FK;

drop index if exists VisitDate1.VisitDate1_PK;

drop table if exists VisitDate1;

drop index if exists VisitDate2.VisitDate4_FK;

drop index if exists VisitDate2.VisitDate3_FK;

drop index if exists VisitDate2.VisitDate2_PK;

drop table if exists VisitDate2;

drop index if exists lead.lead2_FK;

drop index if exists lead.lead_FK;

drop index if exists lead.lead_PK;

drop table if exists lead;

drop index if exists own.own2_FK;

drop index if exists own.own_FK;

drop index if exists own.own_PK;

drop table if exists own;

/*==============================================================*/
/* Table: Account                                               */
/*==============================================================*/
create or replace table Account 
(
   A_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    not null,
   Balance              double                         null,
   OpenDate             date                           null,
   constraint PK_ACCOUNT primary key clustered (A_ID)
);

/*==============================================================*/
/* Index: Account_PK                                            */
/*==============================================================*/
create unique clustered index Account_PK on Account (
A_ID ASC
);

/*==============================================================*/
/* Index: Open_Account_FK                                       */
/*==============================================================*/
create index Open_Account_FK on Account (
B_Name ASC
);

/*==============================================================*/
/* Table: Bank                                                  */
/*==============================================================*/
create or replace table Bank 
(
   B_Name               varchar(50)                    not null,
   City                 varchar(50)                    not null,
   Assets               double                         not null,
   constraint PK_BANK primary key clustered (B_Name)
);

/*==============================================================*/
/* Index: Bank_PK                                               */
/*==============================================================*/
create unique clustered index Bank_PK on Bank (
B_Name ASC
);

/*==============================================================*/
/* Table: Checking_Account                                      */
/*==============================================================*/
create or replace table Checking_Account 
(
   A_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    null,
   Balance              double                         null,
   OpenDate             date                           null,
   Overdraft            double                         null,
   constraint PK_CHECKING_ACCOUNT primary key clustered (A_ID)
);

/*==============================================================*/
/* Index: Checking_Account_PK                                   */
/*==============================================================*/
create unique clustered index Checking_Account_PK on Checking_Account (
A_ID ASC
);

/*==============================================================*/
/* Table: Client                                                */
/*==============================================================*/
create or replace table Client 
(
   C_ID                 varchar(50)                    not null,
   C_Name               varchar(50)                    not null,
   C_Tel                integer                        not null,
   C_Addr               varchar(50)                    not null,
   Co_Name              varchar(50)                    not null,
   Co_Tel               integer                        not null,
   Co_Email             varchar(50)                    not null,
   CCoRelation          varchar(50)                    not null,
   constraint PK_CLIENT primary key clustered (C_ID)
);

/*==============================================================*/
/* Index: Client_PK                                             */
/*==============================================================*/
create unique clustered index Client_PK on Client (
C_ID ASC
);

/*==============================================================*/
/* Table: Department                                            */
/*==============================================================*/
create or replace table Department 
(
   D_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    not null,
   D_Name               varchar(50)                    null,
   D_Type               varchar(50)                    null,
   DM_ID                varchar(50)                    null,
   constraint PK_DEPARTMENT primary key clustered (D_ID)
);

/*==============================================================*/
/* Index: Department_PK                                         */
/*==============================================================*/
create unique clustered index Department_PK on Department (
D_ID ASC
);

/*==============================================================*/
/* Index: build_FK                                              */
/*==============================================================*/
create index build_FK on Department (
B_Name ASC
);

/*==============================================================*/
/* Table: "Department Manager"                                  */
/*==============================================================*/
create or replace table "Department Manager" 
(
   E_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    null,
   D_ID                 varchar(50)                    null,
   E_Tel                integer                        null,
   E_Addr               varchar(50)                    null,
   Work_date            date                           null,
   constraint "PK_DEPARTMENT MANAGER" primary key clustered (E_ID)
);

/*==============================================================*/
/* Index: "Department Manager_PK"                               */
/*==============================================================*/
create unique clustered index "Department Manager_PK" on "Department Manager" (
E_ID ASC
);

/*==============================================================*/
/* Table: Employee                                              */
/*==============================================================*/
create or replace table Employee 
(
   E_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    not null,
   D_ID                 varchar(50)                    not null,
   E_Tel                integer                        null,
   E_Addr               varchar(50)                    null,
   Work_date            date                           null,
   constraint PK_EMPLOYEE primary key clustered (E_ID)
);

/*==============================================================*/
/* Index: Employee_PK                                           */
/*==============================================================*/
create unique clustered index Employee_PK on Employee (
E_ID ASC
);

/*==============================================================*/
/* Index: Work_FK                                               */
/*==============================================================*/
create index Work_FK on Employee (
B_Name ASC
);

/*==============================================================*/
/* Index: work2_FK                                              */
/*==============================================================*/
create index work2_FK on Employee (
D_ID ASC
);

/*==============================================================*/
/* Table: Loan                                                  */
/*==============================================================*/
create or replace table Loan 
(
   L_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    null,
   L_Sum                double                         null,
   constraint PK_LOAN primary key clustered (L_ID)
);

/*==============================================================*/
/* Index: Loan_PK                                               */
/*==============================================================*/
create unique clustered index Loan_PK on Loan (
L_ID ASC
);

/*==============================================================*/
/* Index: give_FK                                               */
/*==============================================================*/
create index give_FK on Loan (
B_Name ASC
);

/*==============================================================*/
/* Table: PayMent                                               */
/*==============================================================*/
create or replace table PayMent 
(
   P_ID                 varchar(50)                    not null,
   L_ID                 varchar(50)                    null,
   PayDate              date                           null,
   PayMoney             double                         null,
   constraint PK_PAYMENT primary key clustered (P_ID)
);

/*==============================================================*/
/* Index: PayMent_PK                                            */
/*==============================================================*/
create unique clustered index PayMent_PK on PayMent (
P_ID ASC
);

/*==============================================================*/
/* Index: Every_Pay_FK                                          */
/*==============================================================*/
create index Every_Pay_FK on PayMent (
L_ID ASC
);

/*==============================================================*/
/* Table: Savings_Account                                       */
/*==============================================================*/
create or replace table Savings_Account 
(
   A_ID                 varchar(50)                    not null,
   B_Name               varchar(50)                    null,
   Balance              double                         null,
   OpenDate             date                           null,
   Interest_rate        double                         null,
   Currency_type        varchar(50)                    null,
   constraint PK_SAVINGS_ACCOUNT primary key clustered (A_ID)
);

/*==============================================================*/
/* Index: Savings_Account_PK                                    */
/*==============================================================*/
create unique clustered index Savings_Account_PK on Savings_Account (
A_ID ASC
);

/*==============================================================*/
/* Table: Service                                               */
/*==============================================================*/
create or replace table Service 
(
   E_ID                 varchar(50)                    not null,
   C_ID                 varchar(50)                    not null,
   S_Type               varchar(50)                    null,
   constraint PK_SERVICE primary key clustered (E_ID, C_ID)
);

/*==============================================================*/
/* Index: Service_PK                                            */
/*==============================================================*/
create unique clustered index Service_PK on Service (
E_ID ASC,
C_ID ASC
);

/*==============================================================*/
/* Index: Service_FK                                            */
/*==============================================================*/
create index Service_FK on Service (
E_ID ASC
);

/*==============================================================*/
/* Index: Service2_FK                                           */
/*==============================================================*/
create index Service2_FK on Service (
C_ID ASC
);

/*==============================================================*/
/* Table: VisitDate1                                            */
/*==============================================================*/
create or replace table VisitDate1 
(
   C_ID                 varchar(50)                    not null,
   A_ID                 varchar(50)                    not null,
   VisitDate1           date                           null,
   constraint PK_VISITDATE1 primary key clustered (C_ID, A_ID)
);

/*==============================================================*/
/* Index: VisitDate1_PK                                         */
/*==============================================================*/
create unique clustered index VisitDate1_PK on VisitDate1 (
C_ID ASC,
A_ID ASC
);

/*==============================================================*/
/* Index: VisitDate1_FK                                         */
/*==============================================================*/
create index VisitDate1_FK on VisitDate1 (
C_ID ASC
);

/*==============================================================*/
/* Index: VisitDate2_FK                                         */
/*==============================================================*/
create index VisitDate2_FK on VisitDate1 (
A_ID ASC
);

/*==============================================================*/
/* Table: VisitDate2                                            */
/*==============================================================*/
create or replace table VisitDate2 
(
   A_ID                 varchar(50)                    not null,
   C_ID                 varchar(50)                    not null,
   VisitDate2           date                           null,
   constraint PK_VISITDATE2 primary key clustered (A_ID, C_ID)
);

/*==============================================================*/
/* Index: VisitDate2_PK                                         */
/*==============================================================*/
create unique clustered index VisitDate2_PK on VisitDate2 (
A_ID ASC,
C_ID ASC
);

/*==============================================================*/
/* Index: VisitDate3_FK                                         */
/*==============================================================*/
create index VisitDate3_FK on VisitDate2 (
A_ID ASC
);

/*==============================================================*/
/* Index: VisitDate4_FK                                         */
/*==============================================================*/
create index VisitDate4_FK on VisitDate2 (
C_ID ASC
);

/*==============================================================*/
/* Table: lead                                                  */
/*==============================================================*/
create or replace table lead 
(
   Dep_E_ID             varchar(50)                    not null,
   E_ID                 varchar(50)                    not null,
   constraint PK_LEAD primary key clustered (Dep_E_ID, E_ID)
);

/*==============================================================*/
/* Index: lead_PK                                               */
/*==============================================================*/
create unique clustered index lead_PK on lead (
Dep_E_ID ASC,
E_ID ASC
);

/*==============================================================*/
/* Index: lead_FK                                               */
/*==============================================================*/
create index lead_FK on lead (
Dep_E_ID ASC
);

/*==============================================================*/
/* Index: lead2_FK                                              */
/*==============================================================*/
create index lead2_FK on lead (
E_ID ASC
);

/*==============================================================*/
/* Table: own                                                   */
/*==============================================================*/
create or replace table own 
(
   C_ID                 varchar(50)                    not null,
   L_ID                 varchar(50)                    not null,
   constraint PK_OWN primary key clustered (C_ID, L_ID)
);

/*==============================================================*/
/* Index: own_PK                                                */
/*==============================================================*/
create unique clustered index own_PK on own (
C_ID ASC,
L_ID ASC
);

/*==============================================================*/
/* Index: own_FK                                                */
/*==============================================================*/
create index own_FK on own (
C_ID ASC
);

/*==============================================================*/
/* Index: own2_FK                                               */
/*==============================================================*/
create index own2_FK on own (
L_ID ASC
);

alter table Account
   add constraint FK_ACCOUNT_OPEN_ACCO_BANK foreign key (B_Name)
      references Bank (B_Name)
      on update restrict
      on delete restrict;

alter table Checking_Account
   add constraint FK_CHECKING_INHERITAN_ACCOUNT foreign key (A_ID)
      references Account (A_ID)
      on update restrict
      on delete restrict;

alter table Department
   add constraint FK_DEPARTME_BUILD_BANK foreign key (B_Name)
      references Bank (B_Name)
      on update restrict
      on delete restrict;

alter table "Department Manager"
   add constraint FK_DEPARTME_INHERITAN_EMPLOYEE foreign key (E_ID)
      references Employee (E_ID)
      on update restrict
      on delete restrict;

alter table Employee
   add constraint FK_EMPLOYEE_WORK_BANK foreign key (B_Name)
      references Bank (B_Name)
      on update restrict
      on delete restrict;

alter table Employee
   add constraint FK_EMPLOYEE_WORK2_DEPARTME foreign key (D_ID)
      references Department (D_ID)
      on update restrict
      on delete restrict;

alter table Loan
   add constraint FK_LOAN_GIVE_BANK foreign key (B_Name)
      references Bank (B_Name)
      on update restrict
      on delete restrict;

alter table PayMent
   add constraint FK_PAYMENT_EVERY_PAY_LOAN foreign key (L_ID)
      references Loan (L_ID)
      on update restrict
      on delete restrict;

alter table Savings_Account
   add constraint FK_SAVINGS__INHERITAN_ACCOUNT foreign key (A_ID)
      references Account (A_ID)
      on update restrict
      on delete restrict;

alter table Service
   add constraint FK_SERVICE_SERVICE_EMPLOYEE foreign key (E_ID)
      references Employee (E_ID)
      on update restrict
      on delete restrict;

alter table Service
   add constraint FK_SERVICE_SERVICE2_CLIENT foreign key (C_ID)
      references Client (C_ID)
      on update restrict
      on delete restrict;

alter table VisitDate1
   add constraint FK_VISITDAT_VISITDATE_CLIENT foreign key (C_ID)
      references Client (C_ID)
      on update restrict
      on delete restrict;

alter table VisitDate1
   add constraint FK_VISITDAT_VISITDATE_SAVINGS_ foreign key (A_ID)
      references Savings_Account (A_ID)
      on update restrict
      on delete restrict;

alter table VisitDate2
   add constraint FK_VISITDAT_VISITDATE_CHECKING foreign key (A_ID)
      references Checking_Account (A_ID)
      on update restrict
      on delete restrict;

alter table VisitDate2
   add constraint FK_VISITDAT_VISITDATE_CLIENT foreign key (C_ID)
      references Client (C_ID)
      on update restrict
      on delete restrict;

alter table lead
   add constraint FK_LEAD_LEAD_DEPARTME foreign key (Dep_E_ID)
      references "Department Manager" (E_ID)
      on update restrict
      on delete restrict;

alter table lead
   add constraint FK_LEAD_LEAD2_EMPLOYEE foreign key (E_ID)
      references Employee (E_ID)
      on update restrict
      on delete restrict;

alter table own
   add constraint FK_OWN_OWN_CLIENT foreign key (C_ID)
      references Client (C_ID)
      on update restrict
      on delete restrict;

alter table own
   add constraint FK_OWN_OWN2_LOAN foreign key (L_ID)
      references Loan (L_ID)
      on update restrict
      on delete restrict;


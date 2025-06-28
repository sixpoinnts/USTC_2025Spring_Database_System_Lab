/*==============================================================*/
/* DBMS name:      SAP SQL Anywhere 17                          */
/* Created on:     2025/5/26 22:28:21                           */
/*==============================================================*/


if exists(select 1 from sys.sysforeignkey where role='FK_OWN_PROJ_OWN_PROJE_TEACHER') then
    alter table Own_Project
       delete foreign key FK_OWN_PROJ_OWN_PROJE_TEACHER
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_OWN_PROJ_OWN_PROJE_PROJECT') then
    alter table Own_Project
       delete foreign key FK_OWN_PROJ_OWN_PROJE_PROJECT
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_PUBLISH__PUBLISH_P_PAPER') then
    alter table Publish_Paper
       delete foreign key FK_PUBLISH__PUBLISH_P_PAPER
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_PUBLISH__PUBLISH_P_TEACHER') then
    alter table Publish_Paper
       delete foreign key FK_PUBLISH__PUBLISH_P_TEACHER
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_TEACH_C_TEACH_CL_TEACHER') then
    alter table Teach_Class
       delete foreign key FK_TEACH_C_TEACH_CL_TEACHER
end if;

if exists(select 1 from sys.sysforeignkey where role='FK_TEACH_C_TEACH_CL_CLASS') then
    alter table Teach_Class
       delete foreign key FK_TEACH_C_TEACH_CL_CLASS
end if;

drop index if exists Class.Class_PK;

drop table if exists Class;

drop index if exists Own_Project.Own_Project2_FK;

drop index if exists Own_Project.Own_Project_FK;

drop index if exists Own_Project.Own_Project_PK;

drop table if exists Own_Project;

drop index if exists Paper.Paper_PK;

drop table if exists Paper;

drop index if exists Project.Project_PK;

drop table if exists Project;

drop index if exists Publish_Paper.Publish_Paper2_FK;

drop index if exists Publish_Paper.Publish_Paper_FK;

drop index if exists Publish_Paper.Publish_Paper_PK;

drop table if exists Publish_Paper;

drop index if exists Teach_Class.Teach_Class2_FK;

drop index if exists Teach_Class.Teach_Class_FK;

drop index if exists Teach_Class.Teach_Class_PK;

drop table if exists Teach_Class;

drop index if exists Teacher.Teacher_PK;

drop table if exists Teacher;

/*==============================================================*/
/* Table: Class                                                 */
/*==============================================================*/
create or replace table Class 
(
   C_ID                 char(256)                      not null,
   C_Name               char(256)                      null,
   C_Sum                integer                        null,
   C_Type               integer                        null,
   constraint PK_CLASS primary key clustered (C_ID)
);

/*==============================================================*/
/* Index: Class_PK                                              */
/*==============================================================*/
create unique clustered index Class_PK on Class (
C_ID ASC
);

/*==============================================================*/
/* Table: Own_Project                                           */
/*==============================================================*/
create or replace table Own_Project 
(
   T_ID                 char(5)                        not null,
   Pr_ID                char(256)                      not null,
   Pr_Rank              integer                        null,
   Pr_money             float                          null,
   constraint PK_OWN_PROJECT primary key clustered (T_ID, Pr_ID)
);

/*==============================================================*/
/* Index: Own_Project_PK                                        */
/*==============================================================*/
create unique clustered index Own_Project_PK on Own_Project (
T_ID ASC,
Pr_ID ASC
);

/*==============================================================*/
/* Index: Own_Project_FK                                        */
/*==============================================================*/
create index Own_Project_FK on Own_Project (
T_ID ASC
);

/*==============================================================*/
/* Index: Own_Project2_FK                                       */
/*==============================================================*/
create index Own_Project2_FK on Own_Project (
Pr_ID ASC
);

/*==============================================================*/
/* Table: Paper                                                 */
/*==============================================================*/
create or replace table Paper 
(
   P_ID                 integer                        not null,
   P_Name               char(256)                      null,
   P_Url                char(256)                      null,
   P_Year               date                           null,
   P_Type               integer                        null,
   P_Level              integer                        null,
   constraint PK_PAPER primary key clustered (P_ID)
);

/*==============================================================*/
/* Index: Paper_PK                                              */
/*==============================================================*/
create unique clustered index Paper_PK on Paper (
P_ID ASC
);

/*==============================================================*/
/* Table: Project                                               */
/*==============================================================*/
create or replace table Project 
(
   Pr_ID                char(256)                      not null,
   Pr_Name              char(256)                      null,
   Pr_From              char(256)                      null,
   Pr_Summoney          float                          null,
   Pr_Fromyear          integer                        null,
   Pr_Endyear           integer                        null,
   constraint PK_PROJECT primary key clustered (Pr_ID)
);

/*==============================================================*/
/* Index: Project_PK                                            */
/*==============================================================*/
create unique clustered index Project_PK on Project (
Pr_ID ASC
);

/*==============================================================*/
/* Table: Publish_Paper                                         */
/*==============================================================*/
create or replace table Publish_Paper 
(
   P_ID                 integer                        not null,
   T_ID                 char(5)                        not null,
   P_Rank               integer                        null,
   P_Contact            smallint                       null,
   constraint PK_PUBLISH_PAPER primary key clustered (P_ID, T_ID)
);

/*==============================================================*/
/* Index: Publish_Paper_PK                                      */
/*==============================================================*/
create unique clustered index Publish_Paper_PK on Publish_Paper (
P_ID ASC,
T_ID ASC
);

/*==============================================================*/
/* Index: Publish_Paper_FK                                      */
/*==============================================================*/
create index Publish_Paper_FK on Publish_Paper (
P_ID ASC
);

/*==============================================================*/
/* Index: Publish_Paper2_FK                                     */
/*==============================================================*/
create index Publish_Paper2_FK on Publish_Paper (
T_ID ASC
);

/*==============================================================*/
/* Table: Teach_Class                                          */
/*==============================================================*/
create or replace table Teach_Class 
(
   T_ID                 char(5)                        not null,
   C_ID                 char(256)                      not null,
   C_Year               integer                        null,
   C_Semester           integer                        null,
   C_hours              integer                        null,
   constraint PK_TEACH_CLASS primary key clustered (T_ID, C_ID)
);

/*==============================================================*/
/* Index: Teach_Class_PK                                       */
/*==============================================================*/
create unique clustered index Teach_Class_PK on Teach_Class (
T_ID ASC,
C_ID ASC
);

/*==============================================================*/
/* Index: Teach_Class_FK                                       */
/*==============================================================*/
create index Teach_Class_FK on Teach_Class (
T_ID ASC
);

/*==============================================================*/
/* Index: Teach_Class2_FK                                      */
/*==============================================================*/
create index Teach_Class2_FK on Teach_Class (
C_ID ASC
);

/*==============================================================*/
/* Table: Teacher                                               */
/*==============================================================*/
create or replace table Teacher 
(
   T_ID                 char(5)                        not null,
   T_Name               char(256)                      null,
   T_sexual             integer                        null,
   T_type               integer                        null,
   constraint PK_TEACHER primary key clustered (T_ID)
);

/*==============================================================*/
/* Index: Teacher_PK                                            */
/*==============================================================*/
create unique clustered index Teacher_PK on Teacher (
T_ID ASC
);

alter table Own_Project
   add constraint FK_OWN_PROJ_OWN_PROJE_TEACHER foreign key (T_ID)
      references Teacher (T_ID)
      on update restrict
      on delete restrict;

alter table Own_Project
   add constraint FK_OWN_PROJ_OWN_PROJE_PROJECT foreign key (Pr_ID)
      references Project (Pr_ID)
      on update restrict
      on delete restrict;

alter table Publish_Paper
   add constraint FK_PUBLISH__PUBLISH_P_PAPER foreign key (P_ID)
      references Paper (P_ID)
      on update restrict
      on delete restrict;

alter table Publish_Paper
   add constraint FK_PUBLISH__PUBLISH_P_TEACHER foreign key (T_ID)
      references Teacher (T_ID)
      on update restrict
      on delete restrict;

alter table Teach_Class
   add constraint FK_TEACH_C_TEACH_CL_TEACHER foreign key (T_ID)
      references Teacher (T_ID)
      on update restrict
      on delete restrict;

alter table Teach_Class
   add constraint FK_TEACH_C_TEACH_CL_CLASS foreign key (C_ID)
      references Class (C_ID)
      on update restrict
      on delete restrict;


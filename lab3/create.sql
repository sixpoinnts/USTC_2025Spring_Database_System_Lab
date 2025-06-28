DROP DATABASE lab3;
CREATE database lab3;
use lab3;
drop table if exists Teacher;
drop table if exists Class;
drop table if exists Paper;
drop table if exists Project;
drop table if exists Own_Project;
drop table if exists Publish_Paper;
drop table if exists Teach_Class;

/*==============================================================*/
/* Table: Teacher                                               */
/*==============================================================*/
create table Teacher (
   T_ID     varchar(5) not null,
   T_Name   varchar(256) default null,
   T_sexual integer default null,
   T_type   integer default null,
   primary key (T_ID)
);
/*==============================================================*/
/* Table: Class                                                 */
/*==============================================================*/
create table Class (
   C_ID     varchar(256) not null,
   C_Name   varchar(256) default null,
   C_Sum    integer default null,
   C_Type   integer default null,
   primary key (C_ID)
);
/*==============================================================*/
/* Table: Paper                                                 */
/*==============================================================*/
create table Paper (
   P_ID     integer not null,
   P_Name   varchar(256) default null,
   P_Url    varchar(256) default null,
   P_Year   date default null,
   P_Type   integer default null,
   P_Level  integer default null,
   primary key (P_ID)
);
/*==============================================================*/
/* Table: Project                                               */
/*==============================================================*/
create table Project (
   Pr_ID       varchar(256) not null,
   Pr_Name     varchar(256) default null,
   Pr_Source   varchar(256) default null,
   Pr_Type     integer default null,
   Pr_Summoney float default null,
   Pr_From     integer default null,
   Pr_End      integer default null,
   primary key(Pr_ID)
);
/*==============================================================*/
/* Table: Own_Project                                           */
/*==============================================================*/
create table Own_Project 
(
   T_ID     varchar(5) not null,
   Pr_ID    varchar(256) not null,
   Pr_Rank  integer default null,
   Pr_money float default null,
   primary key(T_ID, Pr_ID)
);
/*==============================================================*/
/* Table: Teach_Class                                          */
/*==============================================================*/
create table Teach_Class 
(
   T_ID        varchar(5) not null,
   C_ID        varchar(256) not null,
   C_Year      integer default null,
   C_Semester  integer default null,
   C_hours     integer default null,
   primary key (T_ID, C_ID)
);
/*==============================================================*/
/* Table: Publish_Paper                                         */
/*==============================================================*/
create table Publish_Paper 
(
   P_ID        integer not null,
   T_ID        varchar(5)                        not null,
   P_Rank      integer default null,
   P_Contact   smallint default null,
   primary key (P_ID, T_ID)
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

alter table Teach_Class
   add constraint FK_TEACH_C_TEACH_CL_TEACHER foreign key (T_ID)
      references Teacher (T_ID)
      on update restrict
      on delete restrict;

alter table Teach_Class
   add constraint FK_TEACH_C_TEACH_CL_CLASS foreign key (C_ID)
      references Class (C_ID)
      on update restrict
      on delete restrict;
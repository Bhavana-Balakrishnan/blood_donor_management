create database blood_db_aug26;
use blood_db_aug26;
create table donor(id int primary key auto_increment,
     name VARCHAR(100),
     blood_group varchar(5),
     phone varchar(15) unique,
     city varchar(100),
     last_donation date
     )

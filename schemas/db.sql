-- auto-generated definition
create table nickels
(
    id          int auto_increment
        primary key,
    guild       text                     not null,
    username    text                     not null,
    word        text                     not null,
    messaged_on datetime default (now()) not null
);

-- auto-generated definition
create table birthdays
(
    id          int auto_increment
        primary key,
    guild       text                     not null,
    username    text                     not null,
    birthday    datetime                 not null,
    added_by    text                     not null,
    added_on    datetime default (now()) not null
);

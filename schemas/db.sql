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

create table birthdays
(
    id          int auto_increment
        primary key,
    guild       bigint                   not null,
    user_id     bigint                   not null,
    birthday    datetime                 not null,
    added_by    text                     not null,
    added_on    datetime default (now()) not null
);

create table settings
(
    id          int auto_increment
        primary key,
    guild       bigint                   not null,
    setting     text                     not null,
    value       text                     not null,
    set_by      text                     not null,
    set_on      datetime default (now()) not null
);

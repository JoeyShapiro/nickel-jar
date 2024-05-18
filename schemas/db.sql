-- auto-generated definition
create table nickels
(
    id          int auto_increment
        primary key,
    guild       text     not null,
    username    text     not null,
    word        text     not null,
    messaged_on datetime not null
);

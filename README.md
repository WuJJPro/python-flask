# twt-天大毕业季-python-falsk重构代码
接口文档

**https://documenter.getpostman.com/view/18421082/VUxUP5e1**

mysql57 需要支持json字段

mysql配置文件在config.py中


sql建表语句
```sql
create table comment
(
    id              int auto_increment
        primary key,
    comment         varchar(255)                        null,
    created_at      timestamp default CURRENT_TIMESTAMP null,
    father_id       int                                 null,
    like_number     int       default 0                 null,
    dislike_number  int       default 0                 null,
    userid          varchar(255)                        null,
    picture         json                                null,
    nickname        varchar(255)                        null,
    avatar          varchar(255)                        null,
    isShow          int       default 1                 null,
    type            int                                 null,
    question        int                                 null,
    root_comment_id int                                 null,
    is_special      int       default 0                 null,
    constraint USER_id_uindex
        unique (id)
)

create table picture
(
    id    int default 0 not null
        primary key,
    array text          null,
    state int           null,
    constraint picture_id_uindex
        unique (id)
)

create table question
(
    id            int auto_increment
        primary key,
    content       varchar(255)                        null,
    created_at    timestamp default CURRENT_TIMESTAMP null,
    likeNumber    int                                 null,
    dislikeNumber int                                 null,
    picture       json                                null,
    constraint USER_id_uindex
        unique (id)
)

create table user
(
    id         varchar(255)                        not null
        primary key,
    tapNumber  int                                 null,
    is_admin   int                                 null,
    created_at timestamp default CURRENT_TIMESTAMP null,
    constraint user_id_uindex
        unique (id)
)

create table user_dislike
(
    id         int auto_increment
        primary key,
    userid     varchar(255)                        null,
    comment_id int                                 null,
    created_at timestamp default CURRENT_TIMESTAMP null,
    type       int                                 null,
    constraint user_dislike_id_uindex
        unique (id)
)

create table user_like
(
    id         int auto_increment
        primary key,
    userid     varchar(255)                        null,
    comment_id int                                 null,
    created_at timestamp default CURRENT_TIMESTAMP null,
    type       int                                 null,
    constraint user_like_id_uindex
        unique (id)
)
```

dock部署

1. dockfile文件
```dockerfile
# 基于的基础镜像
FROM python:3.9.6
# 将flask目录下的代码添加到镜像中的code文件夹（两个目录参数中间有空格分开）
ADD ./flask /code
# 设置code文件夹是工作目录
WORKDIR /code
# 安装支持
RUN pip install -r requirements.txt
#docker运行时即运行app.py文件
CMD ["python","/code/manage.py"]
```

2.打包成dock而镜像
```
docker build -t flask1  -f dockerfile .
```

3.推送

4.运行
```
#内部端口是8085可修改
docker run -p 8085:8085 --name t1 -d flask1
```
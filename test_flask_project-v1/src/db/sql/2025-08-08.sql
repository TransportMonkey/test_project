CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

INFO  [alembic.runtime.migration] Running upgrade  -> 3d6f2793e583, empty message
-- Running upgrade  -> 3d6f2793e583

CREATE TABLE todo (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL COMMENT 'todo名称',
    done BOOL NOT NULL COMMENT '是否完成' DEFAULT '0',
    user_id INTEGER NOT NULL COMMENT '用户ID',
    PRIMARY KEY (id)
);

CREATE INDEX ix_todo_done ON todo (done);

CREATE INDEX ix_todo_name ON todo (name);

CREATE INDEX ix_todo_user_id ON todo (user_id);

CREATE TABLE user (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL COMMENT '用户名',
    age INTEGER NOT NULL COMMENT '年龄',
    gender INTEGER NOT NULL COMMENT '性别 1:男,2:女',
    email VARCHAR(80) NOT NULL COMMENT '邮箱',
    password VARCHAR(80) NOT NULL COMMENT '密码',
    PRIMARY KEY (id)
);

CREATE INDEX ix_user_email ON user (email);

CREATE INDEX ix_user_name ON user (name);

CREATE INDEX ix_user_password ON user (password);

INSERT INTO alembic_version (version_num) VALUES ('3d6f2793e583');

INFO  [alembic.runtime.migration] Running upgrade 3d6f2793e583 -> ad56bb7e87c9, empty message
-- Running upgrade 3d6f2793e583 -> ad56bb7e87c9

CREATE TABLE article (
    id INTEGER NOT NULL AUTO_INCREMENT,
    title VARCHAR(80) NOT NULL COMMENT '文章标题',
    content VARCHAR(80) NOT NULL COMMENT '文章内容',
    status BOOL COMMENT '是否发布' DEFAULT '1',
    visible BOOL COMMENT '文章可见范围' DEFAULT '1',
    user_id INTEGER NOT NULL COMMENT '用户ID',
    category_id INTEGER NOT NULL COMMENT '专栏ID',
    PRIMARY KEY (id)
);

CREATE INDEX ix_article_category_id ON article (category_id);

CREATE INDEX ix_article_status ON article (status);

CREATE INDEX ix_article_user_id ON article (user_id);

CREATE TABLE comment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    content VARCHAR(80) COMMENT '文章内容',
    user_id INTEGER NOT NULL COMMENT '评论者姓名',
    created_at DATETIME NOT NULL,
    article_id INTEGER NOT NULL COMMENT '被评论的文章ID',
    PRIMARY KEY (id)
);

CREATE INDEX ix_comment_article_id ON comment (article_id);

CREATE INDEX ix_comment_created_at ON comment (created_at);

CREATE TABLE postscategory (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL COMMENT '专栏名称',
    PRIMARY KEY (id)
);

CREATE INDEX ix_postscategory_name ON postscategory (name);

UPDATE alembic_version SET version_num='ad56bb7e87c9' WHERE alembic_version.version_num = '3d6f2793e583';

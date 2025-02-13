
windows的话就用cmd

python -m pip install -r requirements.txt  安装环境依赖，出现报错可以问我或者deepseek

出现报错基本上是有啥没装上去
----------------------------------------------------------------------------------------------------------------------------
database我用的是haroku https://dashboard.heroku.com/account  账号piperkun@gmail.com 密码Qq876883285 需要找我要验证码才能登上
安装完heroku客户端 https://cli-assets.heroku.com/channels/stable/heroku-x64.exe
然后安装sql https://get.enterprisedb.com/postgresql/postgresql-15.10-3-windows-x64.exe

就可以通过 cmd里的 heroku pg:psql postgresql-dimensional-72505 --app cc7940bottest 登录进数据库

使用 SELECT * FROM users;  可以 查看数据库数据

cc7940bottest::DATABASE=> SELECT * FROM users;
  user_id   | interests
------------+-----------
 8111480266 | {原神}
 7922960767 | {原神}
 8199140171 | {原神}
------------------------------------------------------------------------------------------------------------------------------

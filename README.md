# 基于flask的开发api框架

![pyversions](https://img.shields.io/badge/python%20-3.6%2B-blue.svg)

## 开发

### Use Docker

#### Install Docker

[Docker For Mac](https://www.docker.com/docker-mac)

[Docker For CentOs 7](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-centos-7)

#### Install Docker-Compose

```bash
(sudo) pip install -U docker-compose
```

#### Pull and run docker container

```bash
BUILD=y PULL=y ./tools/reset.sh
```

#### Reset

```bash
./tools/reset.sh
```

#### Restart server service

```bash
docker-compose restart backend
```

#### start server with debug

```bash
./tools/deploy.sh
```

#### Logs

```bash
docker-compose logs
```

#### Server Logs

```bash
docker-compose logs -f backend
```

### 运行环境

使用 Python 3.6 开发 

```shell
brew install python3
```

### 安装依赖

* 推荐使用 `virtualenv` + `virtualenvwrapper` 管理项目依赖，保持干净。
* 开发使用 `requirements-dev.txt`，包含代码检查、格式化、mysql 管理等依赖 

```shell
pip install -r requirements-dev.txt
```

### 创建数据库

```mysql
CREATE DATABASE `{db_name}` DEFAULT CHARACTER SET = `utf8mb4`;
```

### ORM 管理数据库

```shell
# 只有第一次需要使用
python manage.py db init
# 检查 model 是否更新
python manage.py db migrate
# 更新数据库
python manage.py db upgrade
```

### 运行

配置相关环境变量

```shell
cp app/local_config.py.template app/local_config.py
```

运行

```shell
python run.py
```

### 格式化代码

```shell
sh tools/format_python_code.sh
```

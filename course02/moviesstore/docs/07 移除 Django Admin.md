# 07 移除 Django Admin



## 一、硬移除的工程边界

**硬移除 ≠ 隐藏入口**

硬移除的含义是：

- `django.contrib.admin` **完全不参与项目**
- 不存在 `/admin/` 路由
- 不存在 admin 模板 / admin UI / admin 代码
- 所有 `admin.py` **不再被 Django 加载**
- 项目仍可：
    - `makemigrations`
    - `migrate`
    - `runserver`

**不会做的事**：

- 不 fake migration
- 不 hack Django 内部
- 不保留“将来可能用到”的 admin 代码（这是技术债）



## 二、第一步：移除依赖（settings.py）

### 2.1 修改 `config/settings.py`

#### 2.1.1 从 `INSTALLED_APPS` 中移除以下项

**必须全部移除：**

```python
# ❌ 删除
"django.contrib.admin",
"jazzmin",
```

#### 2.1.2 删除后的示例（保留必要组件）

```python
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "corsheaders",

    "apps.movie_auth",
    "apps.accounts",
    "apps.content",
    "apps.wallet",
    "apps.orders",
    "apps.membership",
    "apps.download",
]
```

> 说明
>
> - **admin 与 auth 是两个概念**
> - `django.contrib.auth` 必须保留
> - 只移除 admin，不影响用户系统

------

### 2.2 删除所有 Admin UI 配置

如果你之前配置过：

```python
JAZZMIN_SETTINGS = {...}
```

**整段删除**，不要注释。

------

## 三、第二步：清理路由（urls.py）

### 3.1 修改 `config/urls.py`

#### ❌ 删除所有 admin 相关内容

```python
# ❌ 删除
from django.contrib import admin
# ❌ 删除
path("admin/", admin.site.urls),
```

#### ✅ 示例（只保留业务路由）

```python
from django.urls import path, include

urlpatterns = [
    path("", include("movies.urls")),
]
```

------

### 3.2 验证（此时 /admin/ 必须 404）

```bash
python manage.py runserver
```

访问：

```
http://127.0.0.1:8000/admin/
```

结果应为：

- 404（推荐）
- 或你自定义的 Not Found 页面

------

## 四、第三步：清理 admin.py 文件（关键）

### 4.1 原则（非常重要）

- **admin.py 不再被 Django 加载**
- 但 **是否删除文件**，取决于工程规范

### 4.2 推荐规范（企业级）

> **保留空文件，不删除**

理由：

- 保持 app 结构完整
- 避免未来误判 app 是否“缺文件”
- Git 历史更清晰



### 4.3 对所有 app 执行以下操作

针对：

```
apps/movie_auth/admin.py
apps/accounts/admin.py
apps/content/admin.py
apps/wallet/admin.py
apps/orders/admin.py
apps/membership/admin.py
apps/download/admin.py
```

#### 统一改成（空实现）

```python
# admin.py
# Django Admin 已被硬移除
```

⚠️ **不要留 import / register / 自定义 view / URL**

------

## 五、第四步：删除 Admin 专用模板（必须）

你之前为钱包管理员充值写过：

```
templates/admin/wallet/wallet/adjust.html
```

### 5.1 必须删除整个 admin 模板目录

```text
templates/
└── admin/        ❌ 整个目录删除
```

理由：

- Django Admin 已被移除
- 这些模板不会再被使用
- 保留只会造成认知混乱

------

### 5.2 templates 目录仍然可以保留

```text
templates/
├── frontend/     ✅ 给 React 或前端页面
├── errors/       ✅ 404 / 500 页面
```

------

## 六、第五步：删除 admin 专用 forms / 逻辑（关键）

### 6.1 钱包模块的 admin 表单

之前你有：

```
apps/wallet/forms.py
```

其中包含：

```python
AdminCoinAdjustForm
```

这是 **Admin 专用表单**。

### 6.2 处理方式（必须做）

#### ❌ 删除 admin 表单

```python
# 删除 AdminCoinAdjustForm
```

#### ✅ 后续正确归属（先占位）

- 管理员充值逻辑 → **Service 层**
- 管理员充值入口 → **管理端 API**

> 这一点非常关键：
> **管理能力 ≠ Admin 表单**

------

## 七、第六步：确认迁移与 ORM 不受影响

### 7.1 执行系统检查

```bash
python manage.py check
```

必须无错误。

------

### 7.2 执行迁移（不会受 admin 影响）

```bash
python manage.py makemigrations
python manage.py migrate
```

如果这里报错，说明：

- 你还有 admin 代码被 import
- 或 settings / urls 没清干净

------

## 八、第七步：删除 admin 相关依赖（可选但推荐）

### 8.1 requirements.txt / poetry / pip-tools

删除：

```text
django-jazzmin
```

重新安装依赖：

```bash
pip install -r requirements.txt
```

------

## 九、第八步：管理能力如何“正确替代 admin”

这是**硬移除后必须马上规划的事**。

### 9.1 管理端能力清单（你项目已有）

- 用户：
    - 查看
    - 禁用/启用
- 内容：
    - 电影 CRUD
    - 上架 / 下架
- 资金：
    - 管理员充值 / 扣减
    - 流水审计
- 订单：
    - 订单查询
    - 授权查询
- 风控：
    - 下载 token
    - 下载配额

### 9.2 推荐技术路径（下一步）

**后端：**

- Django + DRF
- 管理 API（RBAC）

**前端：**

- React Admin / Ant Design Pro / 自研后台

------

## 十、最终验收清单（逐条对）

- `/admin/` 访问失败 ✅
- `django.contrib.admin` 不在 `INSTALLED_APPS` ✅
- 不存在 `templates/admin/` ✅
- 所有 `admin.py` 无代码或仅注释 ✅
- `makemigrations / migrate` 正常 ✅
- 项目可启动、无 SystemCheckError ✅


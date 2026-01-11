"""
API 自检脚本（幂等）

覆盖：
- Session 登录/登出
- Token 登录 + Profile
- JWT 登录 + Profile
- JWT Refresh

说明：
- Session 通过 requests.Session() 保持 cookie
- 用户依赖 init_data.py 创建（alice/123456）
"""

import requests

BASE = "http://127.0.0.1:8000/api"


def pretty(title, r: requests.Response):
    print("\n" + "=" * 70)
    print(title)
    print("status:", r.status_code)
    try:
        print("json:", r.json())
    except Exception:
        print("text:", r.text)


def main():
    # Session flow
    s = requests.Session()
    r = s.post(f"{BASE}/auth/session/login/", json={"username": "alice", "password": "123456"})
    pretty("POST /auth/session/login/", r)

    r = s.get(f"{BASE}/profile/")
    pretty("GET /profile/ (session)", r)

    r = s.post(f"{BASE}/auth/session/logout/", json={})
    pretty("POST /auth/session/logout/", r)

    # Token flow
    r = requests.post(f"{BASE}/auth/token/login/", json={"username": "alice", "password": "123456"})
    pretty("POST /auth/token/login/", r)
    token = r.json()["data"]["token"]

    r = requests.get(f"{BASE}/profile/", headers={"Authorization": f"Token {token}"})
    pretty("GET /profile/ (token)", r)

    # JWT flow
    r = requests.post(f"{BASE}/auth/jwt/login/", json={"username": "alice", "password": "123456"})
    pretty("POST /auth/jwt/login/", r)
    access = r.json()["data"]["access"]
    refresh = r.json()["data"]["refresh"]

    r = requests.get(f"{BASE}/profile/", headers={"Authorization": f"Bearer {access}"})
    pretty("GET /profile/ (jwt access)", r)

    r = requests.post(f"{BASE}/auth/jwt/refresh/", json={"refresh": refresh})
    pretty("POST /auth/jwt/refresh/", r)
    new_access = r.json()["data"]["access"]

    r = requests.get(f"{BASE}/profile/", headers={"Authorization": f"Bearer {new_access}"})
    pretty("GET /profile/ (jwt new access)", r)

    print("\n[done] api check finished")


if __name__ == "__main__":
    main()
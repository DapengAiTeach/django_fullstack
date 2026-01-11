"""
API 自检脚本（幂等，不污染数据库）

策略：
- 使用固定 title 作为幂等键，确保多次运行不会创建无限数据
- 覆盖所有 API：
  - list/create/retrieve/patch/delete
  - 校验错误（40001）
  - 业务异常（40901/40902）
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


def list_tickets():
    r = requests.get(f"{BASE}/tickets/")
    pretty("GET /tickets/", r)
    r.raise_for_status()
    return r.json()["data"]


def ensure_ticket():
    """
    幂等创建：
    - 若存在同名 title 则复用
    - 否则创建一个 OPEN 工单
    """
    tickets = list_tickets()
    for t in tickets:
        if t["title"] == "API自检工单":
            return t["id"]

    payload = {
        "title": "API自检工单",
        "description": "这是用于 API 自检的工单描述。",
        "priority": 3,
        "status": "OPEN",
    }
    r = requests.post(f"{BASE}/tickets/", json=payload)
    pretty("POST /tickets/ (ensure)", r)
    r.raise_for_status()
    return r.json()["data"]["id"]


def main():
    # list
    list_tickets()

    # create / ensure
    ticket_id = ensure_ticket()
    print("\nensure_ticket id:", ticket_id)

    # retrieve
    r = requests.get(f"{BASE}/tickets/{ticket_id}/")
    pretty("GET /tickets/{id}/", r)

    # patch: 合法更新
    r = requests.patch(f"{BASE}/tickets/{ticket_id}/", json={"priority": 4})
    pretty("PATCH /tickets/{id}/ (valid)", r)

    # trigger validation error: priority out of range
    r = requests.patch(f"{BASE}/tickets/{ticket_id}/", json={"priority": 99})
    pretty("PATCH /tickets/{id}/ (validation_error)", r)

    # create CLOSED without assignee -> object-level validation
    payload = {
        "title": "API自检关闭但无邮箱",
        "description": "用于触发对象级校验。",
        "priority": 3,
        "status": "CLOSED",
    }
    r = requests.post(f"{BASE}/tickets/", json=payload)
    pretty("POST /tickets/ (object_level_validation)", r)

    # business exception: rollback CLOSED->OPEN
    # 确保一个 CLOSED 工单存在（幂等：固定 title）
    tickets = list_tickets()
    closed_id = None
    for t in tickets:
        if t["title"] == "API自检已关闭工单":
            closed_id = t["id"]
            break

    if closed_id is None:
        payload = {
            "title": "API自检已关闭工单",
            "description": "用于触发业务异常回退。",
            "priority": 2,
            "status": "CLOSED",
            "assignee_email": "ops@example.com",
        }
        r = requests.post(f"{BASE}/tickets/", json=payload)
        pretty("POST /tickets/ (create closed)", r)
        r.raise_for_status()
        closed_id = r.json()["data"]["id"]

    r = requests.patch(f"{BASE}/tickets/{closed_id}/", json={"status": "OPEN"})
    pretty("PATCH /tickets/{closed_id}/ (business rollback)", r)

    # business exception: delete CLOSED
    r = requests.delete(f"{BASE}/tickets/{closed_id}/")
    pretty("DELETE /tickets/{closed_id}/ (business delete)", r)

    print("\n[done] api check finished")


if __name__ == "__main__":
    main()
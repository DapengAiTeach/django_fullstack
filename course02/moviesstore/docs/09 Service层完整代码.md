# 09 Service层完整代码

services/
├── common/
│   ├── exceptions.py
│   └── base.py
├── domain/
│   ├── movie_service.py
│   ├── identity_service.py
│   ├── user_service.py
│   ├── wallet_service.py
│   ├── order_service.py
│   ├── license_service.py
│   ├── membership_service.py
│   └── download_service.py
└── core/
    ├── purchase_flow.py
    ├── membership_flow.py
    └── download_flow.py
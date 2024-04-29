# Delivery_db
Delivery Database

## 📌Introduction

### Service Info
▶️ 판매자와 구매자, 배달대행자를 연결해주는 앱과 서비스를 개발하는 시나리오
  
### Project Goal
1️⃣ 판매자(seller) 가게(store) 구매자(customer) 배달부(delivery) DB를 가지고 시나리오 만들기 <br>
2️⃣ 시나리오 기반으로 앱 개발

<br>
     
## 🖥️Model

### Dataset
- 데이터: example 폴더

### Modeling
- 설치 필요
''''
psycopg2_binary
#pip install --upgrade pip
#pip install psycopg2-binary
''''

<br>

## 💻Technology Stack
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) <br>
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) 

<br>

## 📑Scenario
- 1명의 Seller는 0개 이상의 Store을 가지고 있으며 각 Store는 1개 이상의 Menu를 판매한다.
- 각 메뉴는 특정한 하나의 Store에서만 판다.
- Customer는 Store를 검색하고 그 Store에서 판매하는 여러 개의 Menu를 골라 구매하는 것으로 Order를 생성할 수 있다.
- Order가 생성되면 Seller는 Order를 확인하고 메뉴를 발송한다.
- Order가 Store의 위치와 가장 가까운 배달부에게 배송이 할당된다.
- Customer는 배달된 물건을 받고(가정하고) 물건을 확인Confirm하는 것으로 Order는 종결된다.


<br>


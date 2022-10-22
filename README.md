![API Store](https://gonzch.com/img/cloud/online_store/logo_api_store.png)

# RESTful API - Online Store

This is the official repository of the “ABC SAC” company's backend application.

## Overview

The backend application is a RESTful API based on a wholesale distributor that sells products on demand. This API will allow the distributor to integrate its website or mobile application; in addition to facilitating integration with other wholesale trading platforms.

## Content

* [Tech Stack](#techstack)
* [Architecture](#architecture)
* [Code Structure](#code_structure)
* [Requeriments](#requirements)
* [Environment Variables](#env)
* [Unit Test](#codeTest)
* [Code Quality](#codeQuality)
* [Database Entity Model](#dbmodel)
* [Database Information](#dbinfo)
* Endpoints:
    * [API Login](#endpointLogin)
    * [API Token](#endpointToken)
    * [API Logout List](#endpointLogout)
    * [API Customer List](#endpointCustomer)
    * [API Customer Create](#endpointCustomer)
    * [API Customer Search](#endpointCustomer)
    * [API Customer Update](#endpointCustomer)
    * [API Customer Desactive](#endpointCustomer)
    * [API Customer Restore](#endpointCustomer)
	* [API Customer Category List](#endpointCustomerCategory)
	* [API Customer Category Create](#endpointCustomerCategory)
	* [API Customer Category Update](#endpointCustomerCategory)
	* [API Customer Category Desactive](#endpointCustomerCategory)
	* [API Customer Category Restore](#endpointCustomerCategory)
	* [API Customer Category Search](#endpointCustomerCategory)
	* [API Delivery List](#endpointDelivery)
	* [API Delivery Create](#endpointDelivery)
	* [API Delivery Update](#endpointDelivery)
	* [API Delivery Desactive](#endpointDelivery)
	* [API Delivery Restore](#endpointDelivery)
	* [API Delivery Search](#endpointDelivery)
	* [API District List](#endpointDistrict)
	* [API District Create](#endpointDistrict)
	* [API District Update](#endpointDistrict)
	* [API District Desactive](#endpointDistrict)
	* [API District Restore](#endpointDistrict)
	* [API District Search](#endpointDistrict)
    * [API Order Detail List](#endpointOrderDetail)
	* [API Order Detail Create](#endpointOrderDetail)
	* [API Order Detail Update](#endpointOrderDetail)
	* [API Order Detail Desactive](#endpointOrderDetail)
	* [API Order Detail Restore](#endpointOrderDetail)
	* [API Order Detail Search](#endpointOrderDetail)
	* [API Order List](#endpointOrder)
	* [API Order Create](#endpointOrder)
	* [API Order Update](#endpointOrder)
	* [API Order Desactive](#endpointOrder)
	* [API Order Restore](#endpointOrder)
	* [API Order Search](#endpointOrder)
	* [API Product Category List](#endpointProductCategory)
	* [API Product Category Create](#endpointProductCategory)
	* [API Product Category Update](#endpointProductCategory)
	* [API Product Category Desactive](#endpointProductCategory)
	* [API Product Category Restore](#endpointProductCategory)
	* [API Product Category Search](#endpointProductCategory)
	* [API Product List](#endpointProduct)
	* [API Product Create](#endpointProduct)
	* [API Product Update](#endpointProduct)
	* [API Product Desactive](#endpointProduct)
	* [API Product Restore](#endpointProduct)
	* [API Product Search](#endpointProduct)
* [Postman API Platform](#postman)

<a name="techstack"></a>
## Tech Stack

- **RESTful API:** RESTful API written in Python on the Django framework.
- **Transactional Database:** MySQL Server version 8.0.30
- JWT encrypted with public/private key using RSA algorithm.

<a name="architecture"></a>
## Architecture

The architecture implemented consists of:

![image Arquitectura Backend](https://gonzch.com/img/cloud/online_store/arquitectura_backend_products.png)

### Architecture Components

* **RESTful API:** Backend application that implements a communication interface so that external applications can consume information related to the company's products.

* **MySQL Database:** Transactional database, where in addition to products, it can manage purchase orders, sales, delivery, customers, suppliers, billing, collections, among other information entities.

### About Communication

* Communication is **HTTPS**.

* The **JWT** issued by the backend application is signed with a private key using
the **HS256 algorithm**.

<a name="code_structure"></a>
## Code Structure

![image Code Structure](https://gonzch.com/img/cloud/online_store/code_structure_v1.png)

<a name="requirements"></a>
## Requirements

- Python 3.10.7
- MySQL 8.0.30

<a name="npm"></a>
## Python Libraries

asgiref==3.5.2
autopep8==1.7.0
certifi==2022.9.24
charset-normalizer==2.1.1
coreapi==2.3.3
coreschema==0.0.4
Django==4.1.2
django-cors-headers==3.13.0
django-debug-toolbar==3.7.0
django-filter==22.1
djangorestframework==3.14.0
djangorestframework-simplejwt==5.2.1
drf-yasg==1.21.4
idna==3.4
inflection==0.5.1
itypes==1.2.0
Jinja2==3.1.2
MarkupSafe==2.1.1
mysqlclient==2.1.1
packaging==21.3
pycodestyle==2.9.1
PyJWT==2.5.0
pyparsing==3.0.9
pytz==2022.4
requests==2.28.1
ruamel.yaml==0.17.21
ruamel.yaml.clib==0.2.7
sqlparse==0.4.3
toml==0.10.2
tzdata==2022.5
uritemplate==4.1.1
urllib3==1.26.12

<a name="env"></a>
## Environment Variables

```bash
# APP
APP_URL=http://localhost:8000

# ROWS_PER_PAGE
APP_ROWS_PER_PAGE=5

# SERVER
SERVER_PORT=8000

# ORIGIN CORS
ORIGIN_URL='http://localhost:8000'

# JWT AUTH TOKEN
TOKEN_EXPIRE_TIME='90min'
TOKEN_ALGORITHM='HS256'

# TRANSACTIONAL DATABASE
DB_MYSQL_HOST=''
DB_MYSQL_USER=''
DB_MYSQL_PASS=''
DB_MYSQL_PORT=3306
DB_MYSQL_DB='db'
DB_MYSQL_CONNECTION_LIMIT=100
```


REST API in production: 

# Project Documentation

<a name="dbmodel"></a>
## Database Entities Model

The company works with a relational transactional database to store and organize its sales information.

Therefore, a basic entity model of a relational database was defined to cover the scope of the project: develop an API to consume information from the products of the distribution company.

![image Model Database](https://gonzch.com/img/cloud/online_store/model_database.png)

For practical purposes, a database of 20,389 products was created for test. In the "db" folder of this repository you can download a backup of this database. 

<a name="dbinfo"></a>
### Database information

Number of records per table

![image Database Information](https://gonzch.com/img/cloud/online_store/db_01.jpg)

Size of each table

![image Database Information](https://gonzch.com/img/cloud/online_store/db_02.jpg)

**Table: Product Category**

![image Table Product Category](https://gonzch.com/img/cloud/online_store/db_03.jpg)

**Table: Product**

Fragment of the products table content

![image Table Product](https://gonzch.com/img/cloud/online_store/db_04.jpg)

**Table: User**

![image Table Product](https://gonzch.com/img/cloud/online_store/db_05.jpg)

## Endpoints

### Endpoint: Customer List
```
GET /customer
```
This endpoint is used to return the paginated customer list with 5 items.

Example Response:

```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "company_name": "Cinco Tenedores",
            "ruc": "20664585121",
            "customer_category": "Restaurantes",
            "district": "San Isidro",
            "updated_by": "toshi",
            "updated_at": "22-10-22 02:01:00"
        },
        {
            "id": 2,
            "company_name": "Okashi Restaurant",
            "ruc": "20601145852",
            "customer_category": "Restaurantes",
            "district": "Miraflores",
            "updated_by": "admin",
            "updated_at": "22-10-22 02:01:28"
        },
        {
            "id": 3,
            "company_name": "Hotel Palermo",
            "ruc": "20365265851",
            "customer_category": "Hoteles",
            "district": "San Borja",
            "updated_by": "toshi",
            "updated_at": "22-10-22 02:02:31"
        },
        {
            "id": 4,
            "company_name": "Mini Market San Blas",
            "ruc": "10426545201",
            "customer_category": "Tiendas",
            "district": "Surquillo",
            "updated_by": "admin",
            "updated_at": "22-10-22 02:02:58"
        },
        {
            "id": 5,
            "company_name": "Supermarket Las Vegas",
            "ruc": "20115245110",
            "customer_category": "Tiendas",
            "district": "San Borja",
            "updated_by": "admin",
            "updated_at": "22-10-22 02:03:30"
        }
    ]
}
```

### Endpoint: Customer Create
```
POST /customer/
```
This endpoint is used to register customers.

Body:

```json
{
    "company_name": 'Supermarket Las Vegas',
    "ruc": 20115245110,
    "costumer_category": 3,
    "district": 3,
}
```
Response:
```json
{
    "id": 5,
    "company_name": "Supermarket Las Vegas",
    "ruc": "20115245110",
    "customer_category": "Tiendas",
    "district": "San Borja",
    "updated_by": "admin",
    "updated_at": "22-10-22 02:03:30"
}
```

### Endpoint: Customer Search
```
GET /customer/3/
```
This endpoint is used to look up customers.

Example Response:

```json
{
    "id": 3,
    "company_name": "Hotel Palermo",
    "ruc": "20365265851",
    "customer_category": "Hoteles",
    "district": "San Borja",
    "updated_by": "toshi",
    "updated_at": "22-10-22 02:02:31"
}
```

### Endpoint: Customer Update
```
PATH /customer/3/
```
This endpoint is used to update customer fields.

Example Response:

```json
{
    "company_name": "Hotel Palermo",
    "ruc": "20365265851",
}
```

### Endpoint: Customer Update
```
PUT /customer/3/desactivate/
```
This endpoint is used to disable the customer.

Example Response:

```json
{"message": "Cliente eliminado"}
```

### Endpoint: Customer Update
```
PUT /customer/3/restore/
```
This endpoint is used to restore the disabled customer.

Example Response:

```json
{"message": "Cliente restaurado"}
```


### Endpoint: Product List
```
GET /products/
```
This endpoint is used to return paginated products with 5 items.

Example Response:

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "updated_at": "22-10-22 03:09:14",
            "code": "100002",
            "name": "AZÚCAR RUBIA BOLSA 10KG",
            "base_sale_price": "38.50",
            "percent_discount": 5,
            "discount_amount": "1.93",
            "sale_price": "36.57",
            "stock": 77,
            "updated_by": "toshi",
            "product_category": 1,
            "unit_measure": 2,
            "currency": 1
        },
        {
            "id": 1,
            "updated_at": "22-10-22 02:46:30",
            "code": "100001",
            "name": "GASEOSA INCA KOLA BOTELLA 1L",
            "base_sale_price": "4.70",
            "percent_discount": 5,
            "discount_amount": "0.24",
            "sale_price": "4.46",
            "stock": 6,
            "updated_by": "admin",
            "product_category": 1,
            "unit_measure": 1,
            "currency": 1
        }
    ]
}
```

### Endpoint: Product Create
```
POST /products/
```
This endpoint is used to return the product.

Body:
```json
	{
        "code": "100002",
        "name": "AZÚCAR RUBIA BOLSA 10KG",
        "base_sale_price": "38.50",
        "percent_discount": 5,
        "sale_price": "36.57",
        "stock": 77,
        "product_category": 1,
        "unit_measure": 2,
        "currency": 1
    }
```
Response:

```json
	{
        "id": 2,
        "updated_at": "22-10-22 03:09:14",
        "code": "100002",
        "name": "AZÚCAR RUBIA BOLSA 10KG",
        "base_sale_price": "38.50",
        "percent_discount": 5,
        "discount_amount": "1.93",
        "sale_price": "36.57",
        "stock": 77,
        "updated_by": "toshi",
        "product_category": 1,
        "unit_measure": 2,
        "currency": 1
    }
```

### Endpoint: Order List
```
GET /order/
```
This endpoint is used to return the order and its details.

Example Response:

```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "code": "202200004",
            "date": "2022-05-19",
            "total_discount": 5.49,
            "total_subtotal": 104.22,
            "igv": 18.76,
            "total": 122.98,
            "customer": "Okashi Restaurant",
            "date_delivery": "2022-05-19"
        },
        {
            "id": 3,
            "code": "202200003",
            "date": "2022-05-19",
            "total_discount": 5.0,
            "total_subtotal": 59.32,
            "igv": 10.68,
            "total": 70.0,
            "customer": "Cinco Tenedores",
            "date_delivery": "2022-05-19"
        },
        {
            "id": 2,
            "code": "202200002",
            "date": "2022-05-19",
            "total_discount": null,
            "total_subtotal": null,
            "igv": 0,
            "total": 0,
            "customer": "Cinco Tenedores",
            "date_delivery": "2022-05-19"
        },
        {
            "id": 1,
            "code": "202200001",
            "date": "2022-05-19",
            "total_discount": 5.0,
            "total_subtotal": 203.38,
            "igv": 36.61,
            "total": 239.99,
            "customer": "Cinco Tenedores",
            "date_delivery": "2022-05-19"
        }
    ]
}
```

### Endpoint: Order Create
```
POST /order/
```
This endpoint is used to record the order and its details.

Body:

```json
{
    "cliente": 1,
    "status": false,
    "delivery": {
        "address": "xxxxxxx",
        "date": "2022-05-19",
        "district": 1
    },
    "details": [
        {
            "product": 1,
            "quantity": 48
        },
        {
            "product": 2,
            "quantity": 10
        },
        {
            "product": 2,
            "quantity": 15
        }
    ]
}
```
Response:
```json
{
	"mensaje": "Orden creada exitosamente"
}
```

### Endpoint: Order Update
```
PUT /order/1/
```
This endpoint is used to update the order.

Body:

```json
{
    "code": "202200001",
    "date": "2022-05-19",
    "total_discount": 5.0,
    "total_subtotal": 203.38,
    "igv": 36.61,
    "total": 239.99,
    "customer": "Cinco Tenedores",
    "date_delivery": "2022-05-19"
}
```
Response:

```json
```

### Endpoint: Order Search
```
GET /order/1/
```
This endpoint is used to look up the order.

Example Response:

```json
{
    "id": 1,
    "code": "202200001",
    "date": "2022-05-19",
    "total_discount": 5.0,
    "total_subtotal": 203.38,
    "igv": 36.61,
    "total": 239.99,
    "customer": "Cinco Tenedores",
    "date_delivery": "2022-05-19"
}
```
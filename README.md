# Exercise 1: Implement a REST API with Python

## Task
Implement a REST API with Python that provides the following information:

### API Endpoints

#### `/api/articles`
**Method:** GET  
**Description:** Lists all storable products (articles) in the database.  

**Example Response:**  
```json
[
    {"id": 1, "name": "Starter-Set charcoal"},
    {"id": 2, "name": "Starter-Set white"}
]
```

#### `/api/articles/{id}`
**Method:** GET  
**Description:** Retrieves specific properties of a given product (article).

**Example Response:**  
```json
{
    "id": 1,
    "name": "Starter-Set charcoal",
    "description": "Starter-Satin Charcoal-two pods"
}
```

#### `/api/wh_valuation/{wh-id}`
**Method:** GET  
**Description:** Lists the total cost of products by location within a chosen warehouse.

**Example Response:**  
```json
{
    "id": 2,
    "name WH": "ISSY (Main WH)",
    "total_cost": 6000,
    "locations": [
        {
            "name": "Name of loc1",
            "total_cost_products": 2000
        },
        {
            "name": "Name of loc1/1",
            "total_cost_products": 1700
        },
        {
            "name": "Name of loc1/1/1",
            "total_cost_products": 700
        },
        {
            "name": "Name of loc1/1/2",
            "total_cost_products": 1000
        },
        {
            "name": "Name of loc1/2",
            "total_cost_products": 300
        }
    ]
}
```

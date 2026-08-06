# Data Dictionary

Source: `26S1_ASSN1_dataset_data_dictionary.xlsx`. Same base schema across all six scenario datasets — see `table_relationships.md` for the `_set_1x` naming convention and how to map a scenario-suffixed table name back to the base table below.

## customers*.csv — Order-level customer snapshot table

| Column | Description |
|---|---|
| customer_id | Unique customer-session identifier linked to a specific order |
| customer_unique_id | Persistent customer identifier used for repeat purchase analysis |
| customer_name | Generated full name |
| customer_gender | M / F |
| customer_age | Age between 18 and 70 |
| customer_zip_code_prefix | ZIP code prefix |
| customer_city | Customer city |
| customer_state | Customer state |
| customer_segment | VIP, Corporate, Consumer |

## orders*.csv — Core table describing the order lifecycle and delivery process

| Column | Description |
|---|---|
| order_id | Unique order identifier |
| customer_no | Reference to customers table |
| order_status | delivered or canceled |
| order_purchase_timestamp | Purchase datetime |
| order_approved_at | Payment approval timestamp |
| order_delivered_carrier_date | Carrier handoff timestamp |
| order_delivered_customer_date | Final delivery timestamp |
| order_estimated_delivery_date | Estimated delivery date for delay comparison |

## order_items*.csv — Item-level order details

| Column | Description |
|---|---|
| order_no | Reference to orders table |
| order_item_id | Sequential number of items in the same order |
| product_no | Reference to products table |
| seller_no | Reference to sellers table |
| shipping_limit_date | Deadline for seller shipment |
| freight_value | Shipping cost based on distance and weight |
| discount_rate | Applied discount rate |

## products*.csv — Product metadata and physical specifications

| Column | Description |
|---|---|
| product_id | Unique product identifier |
| product_category_name | electronics, furniture, fashion, home_goods, toys, books, auto |
| product_name | Generated realistic product name |
| product_brand | Brand name |
| product_weight_g | Product weight in grams |
| product_length_cm | Product length in centimeters |
| product_height_cm | Product height in centimeters |
| product_width_cm | Product width in centimeters |
| cost | Simulated manufacturing cost |
| price | Base retail price |

## sellers*.csv — Seller master data

| Column | Description |
|---|---|
| seller_id | Unique seller identifier |
| seller_company_name | Generated company name |
| seller_contact_name | Generated seller contact name |
| seller_contact_gender | M / F |
| seller_contact_age | Age between 18 and 70 |
| seller_zip_code_prefix | Seller ZIP code prefix |
| seller_city | Seller city |
| seller_state | Seller state |

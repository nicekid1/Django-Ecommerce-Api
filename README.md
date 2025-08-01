#  Django E-Commerce Store

A fully functional e-commerce RESTful API built with Django, Django REST Framework, PostgreSQL, JWT authentication, and Zarinpal sandbox payment gateway.

##  Features

###  User Authentication & Management
- User registration, login, logout
- JWT-based authentication
- Profile viewing and updating
- Role-based access (admin, user)
- Optional email verification

###  Product Management
- CRUD operations for products (admin-only)
- Product categories
- Product attributes (e.g. color, brand, weight)
- Multi-image support
- Product search (Trigram similarity)
- Filtering and ordering by price/date

###  Shopping Cart
- Add/remove/update items in cart
- View user's cart
- View cart total
- Admin access to specific user's cart

###  Order System
- Create order from cart
- Order items persisted separately
- Order status tracking: `pending`, `paid`, `processing`, `shipped`, `delivered`, `cancelled`
- Order history per user
- Admin can update order status

###  Online Payment Integration
- Zarinpal (sandbox) integration
- Start payment from order
- Verify payment and update order status
- Handle canceled or failed payments

###  Admin Panel
- Manage users, products, categories, orders
- Filter, search, and inline admin features
- View order items directly in order page

###  Email Notifications
- Send confirmation email after order
- Send email on status change (e.g. payment, shipped)
- (Optional) Invoice via email

###  Product Search & Filter
- Search by product name or description
- Filter by category, price, attributes
- Order by price or creation date

###  RESTful API
- All features accessible via clean, token-secured REST API
- Built with `ViewSets` and `Routers` from DRF

---

##  Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (SimpleJWT)
- **Payment Gateway:** Zarinpal (sandbox mode)
- **Filtering & Search:** django-filter, Postgres Trigram similarity
- **Email:** Django Email backend (console or SMTP)
- **Deployment-ready:** Easily extendable to production with docker, gunicorn, nginx

---


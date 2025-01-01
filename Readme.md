# **Django Order Management System**

This project is a Django-based order management system that allows administrators and customers to manage and interact with orders. The system uses a robust permission design pattern for access control and is containerized using Docker for easy setup and deployment.

---

## **Design Pattern for Permissions**

### **Design Pattern Used**
The project uses the **Role-Based Access Control (RBAC)** design pattern for managing permissions. In this approach:
- **Roles** (e.g., Admin, Customer) are assigned to users.
- Permissions are defined based on roles, and access to specific views or actions is restricted accordingly.

### **Efficiency**
- **Scalability**: RBAC scales well as new roles and permissions can be easily added without modifying existing logic.
- **Centralized Management**: Permissions are centrally managed, making it easier to maintain and audit.
- **Security**: By assigning permissions to roles instead of individual users, the system reduces the risk of misconfigured access.

### **Extending with Strategy Pattern**
To further enhance the system, the **Strategy Pattern** could be combined with the RBAC approach. This would allow implementing different permission strategies for different apps or modules. For example:
- A **default permission strategy** for most apps.
- A **custom permission strategy** for apps with unique access requirements (e.g., an app with hierarchical permissions).

#### Example:
- Define a base `PermissionStrategy` class with common methods like `has_permission`.
- Implement specific strategies for different apps or modules (e.g., `OrderPermissionStrategy`, `UserPermissionStrategy`).
- Dynamically select the strategy based on the app or module being accessed.

This approach provides flexibility and modularity, making it easier to manage complex permission requirements.

---

## **Project Setup**

### **Prerequisites**
Ensure you have the following installed on your system:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)

---

### **Steps to Set Up the Project**

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Create a `.env` File**
   Create a `.env` file in the root directory with the following content:
   ```env
   SECRET_KEY=django-insecure-4j91g5a3(5s(cspy$d-)&)9rfg^(vy2f$4xnpmyt1!ghvnht3p
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```

3. **Build and Start the Docker Containers**
   Run the following command to build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. **Apply Migrations**
   After the containers are up, apply the migrations to set up the database schema:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create a Superuser (Optional)**
   If you need to create a superuser for accessing the Django admin panel:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Load Initial Data**
   Import the provided fixture data:
   ```bash
   docker-compose exec web python manage.py loaddata <fixture_file_name>.json
   ```

7. **Access the Application**
   - The application will be accessible at: [http://localhost:8000](http://localhost:8000)
   - Django admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## **User Credentials**

The following users have been preloaded into the system:

| **Username**    | **Role**           | **Password**   |
|------------------|--------------------|----------------|
| `admin`         | Django Admin       | `123456`       |
| `simple_admin`  | System Admin       | `1qaz@QAZ`     |
| `customer`      | Customer           | `1qaz@QAZ`     |
| `customer2`     | Customer           | `1qaz@QAZ`     |

---

## **URLs and Their Descriptions**

The following table provides an overview of the URLs available in the system:

| **URL**                | **HTTP Method** | **Description**                                                                 |
|------------------------|-----------------|---------------------------------------------------------------------------------|
| `/orders/`             | `GET`          | List all orders (Admin) or list own orders (Customer).                         |
| `/orders/`             | `POST`         | Create a new order (Customer).                                                 |
| `/orders/<id>/`        | `GET`          | Retrieve details of a specific order.                                          |
| `/orders/<id>/`        | `PUT`          | Update an order (Admin only).                                                  |
| `/orders/<id>/`        | `DELETE`       | Delete an order (Admin only).                                                  |
| `/orders/filter/`      | `GET`          | Filter orders by date range (Admin only).                                      |
| `/admin/`              | `GET`          | Access the Django admin panel.                                                 |

---

## **Running Test Cases**

To run the test cases, use the following command:
```bash
docker-compose exec web python manage.py test
```

This will execute all the test cases and display the results.

---

## **Importing Fixture Data**

Fixture data can be imported using the `loaddata` management command. This is useful for preloading the database with sample data.

1. Ensure the fixture file is in JSON format and placed in the appropriate directory.
2. Run the following command to load the fixture:
   ```bash
   docker-compose exec web python manage.py loaddata <fixture_file_name>.json
   ```

Example:
```bash
docker-compose exec web python manage.py loaddata initial_data.json
```

---

## **Project Architecture**

### **Apps**
- **Users**: Manages user accounts and roles (e.g., Admin, Customer).
- **Orders**: Handles order-related functionality.

### **Permissions**
The project uses **Role-Based Access Control (RBAC)** to restrict access to views and actions based on user roles.

### **Database**
The project uses **PostgreSQL** as the database, which is containerized using Docker.

---

## **Extending the System**

### **Combining with Strategy Pattern**
To implement different permission strategies for different apps, the system can use the **Strategy Pattern**. For example:
1. Create a base `PermissionStrategy` class.
2. Implement specific strategies for different apps (e.g., `OrderPermissionStrategy`, `UserPermissionStrategy`).
3. Dynamically assign the strategy based on the app or module being accessed.

This approach enhances modularity and allows for greater flexibility in managing permissions.

---

## **Contributing**

If you'd like to contribute to the project:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## **License**

This project is licensed under the MIT License.


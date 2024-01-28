# DjangoEcommerceShop
 
## About The Project
<p>Development of an online store in Django with
Stripe payment integration for secure and
convenient online transactions. UX/UI
optimization, shopping cart and ordering system
for maximum customer convenience
</p>
<p>Website url: <a href="https://kold.pythonanywhere.com/">Link</a></p>
<img src="https://github.com/IvanVoloshanskyi/DjangoEcommerceShop/assets/93157729/6eee36aa-3239-4e56-a341-bed0984ec0f6" style="width: 100%;">
<img src="https://github.com/IvanVoloshanskyi/DjangoEcommerceShop/assets/93157729/51b0cd29-5f0f-4c5d-89f5-ac8f8dfa7d69" style="width: 100%;">
<p align="center" >
  <img src="https://github.com/IvanVoloshanskyi/DjangoEcommerceShop/assets/93157729/4dc753c5-1175-4c4c-9251-d033f8d96d23">
  <img src="https://github.com/IvanVoloshanskyi/DjangoEcommerceShop/assets/93157729/b7befb4b-3f8e-4639-b552-aa6a62df7cde">
</p>
<p>The mobile layout was designed for phones with a 6.1-inch screen.</p>
<p>Best for all iPhones of the "pro" version</p>

### Built With

* Python
* Django
* MYSQL
* Stripe


## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/IvanVoloshanskyi/DjangoEcommerceShop.git
   ```
2. Install python packages
   ```sh
   pip install -r requirements.txt
   ```
3. Create .env file and enter your data from ".env-samples" file `.env`
   ```python
   DB_NAME=ENTER YOUR DATABASE NAME;
   ```

4. Create migrations to your DB
   ```sh
   python manage.py makemigrations
   ```
   ```sh
   python manage.py migrate
   ```
   
5. Run project
   ```sh
   python manage.py runserver
   ```

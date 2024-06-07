## installing

#### 1.clone repository
```sh
git clone git@github.com:danialsadri/multi_shop_project.git
```

#### 2.change directory
```sh
cd multi_shop_project
```

#### 3.setup virtualenv
```sh
python3 -m venv venv
source venv/bin/activate
```

#### 4.install packages
```sh
pip install -r requirements.txt
```

#### 5.make migrations & migrate
```sh
python manage.py makemigrations
python manage.py migrate
```

#### 6.create superuser
```sh
python manage.py createsuperuser
```

#### 7.start server
```sh
python manage.py runserver
```

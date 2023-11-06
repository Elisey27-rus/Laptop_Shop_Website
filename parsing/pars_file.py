from bs4 import BeautifulSoup
import requests as req
import os
import sqlite3

class ParsClass:

    def __init__(self, url, page):
        lst_with_urls = self.func_get_urls(url, page)
        for url_to_product in lst_with_urls:
            dct_product = self.func_get_full_info(url_to_product)
            dct_product = list(dct_product.values())[0]
            name, price, about, href = dct_product[0].values()
            self.load_image(href)
            reviews = dct_product[1]
            with sqlite3.connect('../mysite/db.sqlite3') as connect:
                cursor = connect.cursor()
                sql = """
                INSERT INTO shop_product(product_name, product_description, product_price, product_image, product_category_id)
                VALUES("{name}", "{about}", "{price}", "{file_name}", "{category_id}")
                """.format(name=name, about='\n'.join(about), price=price, file_name=href.split('/')[-1], category_id=9)
                print(sql)
                cursor.execute(sql)
                connect.commit()

    @staticmethod
    def load_image(href):
        r = req.get(href)
        if r.status_code == 200:
            filename = href.split('/')[-1]
            image_folder = "/Users/elisey27/Desktop/Python/Elisey_and_Miron_Shop777/mysite/uploads/products"
            if not os.path.exists(image_folder):
                os.makedirs(image_folder)
            filepath = os.path.join(os.getcwd(), image_folder, filename)
            with open(filepath, "wb") as file:
                file.write(r.content)
            print("Картинка успешно сохранена.")
        else:
            print("Не удалось загрузить картинку.")

    @staticmethod
    def func_get_urls(url, page):
        params = {'page': page}
        r = req.get(url, params=params)
        soup = BeautifulSoup(r.text, "html.parser")
        lst_with_urls = []
        for el in soup.find('div', class_="row-viewed col-catalog-grid product-grid").find_all('a'):
            try:
                res_url = el.get('href')
                if res_url is not None:
                    lst_with_urls.append(res_url)
            except AttributeError:
                pass
        return lst_with_urls

    @staticmethod
    def func_get_detail(url_to_product):
        r = req.get(url_to_product)
        soup = BeautifulSoup(r.text, "html.parser")
        name = soup.find('div', class_="col-lg-60 col-xs-60").text.strip()
        price = soup.find('span', class_="item-price").text.strip()[5:-2].replace(' ', '')
        about = [el.text.strip() for el in soup.find('div', id="tab-1").find_all('div')]
        href = soup.find('img', itemprop="image").get('src')
        return name, price, about, href

    @staticmethod
    def func_get_reviews(url_to_product):
        url = 'https://4frag.ru/review/' + url_to_product[17:]
        r = req.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        count_of_reviews = int(soup.find('span', itemprop="reviewCount").text)
        if count_of_reviews:
            dct_with_reviews = {}
            for index_of_review, review in enumerate(soup.find_all('li', class_="mp-rating-item")):
                dct_with_review = {
                    'msg': review.find('div', class_="mp-excerpt").text.replace('\n', ' ').replace('\r', ''),
                    'plus': review.find('div', class_="mp-plus").text.replace('\n', ' ').replace('\r', ''),
                    'minus': review.find('div', class_="mp-minus").text.replace('\n', ' ').replace('\r', ''),
                    'rate': review.find('span', itemprop="ratingValue").text,
                    'name': review.find('div', class_="mp-rating-author-name").text,
                    'date': review.find('div', class_="mp-rating-date").text
                }
                dct_with_reviews[index_of_review] = dct_with_review
            return dct_with_reviews
        else:
            return 'Отзывов нет'

    def func_get_full_info(self, url_to_product):
        name, price, about, href = self.func_get_detail(url_to_product)
        reviews = self.func_get_reviews(url_to_product)
        dct_product = {
            name: [
                {
                    'name': name,
                    'price': price,
                    'about': about,
                    'href': href
                },
                {
                    'reviews': reviews
                }
            ]
        }
        return dct_product


pars = ParsClass('https://4frag.ru/microsoft-xbox-2267/', page=1)

import sys
import xml.dom.minidom
import mysql.connector
from mysql.connector import Error

# this is ebay
product = {"title": "", "description": "", "price": "", "review": "", "image": ""}
desArray = []
product2 = {"title": "", "description": "", "price": "", "review": "", "image": ""}
desArray2 = []
# title, price, review
document = xml.dom.minidom.parse(sys.argv[1])
everything = document.getElementsByTagName("span")
image = document.getElementsByTagName("img")
description = document.getElementsByTagName("div")

for i in range(len(everything)):
    if everything[i].nodeType == 1 and everything[i].hasAttributes():
        if (
            everything[i].getAttribute("class") == "ux-textspans ux-textspans--BOLD"
            and product["title"] == ""
        ):
            product["title"] = everything[i].firstChild.nodeValue

        if (
            everything[i].getAttribute("class") == "ux-textspans"
            and product["price"] == ""
        ):
            if everything[i].firstChild.nodeValue[:2] == "US":
                product["price"] = everything[i].firstChild.nodeValue[4:9]

        if (
            everything[i].getAttribute("class") == "ux-textspans ux-textspans--BOLD"
            and product["review"] == ""
        ):
            if "%" in everything[i].firstChild.nodeValue:
                product["review"] = everything[i].firstChild.nodeValue[:-1]

        # if price[i].firstChild is not None:
        #     print(price[i].firstChild.nodeValue)

    # image
    for i in range(len(image)):
        if image[i].nodeType == 1 and image[i].hasAttributes():
            if (
                image[i].getAttribute("class") == "ux-image-magnify__image--original"
                and product["image"] == ""
            ):
                product["image"] = image[i].getAttribute("src")

    # description
    for i in range(len(description)):
        if description[i].nodeType == 1 and description[i].hasAttributes():
            if description[i].getAttribute("class") == "ux-labels-values__values":
                spanDesc = description[i].getElementsByTagName("span")[0]
                if (
                    spanDesc.firstChild
                    and spanDesc.firstChild.nodeValue not in desArray
                ):
                    text_content = spanDesc.firstChild.nodeValue
                    desArray.append(text_content)

product["description"] = result_string = ". ".join(
    item for item in desArray if item is not None
)


# this is for HotTopic
document2 = xml.dom.minidom.parse(sys.argv[2])
title = document2.getElementsByTagName("h1")
reviewDesc = document2.getElementsByTagName("div")
price = document2.getElementsByTagName("span")
image2 = document2.getElementsByTagName("img")

# title
for i in range(len(title)):
    if title[i].nodeType == 1 and title[i].hasAttributes():
        if title[i].getAttribute("class") == "product-name" and product2["title"] == "":
            product2["title"] = title[i].firstChild.nodeValue
# price
for i in range(len(price)):
    if price[i].nodeType == 1 and price[i].hasAttributes():
        if price[i].getAttribute("class") == "value" and product2["price"] == "":
            product2["price"] = price[i].getAttribute("content")

# review & description
for i in range(len(reviewDesc)):
    if reviewDesc[i].nodeType == 1 and reviewDesc[i].hasAttributes():
        # review
        if (
            reviewDesc[i].getAttribute("class") == "ratings"
            and product2["review"] == ""
        ):
            spanReview = reviewDesc[i].getElementsByTagName("span")[0]
            ratingNum = spanReview.firstChild.nodeValue
            result = ratingNum.split(" ", 1)[0]
            product2["review"] = result

        # description
        if (
            reviewDesc[i].getAttribute("class") == "details"
            and product2["description"] == ""
        ):
            listItems = reviewDesc[i].getElementsByTagName("li")

            for li in listItems:
                desArray2.append(li.firstChild.nodeValue)

product2["description"] = result_string = ". ".join(
    item for item in desArray2 if item is not None
)

# image
for i in range(len(image2)):
    if image2[i].nodeType == 1 and image2[i].hasAttributes():
        if (
            image2[i].getAttribute("class") == "primary-image"
            and product2["image"] == ""
        ):
            product2["image"] = image2[i].getAttribute("src")

# convert website1 review score from percent to x/
product["review"] = round(float(product["review"]) / 100 * 5, 1)

# insert into sql table
config = {
    "host": "localhost",
    "database": "products",
    "user": "user1",
    "password": "password",
}

try:
    # connect
    connection = mysql.connector.connect(**config)

    # create a cursor
    cursor = connection.cursor()

    # insert data
    cursor.execute(
        """
        INSERT INTO products (title, description, price, review, image)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (
            product["title"],
            product["description"],
            product["price"],
            product["review"],
            product["image"],
        ),
    )

    # commit changes
    connection.commit()

    print("Data inserted successfully.")

except Error as e:
    print(f"Error: {e}")

finally:
    try:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
    except NameError:
        pass

# second product
try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (title, description, price, review, image)
        VALUES (%s, %s, %s, %s, %s)
    """,
        (
            product2["title"],
            product2["description"],
            product2["price"],
            product2["review"],
            product2["image"],
        ),
    )

    connection.commit()

    print("Data for product2 inserted successfully.")

except Error as e:
    print(f"Error: {e}")

finally:
    try:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")
    except NameError:
        pass

import csv

from bs4 import BeautifulSoup
import requests

# for debugging
# with open("htmlFIle.txt", "r") as f:
# bs = BeautifulSoup(f, "html.parser")

search_term = "3070"

url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page=1"
page = requests.get(url).text
bs = BeautifulSoup(page, "html.parser")

# get the number of pages
pages_info = bs.find(class_="list-tool-pagination-text").strong
print(bs.find(class_="list-tool-pagination-text").strong)
end = str(pages_info).rfind("<")
start = str(pages_info).rfind(">", 0, len(str(pages_info)) - 1) + 1
number_of_pages = str(pages_info)[start:end]

print("The number of pages of results is: " + number_of_pages)

# Save the total number of entries
length = 0

# Open a .csv data file to store data
header = ["Product", "Link", "Price"]
data_doc = open(f"{search_term}.csv", "w")
writer = csv.writer(data_doc)
writer.writerow(header)

# Iterate through each page and search it for the desired information
for current_page in range(1, int(number_of_pages) + 1):

    # Get the webpage again for each new page
    print("The current page is: ", current_page)
    url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={current_page}"
    page = requests.get(url).text
    bs = BeautifulSoup(page, "html.parser")

    # Get all of the products on the page into a list
    items = bs.find_all(class_="item-cell")
    print("The number of items on the page is: ", len(items), "\n")

    # For each product print its name and price
    for item in items:
        temp_list = []

        if item.find(class_="item-container"):
            temp_list.append(item.find(class_="item-container").find("img")["title"])
            print(item.find(class_="item-container").find("img")["title"])
            temp_list.append(item.find(class_="item-container").find("a")["href"])
            print("The link to this item is: ", item.find(class_="item-container").find("a")["href"])

            if item.find(class_="price-current") and item.find(class_="price-current").find("strong"):
                temp_list.append(item.find(class_="price-current").strong.text.replace(",", ""))
                print("Current Price is: $", item.find(class_="price-current").strong.text, "\n")
                length += 1
                writer.writerow(temp_list)

data_doc.close()

print("Relevant Entries: ", length)

START_URL = "https://www.webstore.com/shop/all"
PHOTOS_URL = "https://www.webstore.com/_sh/"
FILENAME_MAIN = "data.csv"
FILENAME_LINKS = 'just_links.csv'
filename_num = 'data_num.csv'
COLUMN_NAMES = [
    "Tilda UID",
    "Brand",
    "SKU",
    "Mark",
    "Category",
    "Title",
    "Description",
    "Text",
    "Photo",
    "Price",
    "Quantity",
    "Price Old",
    "Editions",
    "Modifications",
    "External ID",
    "Parent UID",
    "Weight",
    "Length",
    "Width",
    "Height"
]

CATEGORY_NAMES = "Peppers, Tomatoes, Eggplants, Cucumbers, Cucumelons, Exotic Mini Melons, Watermelons, Melons, "\
                 "Pattypan Squash, Zucchini, Pumpkin, Bottle Gourds, Rare Squash Family, Legumes, Carrots, "\
                 "Table Beets, Corn, Okra, 'Russian Size' Seed Series, Miscellaneous, Onion, Parsley, Dill, "\
                 "Leek, Garlic."

DCT_TASKS = {'text': 'Please remove unnecessary symbols from the product description while keeping the content intact.',
             'pre_description': 'Please write the {part_index} part of the brief product description using the {'
                                'part_index} part of the'
                                'full product description for {title}.',
             'description': 'Please write a concise and captivating 20-word description for the "{title}" product, '
                            'using the full product description, for my'
                            'favorite seed-selling store.',
             'category': f'Please select the correct category from the list: {CATEGORY_NAMES}'}
FILENAME_ERRORS = 'filename_errors.txt'

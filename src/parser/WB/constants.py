# Duration of sleep by seconds, use in lib "time".
TIME_FOR_SLEEP: int = 2

# Index of every element in list after that need make sleep
COUNTER_OF_INDEX_FOR_SLEEP_IN_LOOP: int = 10

# Count value after which need make sleep in AsyncRequesterWB._find_api_url_from_network
ASYNC_REQUESTER_SLEEP_INDEX_VALUE: int = 5

CHUNK_SIZE: int = 25

# Duration of timeout by millisecond after you go to page in AsyncRequesterWB._find_api_url_from_network
ASYNC_REQUESTER_TIMEOUT: int = 1000

SYMBOL_TO_REPLACE_FOR_PAGE_NUMBER_IN_URL: str = '*'

SPLIT_VALUE: str = ', '

# JSON object, that contain data about personal info of product
REQUIRED_JSON_FOR_PRODUCT_PERSONAL_INFO: str = "card.json"

# Part of URL that need to change for getting URL for price history
REQUIRED_JSON_FILE_FOR_CHANGE: str = "ru/card.json"

# JSON object, that contain data about price history of product
REQUIRED_JSON_FOR_PRODUCT_PRICE_HISTORY: str = "price-history.json"

DATA_KEY: str = 'data'
PRODUCTS_KEY: str = 'products'
ID_KEY: str = 'id'
ROOT_KEY: str = 'root'
NAME_KEY: str = 'name'

PRODUCT_ID: str = 'product_id'
ROOT_ID: str = 'root_id'
PRODUCT_NAME: str = 'product_name'
DATE: str = 'date'

PRICE_HISTORY_DATE_KEY: str = "dt"
PRICE_HISTORY_PRICE_KEY: str = "price"
PRICE_HISTORY_CURRENT_CURRENCY_KEY: str = "RUB"

FIRST_PAGE: int = 1
LAST_PAGE: int = 3

PRODUCT_ROOT_ID: str = "imt_id"
PRODUCT_NAME_KEY: str = "imt_name"
PRODUCT_CATEGORY: str = "subj_root_name"
PRODUCT_MAIN_CATEGORY: str = "subj_name"
PRODUCT_DESCRIPTION: str = "description"

PRODUCT_SELLING: str = "selling"
PRODUCT_BRAND_NAME: str = "brand_name"
PRODUCT_DETAIL_LIST_KEY: str = "options"

PRODUCT_DETAIL_KEY_VALUES: str = "values"
PRODUCT_DETAIL_KEY_VALUE: str = "value"
PRODUCT_SIZE_DETAILS: str = "details"

PRODUCT_COMPOSITIONS: str = "compositions"
PRODUCT_DETAIL_COMPOSITIONS: list[str] = ["Состав", "Состав ювелирного изделия"]

PRODUCT_SIZES_TABLE: str = "sizes_table"
PRODUCT_MIN_SIZE = "min_size"
PRODUCT_MAX_SIZE = "max_size"

PRODUCT_DETAIL_COLOR: str = "Цвет"
PRODUCT_COLOR: str = "color"

PRODUCT_DETAIL_MADE_IN: str = "Страна производства"
PRODUCT_MADE_IN: str = "made_in"

PRODUCT_PERSONAL_INFO_KEYS: list[str] = [PRODUCT_DESCRIPTION,
                                         PRODUCT_CATEGORY,
                                         PRODUCT_MAIN_CATEGORY,
                                         PRODUCT_ROOT_ID,
                                         PRODUCT_NAME_KEY
                                         ]

FEEDBACKS_KEY: str = "feedbacks"
FEEDBACK_DATE_KEY: str = "createdDate"
FEEDBACK_PRODUCT_ID_KEY: str = "nmId"
FEEDBACK_COMMENT_KEY: str = "text"
FEEDBACK_GRADE_KEY: str = "productValuation"

FEEDBACK_LAST_INDEX_OF_DATE_STR: int = 10

FEEDBACK_COMMENT_TITLE: str = 'comment'
FEEDBACK_GRADE_TITLE: str = 'grade'

PRODUCT_CARD_JSON_TITLE: str = "card_json_url"
PRODUCT_PRICE_HISTORY_JSON_TITLE: str = "price_history_json_url"

PRODUCT_LIST_URL: str = f"https://recom.wb.ru/personal/ru/common/v5/search?ab_testing=false&curr=rub&dest=-1257786&page={SYMBOL_TO_REPLACE_FOR_PAGE_NUMBER_IN_URL}&query=0&resultset=catalog"

PRODUCT_URL: str = f"https://www.wildberries.ru/catalog/{PRODUCT_ID}/detail.aspx"

FEEDBACK_URLS: list[str] = [f"https://feedbacks1.wb.ru/feedbacks/v2/{ROOT_ID}",
                            f"https://feedbacks2.wb.ru/feedbacks/v2/{ROOT_ID}"]

# Count of threads in file 'primary_data_script.py'
THREADS_COUNT: int = 10

# Path to files that contain information about products
PATH_TO_URLS: str = 'csv/urls.csv'
PATH_TO_PRODUCTS: str = 'csv/products.csv'
PATH_TO_PRICE_HISTORY: str = 'csv/price-history.csv'
PATH_TO_FEEDBACK: str = 'csv/feedbacks.csv'

INVALID_RESPONSE_MESSAGE: str = "Validator can't find this key in response: "

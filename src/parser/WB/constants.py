# Count value after which need make sleep in ParserWB.parse_product_list
PRODUCT_LIST_PAGE_NUMBER_FOR_SLEEP = 5

# Duration of sleep by seconds, use in lib "time".
TIME_FOR_SLEEP = 2

# Index of every element in list after that need make sleep
COUNTER_OF_INDEX_FOR_SLEEP_IN_LOOP = 10

# Count value after which need make sleep in AsyncRequesterWB._find_api_url_from_network
ASYNC_REQUESTER_SLEEP_INDEX_VALUE = 5

CHUNK_SIZE = 25

# Duration of timeout by millisecond after you go to page in AsyncRequesterWB._find_api_url_from_network
ASYNC_REQUESTER_TIMEOUT = 1000

SYMBOL_TO_REPLACE_FOR_PAGE_NUMBER_IN_URL = '*'

SPLIT_VALUE = ', '

# JSON object, that contain data about personal info of product
REQUIRED_JSON_FOR_PRODUCT_PERSONAL_INFO = "card.json"

# Part of URL that need to change for getting URL for price history
REQUIRED_JSON_FILE_FOR_CHANGE = "ru/card.json"

# JSON object, that contain data about price history of product
REQUIRED_JSON_FOR_PRODUCT_PRICE_HISTORY = "price-history.json"

DATA_KEY = 'data'
PRODUCTS_KEY = 'products'
ID_KEY = 'id'
ROOT_KEY = 'root'
NAME_KEY = 'name'

PRODUCT_ID = 'product_id'
ROOT_ID = 'root_id'
PRODUCT_NAME = 'product_name'
DATE = 'date'

PRICE_HISTORY_DATE_KEY = "dt"
PRICE_HISTORY_PRICE_KEY = "price"
PRICE_HISTORY_CURRENT_CURRENCY_KEY = "RUB"

FIRST_PAGE = 1
LAST_PAGE = 3

PRODUCT_NAME_KEY = "imt_name"
PRODUCT_CATEGORY = "subj_root_name"
PRODUCT_MAIN_CATEGORY = "subj_name"
PRODUCT_DESCRIPTION = "description"

PRODUCT_SELLING = "selling"
PRODUCT_BRAND_NAME = "brand_name"
PRODUCT_BRAND_ID_KEY = "brand_Id"
PRODUCT_DETAIL_LIST_KEY = "options"

PRODUCT_DETAIL_KEY_VALUES = "values"
PRODUCT_DETAIL_KEY_VALUE = "value"
PRODUCT_SIZE_DETAILS = "details"

PRODUCT_COMPOSITIONS = "compositions"
PRODUCT_DETAIL_COMPOSITIONS = ["Состав", "Состав ювелирного изделия"]

PRODUCT_SIZES_TABLE = "sizes_table"
PRODUCT_SIZES_TABLE_TECH_SIZE_KEY = "tech_size"

PRODUCT_MIN_SIZE = "min_size"

PRODUCT_MAX_SIZE = "max_size"

PRODUCT_DETAIL_COLOR = "Цвет"
PRODUCT_COLOR = "color"

PRODUCT_DETAIL_MADE_IN = "Страна производства"
PRODUCT_MADE_IN = "made_in"

PRODUCT_PERSONAL_INFO_KEYS = [PRODUCT_DESCRIPTION,
                              PRODUCT_CATEGORY,
                              PRODUCT_MAIN_CATEGORY
                              ]

FEEDBACKS_KEY = "feedbacks"
FEEDBACK_DATE_KEY = "createdDate"
FEEDBACK_PRODUCT_ID_KEY = "nmId"
FEEDBACK_COMMENT_KEY = "text"
FEEDBACK_GRADE_KEY = "productValuation"

FEEDBACK_LAST_INDEX_OF_DATE_STR = 10

FEEDBACK_COMMENT_TITLE = 'comment'
FEEDBACK_GRADE_TITLE = 'grade'

PRODUCT_CARD_JSON_TITLE = "card_json_url"
PRODUCT_PRICE_HISTORY_JSON_TITLE = "price_history_json_url"

PRODUCT_LIST_URL = f"https://recom.wb.ru/personal/ru/common/v5/search?ab_testing=false&curr=rub&dest=-1257786&page={SYMBOL_TO_REPLACE_FOR_PAGE_NUMBER_IN_URL}&query=0&resultset=catalog"

PRODUCT_URL = f"https://www.wildberries.ru/catalog/{PRODUCT_ID}/detail.aspx"

FEEDBACK_URLS = [f"https://feedbacks1.wb.ru/feedbacks/v2/{ROOT_ID}",
                 f"https://feedbacks2.wb.ru/feedbacks/v2/{ROOT_ID}"]

THREADS_COUNT = 10

# Path to files that contain information about products
PATH_TO_URLS = 'csv/urls.csv'
PATH_TO_PRODUCTS = 'csv/products.csv'
PATH_TO_PRICE_HISTORY = 'csv/price-history.csv'
PATH_TO_FEEDBACK = 'csv/feedbacks.csv'

INVALID_RESPONSE_MESSAGE = "Validator can't find this key in response: "
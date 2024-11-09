from src.parser.WB import constants

TMP_TABLE = "tmp_table"

ROOT_ID = "root_id"
PRODUCT_ID = "product_id"
DATE = "date"
PRODUCT_NAME = "product_name"
PRODUCT_DESCRIPTION = "description"
PRODUCT_BRAND_NAME = "brand_name"
PRODUCT_MAIN_CATEGORY = "subj_name"
PRODUCT_CATEGORY = "subj_root_name"
PRODUCT_SIZES_TABLE = "sizes_table"
PRODUCT_MIN_SIZE = "min_size"
PRODUCT_MAX_SIZE = "max_size"
PRODUCT_COLOR = "color"
PRODUCT_MADE_IN = "made_in"
PRODUCT_COMPOSITIONS = "compositions"
COMMENT = "comment"
PRICE = "price"
PRODUCT_CARD_JSON = "card_json_url"
PRODUCT_PRICE_HISTORY_JSON = "price_history_json_url"


feedbacks_table_type_dict = {
    ROOT_ID: "INT4",
    PRODUCT_ID: "INT4",
    DATE: "DATE",
    COMMENT: "VARCHAR(5000)"
}

price_history_type_dict = {
    PRODUCT_ID: "INT4",
    DATE: "DATE",
    PRICE: "FLOAT4"
}

products_table_type_dict = {
    ROOT_ID: "INT4",
    PRODUCT_ID: "INT4",
    DATE: "DATE",
    PRODUCT_NAME: "VARCHAR(512)",
    PRODUCT_DESCRIPTION: "VARCHAR(4096)",
    PRODUCT_BRAND_NAME: "VARCHAR(50)",
    PRODUCT_MAIN_CATEGORY: "VARCHAR(50)",
    PRODUCT_CATEGORY: "VARCHAR(50)",
    PRODUCT_SIZES_TABLE: "VARCHAR(128)",
    PRODUCT_MIN_SIZE: "VARCHAR(50)",
    PRODUCT_MAX_SIZE: "VARCHAR(50)",
    PRODUCT_COLOR: "VARCHAR(128)",
    PRODUCT_MADE_IN: "VARCHAR(50)",
    PRODUCT_COMPOSITIONS: "VARCHAR(2048)"
}

urls_table_type_dict = {
    PRODUCT_ID: "INT4",
    PRODUCT_CARD_JSON: "VARCHAR(256)",
    PRODUCT_PRICE_HISTORY_JSON: "VARCHAR(256)"
}
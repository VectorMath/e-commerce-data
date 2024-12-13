"""Indexes of tables
"""
INDEX_PRODUCTS: str = "idx_products"
INDEX_URLS: str = "idx_urls"
INDEX_PRICE_HISTORY: str = "idx_ph"
INDEX_GRADE_HISTORY: str = "idx_gh"
INDEX_FEEDBACKS: str = "idx_feedbacks"

"""Columns of tables
"""
ROOT_ID: str = "root_id"
PRODUCT_ID: str = "product_id"
DATE: str = "date"
PRODUCT_NAME: str = "product_name"
PRODUCT_DESCRIPTION: str = "description"
PRODUCT_BRAND_NAME: str = "brand_name"
PRODUCT_MAIN_CATEGORY: str = "subj_name"
PRODUCT_CATEGORY: str = "subj_root_name"
PRODUCT_SIZES_TABLE: str = "sizes_table"
PRODUCT_MIN_SIZE: str = "min_size"
PRODUCT_MAX_SIZE: str = "max_size"
PRODUCT_COLOR: str = "color"
PRODUCT_MADE_IN: str = "made_in"
PRODUCT_COMPOSITIONS: str = "compositions"
COMMENT: str = "comment"
PRICE: str = "price"
PRODUCT_CARD_JSON: str = "card_json_url"
PRODUCT_PRICE_HISTORY_JSON: str = "price_history_json_url"
GRADE: str = "grade"
MEAN_GRADE: str = "mean_grade"
MEAN_GRADE_FILTERED: str = "mean_grade_filtered"
MEDIAN_GRADE: str = "median_grade"
MEDIAN_GRADE_FILTERED = "median_grade_filtered"
MODE_GRADE: str = "mode_grade"
MODE_GRADE_FILTERED: str = "mode_grade_filtered"

"""Data type of columns in database
"""
feedbacks_table_type_dict = {
    ROOT_ID: "INT4",
    PRODUCT_ID: "INT4",
    DATE: "DATE",
    COMMENT: "VARCHAR(5000)",
    GRADE: "INT4"
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

grade_table_type_dict = {
    PRODUCT_ID: "INT4",
    DATE: "DATE",
    MEAN_GRADE: "FLOAT4",
    MEAN_GRADE_FILTERED: "FLOAT4",
    MEDIAN_GRADE: "FLOAT4",
    MEDIAN_GRADE_FILTERED: "FLOAT4",
    MODE_GRADE: "FLOAT4",
    MODE_GRADE_FILTERED: "FLOAT4"
}

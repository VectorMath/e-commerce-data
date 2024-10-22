"""This script gives you few csv-files of primary data from web-store Wildberries.
in the end, script give you second csv-files, for DB:

1) urls.csv - table that contain urls of API for products information.

2) products - table that contain personal information about products

3) price-history.csv - table that contain story of price for products

4) feedback - table that contain feedbacks for products.

P.S For more fast result you can use multithreading in AsyncRequesterWB too,
but my laptop gets hot with only one thread, so I don't want to risk :/
"""
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)  # Show warning on numpy.array_split

import time

import numpy as np
import pandas as pd

from src.parser.IParser import IParser
from src.parser.WB import constants
from src.parser.WB.AsyncRequesterWB import AsyncRequesterWB
from src.parser.WB.ParserWB import ParserWB

from concurrent.futures import ThreadPoolExecutor, as_completed

parser: IParser = ParserWB()

df_urls = pd.DataFrame()
products_df = pd.DataFrame()
price_history_df = pd.DataFrame()
feedbacks_df = pd.DataFrame()

global_start_time = time.time()
'''IDs table part
'''
start_time = time.time()
print(f"Starting parsing product list of {constants.LAST_PAGE - constants.FIRST_PAGE} pages")

df_product_list = parser.parse_product_list()  # Work very fast so we don't need few threads for that.

end_time = time.time()
print(f"Finished - {(end_time - start_time):.2f} seconds\n")

product_chunks = np.array_split(df_product_list, len(df_product_list) // constants.CHUNK_SIZE)

for i, chunk in enumerate(product_chunks):
    print(f"-----Chunk №{i + 1}-----")

    '''URLs table part
    '''
    start_time = time.time()
    print(f"Starting create table of json URLs")

    network_requester = AsyncRequesterWB(product_ids=list(chunk[constants.PRODUCT_ID]),
                                         root_ids=list(chunk[constants.ROOT_ID]))

    df_urls = pd.concat([df_urls, network_requester.create_table_with_json_urls()])

    end_time = time.time()
    print(f"Finished - {(end_time - start_time):.2f} seconds\n")

    '''Products table part
    '''
    start_time = time.time()
    print(f"[{constants.THREADS_COUNT} THREADS] Starting collect personal info about products")

    with ThreadPoolExecutor(max_workers=constants.THREADS_COUNT) as executor:
        futures = {executor.submit(parser.parse_product_personal_info, url): url for url in
                   df_urls[constants.PRODUCT_CARD_JSON_TITLE]}

        for future in as_completed(futures):
            product = pd.merge(future.result(), chunk, on=constants.PRODUCT_ID)
            products_df = pd.concat([products_df, product])

        if (len(products_df) % constants.COUNTER_OF_INDEX_FOR_SLEEP_IN_LOOP) == 0 and len(products_df) != 0:
            time.sleep(constants.TIME_FOR_SLEEP)

    end_time = time.time()
    print(f"Finished - {(end_time - start_time):.2f} seconds\n")

    '''Price history table part
    '''
    start_time = time.time()
    print(f"[{constants.THREADS_COUNT} THREADS] Starting collect price history")

    with ThreadPoolExecutor(max_workers=constants.THREADS_COUNT) as executor:
        futures = {executor.submit(parser.parse_product_price_history, url): url for url in
                   df_urls[constants.PRODUCT_PRICE_HISTORY_JSON_TITLE]}

        for future in as_completed(futures):
            price_history_df = pd.concat([price_history_df, future.result()])

        if (len(price_history_df) % constants.COUNTER_OF_INDEX_FOR_SLEEP_IN_LOOP) == 0 and len(price_history_df) != 0:
            time.sleep(constants.TIME_FOR_SLEEP)

    end_time = time.time()
    print(f"Finished - {(end_time - start_time):.2f} seconds\n")

    '''Feedbacks table part
    '''
    start_time = time.time()
    print(f"[{constants.THREADS_COUNT} THREADS] Starting collect feedbacks")

    with ThreadPoolExecutor(max_workers=constants.THREADS_COUNT) as executor:
        '''We don't use here pause, because for every response we take big JSON, and extracting take long time
        '''
        futures = {executor.submit(parser.parse_product_feedback, product_id, root_id): (product_id, root_id) for
                   _, (product_id, root_id) in
                   enumerate(zip(df_product_list[constants.PRODUCT_ID], df_product_list[constants.ROOT_ID]))}

        for future in as_completed(futures):
            feedbacks_df = pd.concat([feedbacks_df, future.result()])

    end_time = time.time()
    print(f"Finished - {(end_time - start_time):.2f} seconds\n")

    time.sleep(constants.TIME_FOR_SLEEP)

'''Export part
'''
# Set the sequence in the table products
products_df = products_df[[constants.ROOT_ID,
                           constants.PRODUCT_ID,
                           constants.DATE,
                           constants.PRODUCT_NAME,
                           constants.PRODUCT_DESCRIPTION,
                           constants.PRODUCT_MAIN_CATEGORY,
                           constants.PRODUCT_CATEGORY,
                           constants.PRODUCT_DESCRIPTION,
                           constants.PRODUCT_SIZES_TABLE,
                           constants.PRODUCT_MIN_SIZE,
                           constants.PRODUCT_MAX_SIZE,
                           constants.PRODUCT_COLOR,
                           constants.PRODUCT_MADE_IN,
                           constants.PRODUCT_COMPOSITIONS]]

df_urls.to_csv(constants.PATH_TO_URLS, index=False)
products_df.to_csv(constants.PATH_TO_PRODUCTS, index=False)
price_history_df.to_csv(constants.PATH_TO_PRICE_HISTORY, index=False)
feedbacks_df.to_csv(constants.PATH_TO_FEEDBACK, index=False)

global_end_time = time.time()
print(f"Script finished for - {((global_end_time - global_start_time) / 60):.2f} minutes")

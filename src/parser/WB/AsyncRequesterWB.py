import asyncio
import time

import pandas as pd
from playwright.async_api import async_playwright, Browser, Page

from src import config
from src.parser.WB import constants


class AsyncRequesterWB:
    """This class if using to get URLs from Network tab in developer window of browser.
    Usually, this class uses the result of method parse_product_list of class ParserWB.
    """

    def __init__(self, product_id_list: list[str]):
        """Class constructor
        :param product_id_list: list of product_id
        """
        self._product_id_list: list[str] = product_id_list

    async def _find_api_url_from_network(self) -> list[str]:
        """Async private method that extract API URLs from network requests.
        :return: URLs of personal info products.
        """
        async with async_playwright() as p:
            browser: Browser = await p.chromium.launch()
            page: Page = await browser.new_page()
            urls: list[str] = []

            async def intercept_response(response):
                if constants.REQUIRED_JSON_FOR_PRODUCT_PERSONAL_INFO in response.url:
                    urls.append(response.url)

            page.on("response", intercept_response)

            for index, product_id in enumerate(self._product_id_list):
                if index % constants.ASYNC_REQUESTER_SLEEP_INDEX_VALUE == 0 and index != 0:
                    time.sleep(constants.TIME_FOR_SLEEP)

                await page.goto(constants.PRODUCT_URL.replace(constants.PRODUCT_ID, product_id), wait_until='load')
                await page.wait_for_timeout(constants.ASYNC_REQUESTER_TIMEOUT)

            await page.close()
            await browser.close()
            return urls

    def create_table_with_json_urls(self) -> pd.DataFrame:
        """Method that using private method _find_api_url_from_network
        and create table with product_id and URLs on personal info and price history
        :return: DataFrame with json urls of product and price history.
        """
        product_card_urls: list[str] = asyncio.run(self._find_api_url_from_network())
        product_ids: list[int] = []
        for url in product_card_urls:
            product_ids.append(int(url.split('/')[-4]))
        price_history_urls: list[str] = []

        '''Optimization part, no need make request for product twice.
        '''
        for url in product_card_urls:
            changed_url = str(url).replace(constants.REQUIRED_JSON_FILE_FOR_CHANGE,
                                           constants.REQUIRED_JSON_FOR_PRODUCT_PRICE_HISTORY)
            price_history_urls.append(changed_url)

        table: dict = {
            constants.PRODUCT_ID: product_ids,
            constants.PRODUCT_CARD_JSON_TITLE: product_card_urls,
            constants.PRODUCT_PRICE_HISTORY_JSON_TITLE: price_history_urls
        }

        ''' Sometimes method return duplicates of first row
        Here we checking for that and remove.
        '''
        result: pd.DataFrame = pd.DataFrame(table).drop_duplicates().reset_index(drop=True)
        return result

    def get_product_id_list(self) -> list[str]:
        """Get method for field _product_id_list
        """
        return self._product_id_list

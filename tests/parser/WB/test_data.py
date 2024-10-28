mock_method = "requests.get"

from src.parser.WB import constants

product_url = "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/info/ru/card.json"
price_history_url = "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/info/price-history.json"
price_history_url_with_index_error = "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/v1/info/price-history.json"

product_id = "251750385"

non_existed_key = 'abrakadabra'

actual_sizes = "42, 44, 46, 48, 50, 52, 54, 56, 58"

actual_made_in_value = "Китай"
actual_color = "черный"
actual_compositions = "флис; полиэстер; эластан"

product_response = {
    "imt_id": 227510481,
    "nm_id": 251750385,
    "imt_name": "Термобелье комплект зимний спортивный",
    "slug": "termobele-komplekt-zimnij-sportivnyj",
    "subj_name": "Термокомплекты",
    "subj_root_name": "Белье",
    "vendor_code": "NordicsR",
    "description": "Комплект мужского термобелья от бренда Nordics — это идеальное решение для тех, кто ищет качественную одежду, способную обеспечить комфорт в любое время года. Данный набор включает в себя кофту и кальсоны, которые обеспечивают отличную защиту от холода и поддерживают необходимую терморегуляцию. Качественный флис отличает наш товар от конкурентов уютом и теплом, а также прекрасен для зимних условий. Наша одежда идеально подходит не только для зимы, но и для другого времени года, так как обеспечивает оптимальную вентиляцию и отведение влаги, что делает ее удобной для использования в любую погоду. Это делает форму универсальной вещью для всех сезонов. Наше изделие предназначено также для различных видов спорта. Оно идеально подходит для бега и других активностей, в том числе и для рыбалки. Благодаря компрессионным свойствам штанов и верха, изделие обеспечивает поддержку мышц и улучшает кровообращение, что способствует повышению производительности при занятии хоккеем или футболом. Спортивки станут незаменимым спутником для спортсменов любого уровня. Теплые подштанники и кофта с начесом обеспечивают полный комфорт на протяжении всего дня, даже если вы решили выйти на охоту или в долгий поход. Отличительная особенность термокомплекта – это его долговечность. Вещи легко стираются и быстро сохнут, не теряя своих свойств и внешнего вида после многих стирок. Флисовое белье сохраняет свои теплоизоляционные характеристики и не линяет, что делает его практичным выбором для повседневного использования. Термобелье будет уместным для любого мужского тела. Наш товар представляет собой идеальное сочетание комфорта и стиля. Независимо от того, где вы находитесь и чем занимаетесь, эта термоодежда станет вашим незаменимым спутником. \n",
    "options": [
        {
            "name": "Состав",
            "value": "флис; полиэстер; эластан",
            "charc_type": 1
        },
        {
            "name": "Цвет",
            "value": "черный",
            "is_variable": True,
            "charc_type": 1,
            "variable_values": [
                "черный"
            ]
        },
        {
            "name": "Параметры модели на фото (ОГ-ОТ-ОБ)",
            "value": "112-89-105",
            "charc_type": 1
        },
        {
            "name": "Рост модели на фото",
            "value": "185 см",
            "charc_type": 4
        },
        {
            "name": "Высота посадки брючин",
            "value": "29 см",
            "charc_type": 4
        },
        {
            "name": "Особенности белья",
            "value": "теплосберегающие дышащая ткань плоские швы бесшовное",
            "charc_type": 1
        },
        {
            "name": "Страна производства",
            "value": "Китай",
            "charc_type": 1
        },
        {
            "name": "Уход за вещами",
            "value": "стирка с изнаночной стороны; стирка при t не более 30°C; допускается отпаривание",
            "charc_type": 1
        },
        {
            "name": "Комплектация",
            "value": "Кальсоны - 1шт; Лонгслив - 1шт",
            "charc_type": 1
        }
    ],
    "compositions": [
        {
            "name": "флис"
        },
        {
            "name": "полиэстер"
        },
        {
            "name": "эластан"
        }
    ],
    "sizes_table": {
        "details_props": [
            "RU",
            "Обхват талии, в см",
            "Обхват бедер, в см"
        ],
        "values": [
            {
                "tech_size": "4XL",
                "chrt_id": 402795933,
                "details": [
                    "56",
                    "98-102",
                    "114-115.9"
                ]
            },
            {
                "tech_size": "L",
                "chrt_id": 402795938,
                "details": [
                    "48",
                    "82-86",
                    "100-104"
                ]
            },
            {
                "tech_size": "3XL",
                "chrt_id": 402795935,
                "details": [
                    "54",
                    "94-98",
                    "110-114"
                ]
            },
            {
                "tech_size": "XL",
                "chrt_id": 402795937,
                "details": [
                    "50",
                    "86-90",
                    "104-106"
                ]
            },
            {
                "tech_size": "2XL",
                "chrt_id": 402795936,
                "details": [
                    "52",
                    "90-94",
                    "106-110"
                ]
            },
            {
                "tech_size": "5XL",
                "chrt_id": 402795932,
                "details": [
                    "58",
                    "102-106",
                    "116-119.9"
                ]
            },
            {
                "tech_size": "M",
                "chrt_id": 393402259,
                "details": [
                    "46",
                    "78-82",
                    "96-100"
                ]
            },
            {
                "tech_size": "S",
                "chrt_id": 402795939,
                "details": [
                    "44",
                    "74-78",
                    "92-96"
                ]
            },
            {
                "tech_size": "XS",
                "chrt_id": 402795940,
                "details": [
                    "42",
                    "70-74",
                    "88-92"
                ]
            }
        ]
    },
    "certificate": {
        "verified": True
    },
    "nm_colors_names": "черный",
    "colors": [251750440, 237223633, 270868467, 251750385],
    "contents": "Кальсоны - 1шт; Лонгслив - 1шт",
    "full_colors": [
        {
            "nm_id": 251750440
        },
        {
            "nm_id": 237223633
        },
        {
            "nm_id": 270868467
        },
        {
            "nm_id": 251750385
        }
    ],
    "selling": {
        "no_return_map": 134217727,
        "brand_name": "Nordics",
        "brand_hash": "39EFB601AD25EE43",
        "supplier_id": 4084656
    },
    "media": {
        "has_video": True,
        "photo_count": 14
    },
    "data": {
        "subject_id": 166,
        "subject_root_id": 4,
        "chrt_ids": [402795933, 402795938, 402795935, 402795937, 402795936, 402795932, 393402259, 402795939, 402795940]
    },
    "grouped_options": [
        {
            "group_name": "Основная информация",
            "options": [
                {
                    "name": "Состав",
                    "value": "флис; полиэстер; эластан",
                    "charc_type": 1
                },
                {
                    "name": "Цвет",
                    "value": "черный",
                    "is_variable": True,
                    "charc_type": 1,
                    "variable_values": [
                        "черный"
                    ]
                }
            ]
        },
        {
            "group_name": "Дополнительная информация",
            "options": [
                {
                    "name": "Параметры модели на фото (ОГ-ОТ-ОБ)",
                    "value": "112-89-105",
                    "charc_type": 1
                },
                {
                    "name": "Рост модели на фото",
                    "value": "185 см",
                    "charc_type": 4
                },
                {
                    "name": "Высота посадки брючин",
                    "value": "29 см",
                    "charc_type": 4
                },
                {
                    "name": "Особенности белья",
                    "value": "теплосберегающие дышащая ткань плоские швы бесшовное",
                    "charc_type": 1
                },
                {
                    "name": "Страна производства",
                    "value": "Китай",
                    "charc_type": 1
                },
                {
                    "name": "Уход за вещами",
                    "value": "стирка с изнаночной стороны; стирка при t не более 30°C; допускается отпаривание",
                    "charc_type": 1
                },
                {
                    "name": "Комплектация",
                    "value": "Кальсоны - 1шт; Лонгслив - 1шт",
                    "charc_type": 1
                }
            ]
        }
    ]
}

price_history_response = [
    {
        "dt": 1726358400,
        "price": {
            "RUB": 321075
        }
    },
    {
        "dt": 1726963200,
        "price": {
            "RUB": 246360
        }
    }
]

feedback_response = {
    "feedbackCount": 1360,
    "feedbackCountWithPhoto": 35,
    "feedbackCountWithText": 799,
    "feedbackCountWithVideo": 0,
    "feedbacks": [
        {
            "id": "o1iMcvqqfloZwSOiS6QG",
            "globalUserId": "55848183",
            "wbUserId": 55848183,
            "wbUserDetails": {
                "hasPhoto": False,
                "name": "Анна",
                "country": "ru"
            },
            "nmId": 251750385,
            "text": "Отличное очень теплое белье, размер соответствует",
            "pros": "",
            "cons": "",
            "matchingSize": "",
            "matchingPhoto": "",
            "matchingDescription": "",
            "productValuation": 5,
            "color": "черный",
            "size": "L",
            "createdDate": "2024-10-27T19:20:50Z",
            "updatedDate": "2024-10-27T19:25:35Z",
            "answer": None,
            "metadata": None,
            "feedbackHelpfulness": None,
            "video": None,
            "votes": {
                "pluses": 0,
                "minuses": 0
            },
            "rank": 799,
            "statusId": 16,
            "bables": []
        },
        {
            "id": "QlLmr8IEokgqPvHcfXFn",
            "globalUserId": "63438768",
            "wbUserId": 63438768,
            "wbUserDetails": {
                "country": "ru",
                "hasPhoto": False,
                "name": "Галина"
            },
            "nmId": 20002000,
            "text": "",
            "pros": "Термобелье отличное 👍",
            "cons": "",
            "matchingSize": "",
            "matchingPhoto": "",
            "matchingDescription": "",
            "productValuation": 5,
            "color": "черный",
            "size": "2XL",
            "createdDate": "2024-10-27T18:54:13Z",
            "updatedDate": "2024-10-27T18:56:03Z",
            "answer": None,
            "metadata": None,
            "feedbackHelpfulness": None,
            "video": None,
            "votes": {
                "pluses": 0,
                "minuses": 0
            },
            "rank": 798,
            "statusId": 14,
            "bables": []
        }]
}

feedback_response_with_invalid_key = {
    "feedbackCount": 1360,
    "feedbackCountWithPhoto": 35,
    "feedbackCountWithText": 799,
    "feedbackCountWithVideo": 0,
    non_existed_key: [
        {
            "id": "o1iMcvqqfloZwSOiS6QG",
            "globalUserId": "55848183",
            "wbUserId": 55848183,
            "wbUserDetails": {
                "hasPhoto": False,
                "name": "Анна",
                "country": "ru"
            },
            "nmId": 251750385,
            "text": "Отличное очень теплое белье, размер соответствует",
            "pros": "",
            "cons": "",
            "matchingSize": "",
            "matchingPhoto": "",
            "matchingDescription": "",
            "productValuation": 5,
            "color": "черный",
            "size": "L",
            "createdDate": "2024-10-27T19:20:50Z",
            "updatedDate": "2024-10-27T19:25:35Z",
            "answer": None,
            "metadata": None,
            "feedbackHelpfulness": None,
            "video": None,
            "votes": {
                "pluses": 0,
                "minuses": 0
            },
            "rank": 799,
            "statusId": 16,
            "bables": []
        },
        {
            "id": "QlLmr8IEokgqPvHcfXFn",
            "globalUserId": "63438768",
            "wbUserId": 63438768,
            "wbUserDetails": {
                "country": "ru",
                "hasPhoto": False,
                "name": "Галина"
            },
            "nmId": 20002000,
            "text": "",
            "pros": "Термобелье отличное 👍",
            "cons": "",
            "matchingSize": "",
            "matchingPhoto": "",
            "matchingDescription": "",
            "productValuation": 5,
            "color": "черный",
            "size": "2XL",
            "createdDate": "2024-10-27T18:54:13Z",
            "updatedDate": "2024-10-27T18:56:03Z",
            "answer": None,
            "metadata": None,
            "feedbackHelpfulness": None,
            "video": None,
            "votes": {
                "pluses": 0,
                "minuses": 0
            },
            "rank": 798,
            "statusId": 14,
            "bables": []
        }]
}

feedback_ready_dict = {
    constants.ROOT_ID: [str(227510481)],
    constants.PRODUCT_ID: [str(251750385)],
    constants.DATE: ["2024-10-27"],
    constants.FEEDBACK_COMMENT_TITLE: ["Отличное очень теплое белье, размер соответствует"],
    constants.FEEDBACK_GRADE_TITLE: [5]

}

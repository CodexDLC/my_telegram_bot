



RECO_CATEGORIES: dict[str,dict[str, str]] = {
    "movies": {
        "action": "боевик",
        "adventure": "приключения",
        "comedy": "комедия",
        "drama": "драма",
        "thriller": "триллер",
        "horror": "ужасы",
        "sci-fi": "научная фантастика",
        "fantasy": "фэнтези",
        "mystery": "детектив",
        "crime": "криминал",
        "romance": "мелодрама",
        "family": "семейный",
        "war": "военный",
        "historical": "исторический",
        "biopic": "биографический",
        "western": "вестерн",
        "musical": "мюзикл",
        "sport": "спорт",
        "superhero": "супергеройский",
        "noir": "нуар",
        "disaster": "катастрофа"
    },
    "series": {
        "action": "боевик",
        "adventure": "приключения",
        "comedy": "комедия",
        "drama": "драма",
        "thriller": "триллер",
        "horror": "ужасы",
        "sci-fi": "научная фантастика",
        "fantasy": "фэнтези",
        "mystery": "детектив",
        "crime": "криминал",
        "romance": "мелодрама",
        "family": "семейный",
        "historical": "исторический",
        "biographical": "биографический",
        "sitcom": "ситком",
        "procedural": "процедурал",
        "superhero": "супергеройский",
        "docuseries": "докусериал"
    },
    "anime": {
        "action": "боевик",
        "adventure": "приключения",
        "comedy": "комедия",
        "drama": "драма",
        "thriller": "триллер",
        "horror": "ужасы",
        "sci-fi": "научная фантастика",
        "fantasy": "фэнтези",
        "mystery": "детектив",
        "crime": "криминал",
        "romance": "романтика",
        "slice of life": "повседневность",
        "school": "школа",
        "sports": "спорт",
        "mecha": "меха",
        "isekai": "исекай",
        "supernatural": "сверхъестественное",
        "psychological": "психологический",
        "magical girl": "махо-сёдзё",
        "shounen": "сёнен",
        "seinen": "сэйнен",
        "shoujo": "сёдзё",
        "josei": "дзёсэй",
        "historical": "исторический"
    },
    "books": {
        "fantasy": "фэнтези",
        "sci-fi": "научная фантастика",
        "science fiction": "научная фантастика",
        "adventure": "приключения",
        "mystery": "детектив",
        "crime": "криминал",
        "thriller": "триллер",
        "horror": "ужасы",
        "romance": "романтика",
        "historical": "исторический роман",
        "biography": "биография",
        "memoir": "мемуары",
        "essay": "эссе",
        "poetry": "поэзия",
        "drama": "драма",
        "young adult": "подростковая проза",
        "children": "детская литература",
        "detective": "детектив",
        "dystopia": "антиутопия"
    }
}


resp_reco = """

Ответ — строго JSON-объект без каких-либо пояснений/текста вне JSON.
Схема полей: title (str), description (str), rating (list[str])

Никакого Markdown, кавычек-кодов и текста вне JSON. Только JSON.
Вопросы на русском языке
Если данных мало — делай общий, но корректный вопрос.


"""
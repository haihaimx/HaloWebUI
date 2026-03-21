import logging

import requests
from open_webui.retrieval.web.main import SearchResult
from open_webui.env import SRC_LOG_LEVELS
from yarl import URL

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


def search_jina(
    api_key: str,
    query: str,
    count: int,
    api_base_url: str = "https://s.jina.ai/",
) -> list[SearchResult]:
    """
    Search using Jina's Search API and return the results as a list of SearchResult objects.
    Args:
        api_key (str): The API key for Jina
        query (str): The query to search for
        count (int): The number of results to return
        api_base_url (str): Custom Jina API base URL

    Returns:
        list[SearchResult]: A list of search results
    """
    jina_search_endpoint = api_base_url

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": api_key,
        "X-Retain-Images": "none",
    }

    payload = {"q": query, "count": count if count <= 10 else 10}

    url = str(URL(jina_search_endpoint))
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    results = []
    for result in data["data"]:
        results.append(
            SearchResult(
                link=result["url"],
                title=result.get("title"),
                snippet=result.get("content"),
            )
        )

    return results

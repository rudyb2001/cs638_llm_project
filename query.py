from typing import List, Tuple
import os
from requests import get
from metaphor_python import Metaphor, SearchResponse

def metaphor_query(query: str) -> Tuple[SearchResponse, List[str]]:

    client = Metaphor(api_key="")

    response = client.search(
        query,
        num_results=10,
        use_autoprompt=True,
        type="neural"
    )

    # Fetch HTML content for each result
    html_content = get_html([result.url for result in response.results])

    return response, html_content

def get_html(urls: List[str]) -> List[str]:
    html_results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.3'}

    for url in urls:
        try:
            http_response = get(url, headers=headers)
            if http_response.status_code == 200:
                html_results.append(http_response.text)
            else:
                fail_msg = f"Failed to get content for {url}, with status code: {http_response.status_code}"
                print(fail_msg)
                html_results.append(fail_msg)
        except Exception as e:
            error_msg = f"An error occured while attempting to fetch {url}: {e}"
            print(error_msg)
            html_results.append(error_msg)
            
    return html_results


if __name__ == "__main__":
    my_query = "Butternut Squash Recipe"
    search_response, html_response = metaphor_query(my_query)

    # Create a new folder if it doesn't exist
    folder_path = 'search_output'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    print(search_response)
    
    # Save each HTML content as a new file
    for idx, html_content in enumerate(html_response):
        if html_content is not None:
            file_path = os.path.join(folder_path, f'result_{idx + 1}.html')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
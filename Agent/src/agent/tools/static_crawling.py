import requests
import re
from bs4 import BeautifulSoup

from src.agent.tools.base import BaseTool
from src.agent.tools.validate_wrapper import ValidateWrapper

class WebStaticCrawlingTool(BaseTool):
    name = "Statistics Web Crawling"
    description = "정적으로 특정 회사의 뉴스들을 크롤링해주는 도구 입니다."

    def _convert_code(self, stock_name: str) -> str:
        """
        종목명을 입력받으면 Code로 변환해주는 함수 (국내 주식만 가능함. 국내 주식은 개별 코드가 존재하기 때문에)
            e.g., 삼성전자 -> 005935
        :param code:
        :return: number string | None
        """
        url = "https://search.naver.com/search.naver"
        res = requests.get(url, params={"query": stock_name}, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, 'html.parser')

        # 종목 상세 페이지 링크 찾기
        links = soup.find_all('a', href=True)

        for a in links:
            href = a["href"]
            if "finance.naver.com/item/main.naver?code=" in href:
                # URL에서 종목 코드 추출
                match = re.search(r'code=(\d+)', href)
                if match:
                    return match.group(1)

    def _fetch_news_list(self, code_name: str, limit: int = 10) -> list:
        """
        네이버 뉴스에서 특정 키워드로 뉴스를 검색하여 제목과 링크를 반환하는 함수 (정적 크롤링)
        :param code_name: 검색할 키워드
        :param limit: 최대 뉴스 개수
        :return: 리스트 of dict -> [{"title": ..., "link": ...}, ...]
        """
        url = "https://search.naver.com/search.naver"
        res = requests.get(
            url,
            params={
                "where": "news",
                "query": code_name
            },
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        news_list = []
        seen_links = set() # 중복제거

        for a in soup.select("a[href*='article']"):
            link = a["href"]
            if link in seen_links:
                continue
            seen_links.add(link)
            span = a.select_one("span")
            if not span:
                continue

            # mark 제거
            for mark in span.select("mark"):
                mark.decompose()
            title = span.get_text(strip=True)
            if not title:
                continue
            news_list.append({
                "title": title,
                "link": link
            })
            if len(news_list) >= limit:
                break
        return news_list

    @ValidateWrapper
    def process(self, **kwargs) -> dict: # **kwargs: url, depth
        result_list = list()
        code_name = kwargs.get('code_name')
        if not code_name:
            raise ValueError("코드명 입력이 필요합니다.")
        news_list = self._fetch_news_list(code_name=code_name)
        for news in news_list:
            result_list.append(f"Title: {news['title']}\nLink: {news['link']}\n")
        return result_list

# Example usage:
if __name__ == "__main__":
    tool = WebCrawlingTool()
    result = tool.process(code_name="케이뱅크")
    print(result)


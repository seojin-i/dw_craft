from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from .base import BaseTool

class WebDynamicCrawlingTool(BaseTool):
    name = "Dynamic_Web_Crawling"
    description = "동적으로 특정 웹페이지를 크롬으로 열어주는 도구 입니다."
    def __init__(self, headless=True, auto_close=True):

        self.headless = headless
        self.auto_close = auto_close
        self.driver = self._create_driver()

    def schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "네이버 금융에서 특정 종목의 뉴스를 동적 크롤링으로 가져오는 도구입니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "종목 코드. 예: '005930' (삼성전자), '035720' (카카오)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "가져올 뉴스 개수 (기본값: 5)"
                        }
                    },
                    "required": ["code"]
                }
            }
        }

    def _create_driver(self):
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        return driver

    def fetch_news(self, code: str, limit: int = 5):
        url = f"https://finance.naver.com/item/news.naver?code={code}"

        self.driver.get(url)

        # 🔥 JS 로딩 대기
        time.sleep(3)

        # JS 렌더링 후 페이지 소스 가져오기
        html = self.driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        news_list = []
        seen = set()

        # 🔥 현재 구조 대응 (article / news_read 링크 기준)
        for a in soup.select("a[href*='article'], a[href*='news_read']"):
            link = a.get("href")
            if not link:
                continue

            if not link.startswith("http"):
                link = "https://finance.naver.com" + link

            if link in seen:
                continue
            seen.add(link)

            title = a.get_text(strip=True)
            if not title:
                continue

            news_list.append({
                "title": title,
                "link": link
            })

            if len(news_list) >= limit:
                break

        return news_list

    def _close(self):
        self.driver.quit()

    def process(self, **kwargs):
        code = kwargs.get("code", "277810")  # 기본값: 종목 코드 (예: '277810'은 카카오)
        limit = kwargs.get("limit", 10)  # 기본값: 가져올 뉴스 개수
        try:
            # 여기에 필요한 작업 수행
            news = self.fetch_news(code=code, limit=limit)
            for n in news:
                print(n["title"])
                print(n["link"])
                print("-" * 40)
            input("엔터 누르면 종료...")
        finally:
            if self.auto_close:
                self._close()

# agent = WebDynamicCrawlingTool(headless=False, auto_close=False)
# agent.process()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from bs4 import BeautifulSoup

app = FastAPI(
    title="Fashion AI MVP",
    description="무신사 상품 URL로부터 메타데이터를 추출하고 가짜 OOTD 추천을 반환하는 API",
    version="1.0.0"
)

# 요청 스키마 정의
class UrlRequest(BaseModel):
    url: str

# 응답 스키마 정의
class RecommendationResponse(BaseModel):
    title: str | None
    image_url: str | None
    ootd_recommendation: str

@app.get("/")
async def root():
    return {"message": "Fashion AI MVP API 서버가 실행 중입니다."}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(request: UrlRequest):
    target_url = request.url
    
    # HTTP 요청 헤더 (봇 차단 방지)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    
    try:
        # 비동기 HTTP 요청
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(target_url, headers=headers)
            response.raise_for_status()
            
            # BeautifulSoup을 사용한 HTML 파싱
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 메타 태그에서 상품명과 이미지 URL 추출 (무신사에서 주로 사용하는 OpenGraph 메타 태그 활용)
            meta_title = soup.find("meta", property="og:title")
            title = meta_title["content"] if meta_title else "상품명을 찾을 수 없습니다"
            
            meta_image = soup.find("meta", property="og:image")
            image_url = meta_image["content"] if meta_image else "이미지 URL을 찾을 수 없습니다"
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"URL에 접근할 수 없습니다: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"스크래핑 중 오류가 발생했습니다: {str(e)}")

    # 임시(Mock) OOTD 추천 텍스트
    mock_ootd = "이 상의에는 세미 오버핏 블랙 슬랙스와 더비 슈즈를 매치하여 깔끔한 미니멀룩을 연출하는 것을 추천합니다!"

    return RecommendationResponse(
        title=title,
        image_url=image_url,
        ootd_recommendation=mock_ootd
    )

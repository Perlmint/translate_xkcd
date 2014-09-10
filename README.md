# translate_xkcd

[![Build Status](https://travis-ci.org/omniavinco/translate_xkcd.svg?branch=master)](https://travis-ci.org/omniavinco/translate_xkcd)

Translate xkcd

[xkcd](http://xkcd.com/)의 만화를 한국어로 번역, 제공하는 프로젝트

## 번역 요령

xkcd사이트에서 아직 번역 안된 이미지를 받아서 번역을 하고
res폴더에 이미지를, src폴더에 기타 정보(작성자, 파일명, 제목 등)을 작성해서
풀 리퀘스트를 보내주시면 메타 정보 검토와 간단한 번역 검토 후에 적용해드리겠습니다.

### 번역을 할 때 주의 사항

1. 폰트는 네이버에서 제공하고 있는 나눔손글씨체를 사용한다.
    * 원래 xkcd에서 사용하고 있는 comic-sans와 비슷한 느낌이며 라이센스상 문제가 발생할 가능성이 없어서 선택됨
2. 이미지 리소스는 png포맷으로 저장한다.
3. 이미지 리소스는 ID.TITLE.png의 형태를 취한다.


## 라이센스

번역된 리소스(res폴더 안의 이미지)에 대해서는
[xkcd에 적용된 라이센스](http://xkcd.com/license.html)인 [Creative Commons License 2.5 Attribution-Noncommercial](http://creativecommons.org/licenses/by-nc/2.5/)을 동일하게 적용합니다.

그 외의 HTML 템플릿 파일(templates폴더 안의 html파일들), HTML생성 스크립트(render.py), travis-ci관련 파일(.travis.yml)은 [MIT라이센스](http://opensource.org/licenses/MIT)를 적용합니다. 

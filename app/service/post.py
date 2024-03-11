from bs4 import BeautifulSoup
from core.driver import get_driver
from fastapi import Depends
from schema import Post
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_latest_post_id_from_band(band_id, driver=Depends(get_driver)) -> int:
    driver.get(f"https://band.us/band/{band_id}")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                '//*[@data-viewname="DPostListView" and contains(@class, "postWrap")]',
            )
        )
    )
    post_list_html = driver.execute_script("return document.documentElement.outerHTML;")
    _post_summary = get_post_summary(band_id, post_list_html)

    return int(_post_summary[0]["id"])


def get_post_detail(band_id, post_id, driver=Depends(get_driver)) -> Post:
    driver.get(f"https://band.us/band/{band_id}/post/{post_id}")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "postMain"))
    )
    post_html = driver.execute_script("return document.documentElement.outerHTML;")

    soup = BeautifulSoup(post_html, "lxml")
    post_head = soup.find("div", class_="postWriterInfoWrap")
    created_at = post_head.find("time", class_="time").text
    try:
        view_count = post_head.find("span", class_="readCount").text.split(" ")[0]
    except AttributeError:
        view_count = "0"
    post = soup.find("div", class_="postBody")
    _post_text_list = post.find_all(
        "div", attrs={"data-viewname": "DPostTextView", "class": "dPostTextView"}
    )
    post_text_list = [p.get_text(separator="\n") for p in _post_text_list]
    post_text = "\n".join(post_text_list)

    count_divs = soup.find("div", class_="postCount")
    try:
        comment_count = count_divs.find_all("span", class_="count")[-1].text
    except AttributeError:
        comment_count = "0"
    return Post(
        id=post_id,
        content=post_text[2:-4],
        band_id=band_id,
        comments_count=comment_count,
        view_count=view_count,
        created_at=created_at,
    )


def get_post_summary(band_id, html) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    link_divs = soup.find_all("div", class_="_postAuthorRegion")
    body_divs = soup.find_all("div", class_="postBody")
    count_divs = soup.find_all("div", class_="postCount")
    a_tags = []
    p_tags = []
    comment_counts = []
    view_counts = []
    for div in link_divs:
        a_tag = div.find(
            "a",
            href=lambda href: href
            and href.startswith(f"https://band.us/band/{band_id}/post/"),
        )
        if a_tag is not None:
            a_tags.append(a_tag.get("href"))

    for div in body_divs:
        p_tag = div.find("p", class_="txtBody")
        body_head = p_tag.get_text(separator="\n")
        p_tags.append(body_head)

    for div in count_divs:
        try:
            comment_count = (
                div.find("button", class_="comment _commentCountBtn").find("span").text
            )
        except AttributeError:
            comment_count = 0
        view_count = (
            div.find("div", class_="postCountRight").find("span", class_="count").text
        )
        comment_counts.append(comment_count)
        view_counts.append(view_count)

    zipped = zip(a_tags, p_tags, comment_counts, view_counts)
    post_summary = []
    for a, p, _comment_counts, _view_counts in zipped:
        post_summary.append(
            {
                "id": a.split("/")[-1],
                "content": p,
                "band_id": band_id,
                "comments_count": _comment_counts,
                "view_count": _view_counts,
            }
        )
    return post_summary

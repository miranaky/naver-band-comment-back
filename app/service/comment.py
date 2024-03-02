import platform
import time

from fastapi import Depends
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.core.driver import get_browser_driver
from app.models import CreateComment


class CreateCommentService:
    ctrl = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

    def __init__(
        self,
        new_comment: CreateComment,
        driver=Depends(get_browser_driver),
    ):
        self.driver = driver
        self.new_comment = new_comment
        self.comments_count = 0
        self.tagged_comments_count = 0
        self.chunk_size = 100

    def click_first_comment_button(self):
        try:
            go_to_first_comment_button = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "goFirstComment"))
            )
            go_to_first_comment_button.click()
        except TimeoutException:
            print("No first comment button")
            pass

    def click_more_comment_button(self):
        counter = 0
        while True:
            try:
                more_comment_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "moreView"))
                )
                more_comment_button.click()
                self.driver.find_element(By.CLASS_NAME, "moreView")
                time.sleep(1)

            except TimeoutException:
                if counter > 2:
                    print("No more comment button")
                    break  # 요소가 존재하지 않으면 루프를 종료
                time.sleep(1)
                counter += 1
                continue

    def get_all_comments(self):
        self.driver.get(
            f"https://band.us/band/{self.new_comment.band_id}/post/{self.new_comment.post_id}"
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dPostCommentMainView"))
        )

        number_of_comments_div = self.driver.find_element(
            By.CSS_SELECTOR, "span.comment._commentCountBtn.gCursorDefault span.count"
        )
        number_of_comments = int(number_of_comments_div.text)

        if number_of_comments > 10:
            self.click_first_comment_button()
            self.click_more_comment_button()
        comment_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.cComment")
        count = 0
        while count < 2:
            comment_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.cComment")
            if len(comment_divs) == int(number_of_comments):
                self.comments_count = len(comment_divs)
                print("댓글 갯수가 일치합니다.")
                break
            print(
                f"댓글 갯수가 일치하지 않습니다. {len(comment_divs)} / {number_of_comments}"
            )
            time.sleep(1)
            count += 1
        return comment_divs

    def click_name_with_condition(self, comment):
        name_button = comment.find_element(By.CSS_SELECTOR, "button.nameWrap")
        if name_button.text == self.new_comment.my_name:
            return None
        try:
            comment_body = comment.find_element(
                By.CSS_SELECTOR, "p.txt._commentContent"
            )
        except:
            # 댓글이 없이 스티커만 있는 경우
            return None
        action_chain = ActionChains(self.driver)

        if self.new_comment.check_message is None:
            action_chain.move_to_element(name_button).click(name_button).perform()
        else:
            if self.new_comment.check_message in comment_body.text:
                action_chain.move_to_element(name_button).click(name_button).perform()
        return name_button.text, comment_body.text

    def add_all_tagged_comment(self):
        comment_divs = self.get_all_comments()
        num_chunks = len(comment_divs) // self.chunk_size + (
            len(comment_divs) % self.chunk_size > 0
        )
        for i in range(num_chunks):
            current_chunk = comment_divs[
                i * self.chunk_size : (i + 1) * self.chunk_size
            ]
            # 댓글을 입력한 사용자의 이름을 클릭합니다.
            for idx, comment in enumerate(current_chunk):
                result = self.click_name_with_condition(comment)
                if result is None:
                    continue
                print(f"{idx+1}번째 댓글 {result[0]} : {result[1]}")
            # 댓글을 입력할 수 있는 textarea를 찾습니다.
            input_section = self.driver.find_element(By.CLASS_NAME, "uInputComment")
            text_area = input_section.find_element(By.TAG_NAME, "textarea")
            text_area.send_keys(self.new_comment.my_comment)

            # input_section html 출력
            # submit 버튼을 찾습니다.
            send_button = WebDriverWait(self.driver, 2).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".writeSubmit.uButton._sendMessageButton.-active")
                )
            )

            text_area = input_section.find_element(By.TAG_NAME, "textarea")
            self.tagged_comments_count = (
                len(text_area.get_attribute("value").split("@")) - 1
            )
            print(text_area.get_attribute("value"))
            print(self.tagged_comments_count)
            print("댓글 갯수 : ", len(comment_divs))
            if self.tagged_comments_count > 0:
                print("Tagged comments count: ", self.tagged_comments_count)
                # 버튼을 클릭합니다.
                # send_button.click()
                action_chain = ActionChains(self.driver)
                action_chain.click(text_area).key_down(self.ctrl).send_keys("a").key_up(
                    self.ctrl
                ).send_keys(Keys.DELETE).perform()
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "dPostCommentMainView")
                    )
                )

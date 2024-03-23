import platform
import time

from fastapi import Depends
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.core.driver import get_driver
from app.models import CreateComment


class CreateCommentService:
    ctrl = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL

    def __init__(
        self,
        new_comment: CreateComment,
        driver=Depends(get_driver),
    ):
        self.driver = driver
        self.new_comment = new_comment
        self.comments_count = 0
        self.tagged_comments_count = 0
        self.chunk_size = 100

    def get_my_name(self):
        if self.new_comment.my_name is None and self.new_comment.new:
            self.driver.get(f"https://band.us/band/{self.new_comment.band_id}/member")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "ul.cMemberList._memberList")
                )
            )
            first_li = self.driver.find_element(
                By.CSS_SELECTOR, "ul.cMemberList._memberList > li:first-child"
            )
            self.new_comment.my_name = first_li.text.split("\n")[0]

    def click_first_comment_button(self):
        try:
            go_to_first_comment_button = WebDriverWait(self.driver, 5).until(
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
                more_comment_button = WebDriverWait(self.driver, 5).until(
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
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "span.comment._commentCountBtn.gCursorDefault span.count",
                )
            )
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
        if len(comment_divs) > number_of_comments:
            print(f"전체 댓글 갯수를 못 불러왔습니다.  {number_of_comments}")
            number_of_comments_div = self.driver.find_element(
                By.CSS_SELECTOR,
                "span.comment._commentCountBtn.gCursorDefault span.count",
            )
            number_of_comments = int(number_of_comments_div.text)
            self.click_first_comment_button()
            self.click_more_comment_button()
        while count < 5:
            comment_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.cComment")
            if len(comment_divs) == int(number_of_comments):
                self.comments_count = len(comment_divs)
                print(
                    f"댓글 갯수가 일치합니다. {len(comment_divs)} : {number_of_comments}"
                )
                break
            print(
                f"댓글 갯수가 일치하지 않습니다. {len(comment_divs)} : {number_of_comments}"
            )
            time.sleep(1)
            count += 1
        return comment_divs

    def click_name_with_condition(self, comment, tagged_users: set):
        name_button = comment.find_element(By.CSS_SELECTOR, "button.nameWrap")

        if (
            self.new_comment.my_name is not None
            and self.new_comment.my_name[:-1] in name_button.text
        ):
            return None
        if len(tagged_users) > 0:
            if name_button.text in tagged_users:
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

    def get_tagged_users(self, comment_divs):
        # 댓글 내용 중에서 태그된 사용자를 모아야 함
        tagged_users = set()
        for idx, comment in enumerate(comment_divs):
            # 댓글을 입력한 사용자의 이름을 확인합니다. 그 이름이 내 이름이면 그 댓글 안에 태그된 사용자가 있는지 확인합니다.
            # 태그된 사용자가 있으면 그 사용자를 tagged_users에 추가합니다.
            name_button = comment.find_element(By.CSS_SELECTOR, "button.nameWrap")
            if self.new_comment.my_name[:-1] not in name_button.text:
                continue
            try:
                comment_body = comment.find_element(
                    By.CSS_SELECTOR, "p.txt._commentContent"
                )
                tagged_users_tag = comment_body.find_elements(
                    By.CSS_SELECTOR, "a.gBandMember"
                )
            except:
                # 댓글이 없이 스티커만 있는 경우
                pass

            if len(tagged_users_tag) == 0:
                continue
            tagged_users_text = [user.text.split("@")[1] for user in tagged_users_tag]
            tagged_users.update(tagged_users_text)
        return tagged_users

    def write_comment(self, text_area):
        try:
            JS_ADD_TEXT_TO_INPUT = """
            var elm = arguments[0], txt = arguments[1];
            elm.value += txt;
            elm.dispatchEvent(new Event('change'));
            """
            self.driver.execute_script(
                JS_ADD_TEXT_TO_INPUT, text_area, self.new_comment.my_comment
            )
            text_area.send_keys(".")
            text_area.send_keys(Keys.BACKSPACE)
        except Exception as e:
            print(f"Failed to add comment ({e})")
            raise e

    def add_all_tagged_comment(self):
        comment_divs = self.get_all_comments()
        tagged_users = set()
        if self.new_comment.new:
            # 댓글 내용 중에서 태그된 사용자를 모아야 함
            tagged_users = self.get_tagged_users(comment_divs)
        num_chunks = len(comment_divs) // self.chunk_size + (
            len(comment_divs) % self.chunk_size > 0
        )
        for i in range(num_chunks):
            current_chunk = comment_divs[
                i * self.chunk_size : (i + 1) * self.chunk_size
            ]
            # 댓글을 입력한 사용자의 이름을 클릭합니다.
            for comment in current_chunk:
                result = self.click_name_with_condition(comment, tagged_users)
                if result is None:
                    continue
            # 댓글을 입력할 수 있는 textarea를 찾습니다.
            input_section = self.driver.find_element(By.CLASS_NAME, "uInputComment")
            text_area = input_section.find_element(By.TAG_NAME, "textarea")
            self.write_comment(text_area)
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

            if self.tagged_comments_count > 0:
                # 버튼을 클릭합니다.
                send_button.click()
                time.sleep(1)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "dPostCommentMainView")
                    )
                )

    def add_comment(self):
        """
        태그를 하지 않고 댓글을 달 때 사용합니다.
        """
        self.driver.get(
            f"https://band.us/band/{self.new_comment.band_id}/post/{self.new_comment.post_id}"
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dPostCommentMainView"))
        )
        # 댓글을 입력할 수 있는 textarea를 찾습니다.
        input_section = self.driver.find_element(By.CLASS_NAME, "uInputComment")
        text_area = input_section.find_element(By.TAG_NAME, "textarea")
        self.write_comment(text_area)

        # input_section html 출력
        # submit 버튼을 찾습니다.
        send_button = WebDriverWait(self.driver, 2).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".writeSubmit.uButton._sendMessageButton.-active")
            )
        )
        send_button.click()
        time.sleep(1)

    def create_comment(self):
        if self.new_comment.tag:
            self.get_my_name()
            self.add_all_tagged_comment()
        else:
            self.add_comment()

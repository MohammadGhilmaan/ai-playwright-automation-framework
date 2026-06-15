from playwright.sync_api import Page, expect
from utils.ai_locator import get_ai_locator_sync


class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://demo.playwright.dev/todomvc"

    def goto(self):
        self.page.goto(self.url)

    def add_todo(self, task_name: str):
        input_field = self.page.get_by_placeholder("What needs to be done?")
        input_field.fill(task_name)
        input_field.press("Enter")

    def complete_first_todo_with_ai(self):
        # 1. Get the DOM synchronously (No 'await' needed!)
        dom_snapshot = self.page.evaluate("document.body.innerHTML")

        # 2. Pass the HTML string to our sync AI utility
        ai_locator_string = get_ai_locator_sync(dom_snapshot, "the checkbox to mark the first todo item as complete")

        try:
            checkbox = self.page.locator(ai_locator_string).first
            checkbox.click()
            print(f"✅ Successfully clicked using AI locator: {ai_locator_string}")
        except Exception:
            print("⚠️ AI locator failed. Using traditional fallback.")
            self.page.locator(".todo-list li").first.locator(".toggle").click()

    def verify_first_todo_is_completed(self):
        expect(self.page.locator(".todo-list li").first).to_have_class("completed")
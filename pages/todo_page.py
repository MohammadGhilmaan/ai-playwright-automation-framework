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
        dom_snapshot = self.page.evaluate("document.body.innerHTML")
        ai_locator_string = get_ai_locator_sync(dom_snapshot, "the checkbox to mark the first todo item as complete")

        # PROFESSIONAL FALLBACK: If AI returns None (e.g., in CI/CD), use traditional locator
        if ai_locator_string is None:
            print("⚠️ AI unavailable in this environment. Using traditional fallback locator.")
            self.page.locator(".todo-list li").first.locator(".toggle").click()
            return

        try:
            checkbox = self.page.locator(ai_locator_string).first
            checkbox.click()
            print(f"✅ Successfully clicked using AI locator: {ai_locator_string}")
        except Exception:
            print("⚠️ AI locator failed to click. Using traditional fallback.")
            self.page.locator(".todo-list li").first.locator(".toggle").click()

    def verify_first_todo_is_completed(self):
        expect(self.page.locator(".todo-list li").first).to_have_class("completed")
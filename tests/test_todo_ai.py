from playwright.sync_api import Page
from pages.todo_page import TodoPage
import allure


@allure.feature("Todo Application")
@allure.story("AI-Powered Task Completion")
def test_add_and_complete_todo_with_ai(page: Page):
    """
    Test Case: Verify a user can add a task and mark it as complete using AI locators.
    """
    # 1. Initialize the Page Object
    todo_page = TodoPage(page)

    # 2. Allure Step: Navigation
    with allure.step("Navigate to TodoMVC application"):
        todo_page.goto()

    # 3. Allure Step: Add a task
    with allure.step("Add a new todo item: 'Learn AI Automation'"):
        todo_page.add_todo("Learn AI Automation")

    # 4. Allure Step: Complete task using AI
    with allure.step("Mark the first todo as complete using AI Self-Healing Locator"):
        todo_page.complete_first_todo_with_ai()

    # 5. Allure Step: Assertion
    with allure.step("Verify the todo item is marked as completed"):
        todo_page.verify_first_todo_is_completed()
from selenium.webdriver.common.by import By


class Locator:
    """Все необходимые селекторы"""
    ID = (By.CSS_SELECTOR, "span.Text__jKJsQramuu[data-name='Text']")
    ROWS = (By.CSS_SELECTOR, "div.All-supplies-table-row__C6iU8GGIHd[role='button'][tabindex='0']")
    STATUS = (By.CSS_SELECTOR, "span.Badge__qTItng6q8g[data-name='Badge']")
    PLAN = (By.CSS_SELECTOR, "div.Supply-detail-options__plan-desktop-button__-N407e2FDC button")
    CONFIRM = (By.XPATH, 'button.button__I8dwnFm136')
    DATE = (By.CSS_SELECTOR, "div.Calendar-cell__date-container__2TUSaIwaeG span")
    RATE = (By.CSS_SELECTOR, "div.Coefficient-table-cell__EqV0w0Bye8")
    CHOOSE_HOVER = (By.CSS_SELECTOR, 'div.Calendar-cell__button-container__ANliSQlw9D')
    CHOOSE = (By.XPATH, '//button[span[text()="Выбрать"]]')
    CELLS_TABLE = (By.CSS_SELECTOR, "div.Calendar-cell__cell-content__EoHgwsbqB0")
    NAVIGATOR = (By.CSS_SELECTOR, '[data-testid="menu.section.supply-management-button-link"]')
    LI_NAVIGATOR = (By.CSS_SELECTOR, '[data-testid="menu.supply-management-front-button-link"]')
    PAGINATION = (By.CSS_SELECTOR, "input[name=pagination-select]")
    OPTIONS = (By.CSS_SELECTOR, "div.Custom-select-option__HLXYwVWDUc span")
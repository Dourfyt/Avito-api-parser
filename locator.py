from selenium.webdriver.common.by import By


class Locator:
    """Все необходимые селекторы"""
    ID = (By.CSS_SELECTOR, "[id='preorderID']")
    ROWS = (By.CSS_SELECTOR, "div.All-supplies-table-row__C6iU8GGIHd[role='button'][tabindex='0']")
    STATUS = (By.CSS_SELECTOR, "[data-name='Badge']")
    PLAN = (By.CSS_SELECTOR, ".caption_kqFcIewCT5")
    CONFIRM = (By.CSS_SELECTOR, '')
    CANCEL = (By.CSS_SELECTOR, '.Calendar-plan-buttons--cancel__bMSoh-OauP')
    RATE = (By.CSS_SELECTOR,".Calendar-cell__amount-cost__DgFCG5om3L")
    RATE_X = (By.CSS_SELECTOR,'.Text__jKJsQramuu Text--body-xs__rO4cjFs0Uk Text--black__hIzfx5PELf Text--textDecoration-none__rkxLphaqR0')
    CHOOSE_HOVER = (By.CSS_SELECTOR, ".Custom-popup")
    CHOOSE = (By.CSS_SELECTOR,".Custom-popup")
    ROW_TABLE = (By.CSS_SELECTOR, ".Calendar-plan-view__calendar-row")
    TEST = (By.CSS_SELECTOR, ".Select__input__-CFKpO5qqT")
    NAVIGATOR = (By.CSS_SELECTOR, '[data-testid="menu.section.supply-management-button-link"]')
    LI_NAVIGATOR = (By.CSS_SELECTOR, '[data-testid="menu.supply-management-front-button-link"]')
from selenium.webdriver.common.by import By


class Locator:
    """Все необходимые селекторы"""
    ID = (By.CSS_SELECTOR, "span.Text__jKJsQramuu[data-name='Text']")
    ROWS = (By.CSS_SELECTOR, "div.All-supplies-table-row__C6iU8GGIHd[role='button'][tabindex='0']")
    STATUS = (By.CSS_SELECTOR, "span.Badge__qTItng6q8g[data-name='Badge']")
    PLAN = (By.CSS_SELECTOR, "div.Supply-detail-options__plan-desktop-button__-N407e2FDC button")
    CONFIRM = (By.CSS_SELECTOR, '')
    CANCEL = (By.CSS_SELECTOR, '.Calendar-plan-buttons--cancel__bMSoh-OauP')
    RATE = (By.CSS_SELECTOR,".Calendar-cell__amount-cost__DgFCG5om3L")
    RATE_X = (By.CSS_SELECTOR,'.Text__jKJsQramuu Text--body-xs__rO4cjFs0Uk Text--black__hIzfx5PELf Text--textDecoration-none__rkxLphaqR0')
    CHOOSE_HOVER = (By.CSS_SELECTOR, ".Custom-popup")
    CHOOSE = (By.CSS_SELECTOR,".Custom-popup")
    CELLS_TABLE = (By.CSS_SELECTOR, "div.Calendar-cell__cell-content__EoHgwsbqB0")
    TEST = (By.CSS_SELECTOR, ".Select__input__-CFKpO5qqT")
    NAVIGATOR = (By.CSS_SELECTOR, '[data-testid="menu.section.supply-management-button-link"]')
    LI_NAVIGATOR = (By.CSS_SELECTOR, '[data-testid="menu.supply-management-front-button-link"]')
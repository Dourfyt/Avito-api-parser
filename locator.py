from selenium.webdriver.common.by import By


class Locator:
    """Все необходимые селекторы"""
    ID = (By.CSS_SELECTOR, "[id='preorderID']")
    ROWS = (By.CSS_SELECTOR, "All-suplies-table-row__C6iU8GGIhd")
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
    NAVIGATOR = (By.CSS_SELECTOR, ".button-link_Button-link__BkNzZ button-link_Button-link--button__VBlT9 button-link_Button-link--list-item__u-gjf button-link_Button-link--button-small__7YJ-w")
    LI_NAVIGATOR = (By.CSS_SELECTOR, ".text_Text__60ecO text_Text--body-m__QbFDv text_Text--inherit__kLuQ1 text_Text--white-space-nowrap__uHONd text_Text--textDecoration-none__RR11p")
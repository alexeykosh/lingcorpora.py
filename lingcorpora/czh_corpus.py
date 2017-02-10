from selenium import webdriver


CORP_URL='https://kontext.korpus.cz'
CLASS_NAMES = {'word':'query', 'corpus':'qselector'}


def get_page_src(*args):
    _driver = _driver_init()
    _arg_list = _make_keys_lists(args)
    _send_all_keys_to_forms(_driver, CLASS_NAMES.values(), _arg_list)
    _wait_till_load(_driver)
    html_src = _driver.page_source
    _driver.close()
    return html_src


def _make_keys_lists(args):
    output_list = []
    for arg,class_name in zip(args,CLASS_NAMES.values()):
        output_list.append(arg)
    return output_list


def _wait_till_load(queued_webdriver):
    _query_string = queued_webdriver.current_url.split('/')[3]
    while not _query_string.startswith('view'):
        _query_string = queued_webdriver.current_url.split('/')[3]
        continue
    return None


def _send_all_keys_to_forms(webdriver, form_html_classes, keys):
    for key,form_html_class in zip(keys,form_html_classes):
        print(key, form_html_class)
        form = webdriver.find_element_by_class_name(form_html_class)

        form.send_keys(key)
    triggering_form = webdriver.find_element_by_class_name('query')
    triggering_form.submit()
    return None


def _driver_init(driver_type='Chrome'):
    driver = eval('webdriver.'+ driver_type)()
    driver.get(CORP_URL)
    return driver


def main():
    get_page_src('tata','Basic')

if __name__ == '__main__':
    main()


def open_second_tab(d, url):
    d.execute_script(f'''window.open("{url}","_blank");''')


def switch_tabs(d):
    current_tab = d.current_window_handle

    # check all the tabs, switch to the one that differs from the current tab
    for tab in d.window_handles:
        if tab != current_tab:
            d.switch_to.window(tab)


# def open_tabs(d):
#     d.execute_script("window.open('');")
#     d.switch_to.window(d.window_handles[1])
#     d.get(TARGET_URLS['grammar_url'])
#     d.switch_to.window(d.window_handles[0])

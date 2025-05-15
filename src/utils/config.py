TARGET_URLS = {
    'dictation_url': 'https://speechnotes.co/dictate/',
    'grammar_url': 'https://www.deepl.com/write'
}

XPATH_LIBRARY = {
    'record_button': '//div[@id="start_button"]',
    'text_area': '//div[@id="output_box"]/textarea',
    'text_mirror': '//div[@id="mirror_container"]//div',
    'lan_selector': '//select[@id="select_language"]',
    'ES': '//option[contains(., "España")]',
    'EN': '//option[contains(., "UK")]',

}

VOICE_COMMANDS = {
    "toggle recording": "toggle_record",    
    "stop execution": "toggle_record",    
    "start execution": "toggle_record",    
    "switch to spanish": "ES",   
    
    "cambiar a inglés": "EN",
    "activar grabación": "toggle_record",
    "alternar grabación": "toggle_record"
    # "",    
}

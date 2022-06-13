BOOST_TYPE_NAME_TO_NUMBER = {
    'casual': 0, # Классический буст
    'auto': 1, # Автоматический буст
} 

BOOST_TYPE_CHOICES = {
    (BOOST_TYPE_NAME_TO_NUMBER['casual'], 'casual'),
    (BOOST_TYPE_NAME_TO_NUMBER['auto'], 'auto'),
}

BOOST_TYPE_VALUES = {
    BOOST_TYPE_NAME_TO_NUMBER['casual']: {
        'click_power_scale': 1, # В классическом бусте сила клика будет оставаться такой, какая она есть.
        'auto_click_power_scale': 0, # В классическом бусте сила автоклика будет уничтожена.
        'price_scale': 5, # Немного вырастет в цене.
    },
    BOOST_TYPE_NAME_TO_NUMBER['auto']: {
        'click_power_scale': 0, # В автоматическом бусте сила клика будет самовыпиливаться.
        'auto_click_power_scale': 1, # В автоматическом бусте сила автоклика останется прежней.
        'price_scale': 25, # Невероятно вырастет в цене.
    }
}
from functions_utility import set_up, choose_city, choose_check_in_and_out_dates, choose_guests_amount, click_search, choose_type_of_place, set_max_price, navigate_to_next_page

set_up('https://www.airbnb.com/')
choose_city("Odessa")
choose_check_in_and_out_dates("2020-09-15", "2020-09-16")
choose_guests_amount(2)
click_search()
choose_type_of_place('Entire')
set_max_price("25")
navigate_to_next_page()

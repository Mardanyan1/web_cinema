import schedule
import time
from ivi_all_parse import ivi_search_all


schedule.every(0.5).minutes.do(ivi_search_all)
# schedule.every().hour.do(ivi_search_all)
# schedule.every().day.at("4:32").do(ivi_search_all)

while True:
    schedule.run_pending()
    time.sleep(1)

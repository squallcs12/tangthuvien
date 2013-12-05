from .user_daily_login_history import UserDailyLoginHistory
from .thank_point import ThankPoint, ThankPointHistory

def import_signal():
    from thankshop import signals  # @UnusedImport
import_signal()

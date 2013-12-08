from .user_daily_login_history import UserDailyLoginHistory
from .thank_point import ThankPoint, ThankPointHistory
from .package import Package

def import_signal():
    from thankshop import signals  # @UnusedImport
import_signal()

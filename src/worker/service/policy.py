# служба, подтверждающая отправку уже сформированного уведомления
# проводит проверки актуальности и исполнения настроек
# отвечает за групповые нотификации по частям, трекинг состояний нотификаций
# last_content last_updated_time

from lib.model.notification import Notification
from lib.model.user import User

from lib.api.v1.admin.user import IUserInfo
from lib.api.v1.admin.notification import INotification


class PolicyService():
    '''Check sender policy and user subscription settings'''
    def __init__(
            self,
            iuserinfo: IUserInfo,
            inotification: INotification
    ):
        self.userinfo: IUserInfo = iuserinfo
        self.notifier = inotification

    # Python program to illustrate the intersection
    # of two lists using set() method
    @staticmethod
    def intersection(lst1, lst2):
        return list(set(lst1) & set(lst2))

    def check_user_policy(self, notice: Notification, user: User) -> bool:
        '''Individual user groups to subscribe for notification types'''
        user_group = self.userinfo.get_user_groups(user.id)
        notice_group = self.notifier.get_target_groups(notice)

        match = PolicyService.intersection(user_group, notice_group)
        if len(match):
            return True
        return False

    def check_notification_policy(self, notice: Notification) -> bool:
        '''Common policies for notification maillists - priority over user'''
        target_groups = self.notifier.get_target_groups(notice)
        if 'all' in target_groups:
            return True
        return False

    def check_unified_policy(self, user: User, notice: Notification) -> bool:
        '''Managers can enforce sending notifications to all'''
        return self.check_notification_policy(notice) or self.check_user_policy(notice, user)

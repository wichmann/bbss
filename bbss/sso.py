
"""
bbss - BBS Student Management

Upload student users to school server for Single SignOn.

Created on Fri Jan 31 08:43:12 2025

@author: Christian Wichmann
"""


import logging
import logging.handlers

import authentik_client
from authentik_client.rest import ApiException

from bbss import data


__all__ = ['upload_data']


logger = logging.getLogger('bbss.sso')


def upload_data(student_list):
    userManagement = UserManagement('auth.xxx.com', '')
    userManagement.import_users(student_list)


class UserManagement:
    def __init__(self, authentik_domain: str, token: str):
        self._host = f'https://{authentik_domain}/api/v3'
        self._token = token
        configuration = authentik_client.Configuration(
            host=self._host,
            access_token=self._token
        )
        self._api_client = authentik_client.ApiClient(configuration)
        self._core_api = authentik_client.CoreApi(self._api_client)

    def _list_users(self):
        api_response = self._core_api.core_users_list()
        result = []
        for u in api_response.results:
            result.append((u.username, u.name, u.email))
        return result

    def _list_groups(self):
        api_response = self._core_api.core_groups_list()
        for g in api_response.results:
            logger.debug(f'Group "{g.name}" has {len(g.users_obj)} users.')
        return api_response.results

    def _create_user(self, name, username, email):
        logger.info(f'Creating user {username}...')
        api_response = self._core_api.core_users_create(
            user_request={'name': name, 'username': username, 'email': email}
        )
        logger.info(f'Created user {api_response.username} with email {api_response.email} and assigned user id {api_response.pk}')
        return api_response.pk

    def _find_group_id(self, group_name: str):
        return [g for g in self._list_groups() if g.name == group_name][0].pk

    def _create_group_for_class(self, group_name):
        logger.info(f'Creating group {group_name}...')
        parent_group = self._find_group_id('Schülerinnen und Schüler')
        api_response = self._core_api.core_groups_create(
            user_request={'name': group_name, "is_superuser": False, 'parent': parent_group}
            # "users": [ 0 ],
        )
        logger.info(f'Created group {api_response.name} with id {api_response.pk}')
        return api_response.pk

    def _set_user_password(self, userid, password):
        logger.info(f'Setting password for user no. {userid}...')
        api_response = self._core_api.core_users_set_password_create(
            id=userid, user_password_set_request={'password': password}
        )
        #logger.debug(api_response)

    def _add_user_to_group(self, userid, group_name):
        logger.info(f'Adding user no. {userid} to group "{group_name}"...')
        try:
            group_id = self._find_group_id(group_name)
            api_response = self._core_api.core_groups_add_user_create(
                group_uuid=group_id, user_account_request={'pk': userid}
            )
            #logger.debug(api_response)
        except ApiException as e:
            print('Exception while adding user to group: %s\n' % e)

    def import_users(self, student_list):
        try:
            for student in student_list:
                logger.debug(f'Uploading: {student.firstname} {student.surname}, {student.user_id}, {student.email}')
                userid = self._create_user(f'{student.firstname} {student.surname}', student.user_id.casefold(), student.email)
                self._set_user_password(userid, student.password)
                self._add_user_to_group(userid, 'Schülerinnen und Schüler')
        except ApiException as e:
            print('Exception while importing users: %s\n' % e)

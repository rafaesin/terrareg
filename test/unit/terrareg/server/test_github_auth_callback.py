
import datetime
import unittest.mock

import pytest

import terrareg.errors
from terrareg.namespace_type import NamespaceType
from test.unit.terrareg import TerraregUnitTest, mock_models
from test import client, app_context, test_request_context
import terrareg.auth
from test.integration.terrareg.fixtures import test_github_provider_source


class TestGithubAuthCallback(TerraregUnitTest):
    """Test Github Auth callback API."""

    @pytest.mark.parametrize('query_string, expected_code', [
        ('', None),
        ('?code=', ''),
        ('?code=testcode', 'testcode')
    ])
    def test_with_invalid_code(self, query_string, expected_code, client, mock_models, test_github_provider_source):
        """Test endpoint without valid code."""
        with unittest.mock.patch('terrareg.config.Config.SECRET_KEY', 'abcdefg'), \
                unittest.mock.patch('terrareg.audit.AuditEvent.create_audit_event') as mock_create_audit_event, \
                unittest.mock.patch('terrareg.models.Session.cleanup_old_sessions', create=True) as cleanup_old_sessions_mock, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.get_user_access_token', unittest.mock.MagicMock(return_value=None)) as mock_get_access_token:
            # Update real app secret key
            self.SERVER._app.secret_key = 'abcdefg'

            res = client.get(f"/test-github-provider/callback{query_string}")

            assert res.status_code == 200
            assert "Invalid code returned from test-github-provider" in res.data.decode('utf-8')

            mock_get_access_token.assert_called_once_with(expected_code)

            # Ensure session variables have not been set
            with client.session_transaction() as session:
                assert session == {}

    def test_unable_to_get_username(self, client, mock_models, test_github_provider_source):
        """Test endpoint without being able to get valid username."""
        with unittest.mock.patch('terrareg.config.Config.SECRET_KEY', 'abcdefg'), \
                unittest.mock.patch('terrareg.audit.AuditEvent.create_audit_event') as mock_create_audit_event, \
                unittest.mock.patch('terrareg.models.Session.cleanup_old_sessions', create=True) as cleanup_old_sessions_mock, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.get_user_access_token', unittest.mock.MagicMock(return_value="unittestaccesstoken")) as mock_get_access_token, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.get_username', unittest.mock.MagicMock(return_value=None)) as mock_get_username, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.update_repositories', unittest.mock.MagicMock()) as mock_update_repositories:
            # Update real app secret key
            self.SERVER._app.secret_key = 'abcdefg'

            res = client.get(f"/test-github-provider/callback?code=abc")

            assert res.status_code == 200
            assert "Invalid user data returned from test-github-provider" in res.data.decode('utf-8')

            mock_get_username.assert_called_once_with("unittestaccesstoken")
            mock_update_repositories.assert_not_called()

            # Ensure session variables have not been set
            with client.session_transaction() as session:
                assert session == {}

    def test_call(self, client, mock_models, test_github_provider_source):
        with unittest.mock.patch('terrareg.config.Config.SECRET_KEY', 'abcdefg'), \
                unittest.mock.patch('terrareg.audit.AuditEvent.create_audit_event') as mock_create_audit_event, \
                unittest.mock.patch('terrareg.models.Session.cleanup_old_sessions', create=True) as cleanup_old_sessions_mock, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.get_user_access_token', unittest.mock.MagicMock(return_value="unittestaccesstoken")) as mock_get_access_token, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.get_username', unittest.mock.MagicMock(return_value='unittestgithubusername')) as mock_get_username, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.get_user_organisations', unittest.mock.MagicMock(
                    return_value={'unittestgithubusername': NamespaceType.GITHUB_USER, 'testorg': NamespaceType.GITHUB_ORGANISATION}
                )) as mock_get_user_organisations, \
                unittest.mock.patch('terrareg.provider_source.github.GithubProviderSource.update_repositories', unittest.mock.MagicMock()) as mock_update_repositories:
            # Update real app secret key
            self.SERVER._app.secret_key = 'abcdefg'

            res = client.get(f"/test-github-provider/callback?code=abc")

            assert res.status_code == 302
            assert res.headers.get("Location") == "/"

            mock_get_username.assert_called_once_with("unittestaccesstoken")
            mock_get_user_organisations.assert_called_once_with("unittestaccesstoken")
            mock_update_repositories.assert_called_once_with('unittestaccesstoken')

            with client.session_transaction() as session:
                assert session['is_admin_authenticated'] == True
                assert session['authentication_type'] == 6
                assert session['github_username'] == 'unittestgithubusername'
                assert session['organisations'] == {'testorg': 'GithubOrganisation', 'unittestgithubusername': 'GithubUser'}

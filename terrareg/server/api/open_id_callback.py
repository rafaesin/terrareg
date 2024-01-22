
import datetime
import urllib.parse

from flask import request, make_response, render_template, session, redirect

from terrareg.server.error_catching_resource import ErrorCatchingResource
import terrareg.openid_connect
import terrareg.config
import terrareg.models
import terrareg.audit
import terrareg.audit_action
import terrareg.auth
import terrareg.utils


class ApiOpenIdCallback(ErrorCatchingResource):
    """Interface to handle callback from authorization flow from OpenID connect"""

    def _get(self):
        """Handle response from OpenID callback"""
        # If session state has not been set, return 
        state = session.get('openid_connect_state')
        if not state:
            return {}, 400

        # Adapt current URL to URL manipulated over PUBLIC_URL to avoid
        # issues with reverse proxies forwarding to Terrareg serving on HTTP port
        parsed_url = urllib.parse.urlparse(request.url)
        protocol, domain, port = terrareg.utils.get_public_url_details()
        parsed_url = parsed_url._replace(scheme=protocol, netloc=f'{domain}:{port}')

        # Fetch access token
        try:
            access_token = terrareg.openid_connect.OpenidConnect.fetch_access_token(uri=parsed_url.geturl(), valid_state=state)
            if access_token is None:
                raise Exception('Error getting access token')
        except Exception as exc:
            # In dev, re-raise exception
            if terrareg.config.Config().DEBUG:
                raise

            res = make_response(render_template(
                'error.html',
                error_title='Login error',
                error_description='Invalid response from SSO'
            ))
            res.headers['Content-Type'] = 'text/html'
            return res

        user_info = terrareg.openid_connect.OpenidConnect.get_user_info(access_token=access_token['access_token'])

        session_obj = self.create_session()
        if not isinstance(session_obj, terrareg.models.Session):
            res = make_response(render_template(
                'error.html',
                error_title='Login error',
                error_description='Sessions are not available'
            ))
            res.headers['Content-Type'] = 'text/html'
            return res

        session['openid_connect_id_token'] = access_token['id_token']
        session['openid_connect_access_token'] = access_token['access_token']
        session['openid_groups'] = user_info.get('groups', [])
        session['openid_username'] = user_info.get('preferred_username', user_info.get("email", None))
        session['is_admin_authenticated'] = True
        session['authentication_type'] = terrareg.auth.AuthenticationType.SESSION_OPENID_CONNECT.value

        if terrareg.config.Config().OPENID_CONNECT_DEBUG:
            print(f"""
Successul OpenID connect authentication response:
User info:
{user_info}
User groups:
{session['openid_groups']}
Username:
{session['openid_username']}
""")

        # Manually calculate expires at, to avoid time-zone issues
        session['openid_connect_expires_at'] = datetime.datetime.now().timestamp() + access_token['expires_in']
        session.modified = True

        # Create audit event
        terrareg.audit.AuditEvent.create_audit_event(
            action=terrareg.audit_action.AuditAction.USER_LOGIN,
            object_type=None, object_id=None,
            old_value=None, new_value=None
        )

        # Redirect to homepage
        return redirect('/')

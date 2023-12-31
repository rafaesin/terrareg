
from functools import wraps
import types

from flask import abort

import terrareg.auth


def auth_wrapper(auth_check_method, *wrapper_args, request_kwarg_map={}, kwarg_values={}, **wrapper_kwargs):
    """
    Wrapper to custom authentication decorators.
    An authentication checking method should be passed with args/kwargs, which will be
    used to check authentication and authorisation.
    """
    def decorator_wrapper(func):
        """Check user is authenticated as admin and either call function or return 401, if not."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtain authentication method of the current user
            auth_method = terrareg.auth.AuthFactory().get_current_auth_method()

            # Obtain all arguments passed to the wrapper and create a map
            # of arguments to the request
            auth_kwargs = wrapper_kwargs.copy()
            for request_kwarg in request_kwarg_map:
                if request_kwarg in kwargs:
                    auth_kwargs[request_kwarg_map[request_kwarg]] = kwargs[request_kwarg]

            # Iterate through kwarg values map and add these directly to the call
            for auth_kwarg_itx in kwarg_values:
                # If value is a lambda, execute it to generate the value
                if isinstance(kwarg_values[auth_kwarg_itx], types.LambdaType):
                    auth_kwargs[auth_kwarg_itx] = kwarg_values[auth_kwarg_itx](**kwargs)
                else:
                    auth_kwargs[auth_kwarg_itx] = kwarg_values[auth_kwarg_itx]

            # Call authentication method.
            if (status := getattr(auth_method, auth_check_method)(*wrapper_args, **auth_kwargs)) is False:
                # Return 403 and 401 based on whether user is authenticated
                if auth_method.is_authenticated():
                    abort(403)
                else:
                    abort(401)

            # Otherwise, if the authentication was successful, call the wrapped method
            elif status is True:
                return func(*args, **kwargs)

            # If status is None, treat as not found
            elif status is None:
                abort(404)
            else:
                raise Exception('Invalid response from auth check method')
        return wrapper
    return decorator_wrapper
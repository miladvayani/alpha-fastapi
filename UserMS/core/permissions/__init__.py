"""
- For add new permission:
    Add your specific permission class in the service.py file add inherit it from the IPermission interface.

- For use permission:
    Create new object of PermissionChecker in checker.py and pass the new object of permission service to class __init__ 
    then call check function for fastapi depends in router.
    
``Example``:

.. code-block:: python

    dependencies = [Depends(PermissionChecker(UserAuthenticated()).check)]

"""

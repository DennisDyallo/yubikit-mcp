.. OATH_Commands.rst

.. _oath-commands-label:

===============
OATH Commands
===============

Acronyms and their definitions are listed at the bottom of the :ref:`base-commands-label` page.


ykman oath [OPTIONS] COMMAND [ARGS]...
======================================

Manage OATH application.


Examples
--------

* Generate codes for accounts starting with ``yubi``:

  .. code-block::

     $ ykman oath accounts code yubi

* Add an account that requires touch, the secret key ``f5up4ub3dw``, and the name ``yubico``:

  .. code-block::

     $ ykman oath accounts add yubico f5up4ub3dw --touch

* Set a password for the OATH application:

  .. code-block::

     $ ykman oath access change-password


Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+


Commands
--------

.. table::

   +----------------+----------------------------------------------------------+
   | Command        | Description                                              |
   +================+==========================================================+
   | ``access``     | Manage password protection for OATH.                     |
   +----------------+----------------------------------------------------------+
   | ``accounts``   | Manage and use OATH accounts.                            |
   +----------------+----------------------------------------------------------+
   | ``info``       | Display general status of OATH application.              |
   +----------------+----------------------------------------------------------+
   | ``reset``      | Reset all OATH data.                                     |
   +----------------+----------------------------------------------------------+



ykman oath access [OPTIONS] COMMAND [ARGS]...
=============================================

Manage password protection for OATH.


Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+


Commands
--------

.. table::

   +----------------+----------------------------------------------------------+
   | Command        | Description                                              |
   +================+==========================================================+
   | ``change``     | Change the password used to protect OATH accounts.       |
   +----------------+----------------------------------------------------------+
   | ``forget``     | Remove a stored password from this computer.             |
   +----------------+----------------------------------------------------------+
   | ``remember``   || Store YubiKeys passwords on this computer to avoid      |
   |                || having to enter it on each use.                         |
   +----------------+----------------------------------------------------------+



ykman oath access change [OPTIONS]
==================================

Change the password used to protect OATH accounts. Allows you to set or change a password that is required to access the OATH accounts stored on the YubiKey.


Options
-------

.. table::

   +-----------------------------+---------------------------------------------+
   | Option                      | Description                                 |
   +=============================+=============================================+
   | ``-h, --help``              | Show this message and exit.                 |
   +-----------------------------+---------------------------------------------+
   | ``-c, --clear``             | Clear the current password.                 |
   +-----------------------------+---------------------------------------------+
   | ``-n, --new-password TEXT`` | Provide a new password as an argument.      |
   +-----------------------------+---------------------------------------------+
   | ``-p, --password TEXT``     | Provide a password to unlock the YubiKey.   |
   +-----------------------------+---------------------------------------------+
   | ``-r, --remember``          | Remember the password on this machine.      |
   +-----------------------------+---------------------------------------------+



ykman oath access forget [OPTIONS]
==================================

Remove a stored password from this computer.


Options
--------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+
   | ``-a, --all``  | Remove all stored passwords.                             |
   +----------------+----------------------------------------------------------+



ykman oath access remember [OPTIONS]
====================================

Store the YubiKey password on this computer to avoid entering it on each use.


Options
-------

.. table::

   +-------------------------+-------------------------------------------------+
   | Option                  | Description                                     |
   +=========================+=================================================+
   | ``-h, --help``          | Show this message and exit.                     |
   +-------------------------+-------------------------------------------------+
   | ``-p, --password TEXT`` | Provide a password to unlock the YubiKey.       |
   +-------------------------+-------------------------------------------------+


ykman oath accounts [OPTIONS] COMMAND [ARGS]...
================================================

Manage and use OATH accounts.


Options
-------

.. table::

   +-------------------------+-------------------------------------------------+
   | Option                  | Description                                     |
   +=========================+=================================================+
   | ``-h, --help``          | Show this message and exit.                     |
   +-------------------------+-------------------------------------------------+


Commands
--------

.. table::

   +-------------+-------------------------------------------------------------+
   | Command     | Description                                                 |
   +=============+=============================================================+
   | ``add``     | Add a new account.                                          |
   +-------------+-------------------------------------------------------------+
   | ``code``    | Generate codes.                                             |
   +-------------+-------------------------------------------------------------+
   | ``delete``  | Delete an account.                                          |
   +-------------+-------------------------------------------------------------+
   | ``list``    | List all accounts.                                          |
   +-------------+-------------------------------------------------------------+
   | ``rename``  | Rename an account. Requires YubiKey 5.3 or later.           |
   +-------------+-------------------------------------------------------------+
   | ``uri``     | Add a new account from an ``otpauth://`` URI.               |
   +-------------+-------------------------------------------------------------+


ykman oath accounts add [OPTIONS] NAME [SECRET]
================================================

Add a new OATH account to the YubiKey.


Arguments
----------

.. table::

   +------------+--------------------------------------------------------------+
   | Argument   | Description                                                  |
   +============+==============================================================+
   | ``NAME``   || Human readable name for this account, such as username or   |
   |            || email address.                                              |
   +------------+--------------------------------------------------------------+
   | ``SECRET`` || Optional. Base32-encoded secret/key value provided by       |
   |            || the server.                                                 |
   +------------+--------------------------------------------------------------+


Options
-------

.. table::

   +---------------------------------+-----------------------------------------+
   | Option                          | Description                             |
   +=================================+=========================================+
   | ``-h, --help``                  | Show this message and exit.             |
   +---------------------------------+-----------------------------------------+
   || ``-a, --algorithm``            || Algorithm to use for code              |
   || ``[SHA1|SHA256|SHA512]``       || generation. Default: SHA1              |
   +---------------------------------+-----------------------------------------+
   | ``-c, --counter INTEGER``       | Initial counter value for HOTP accounts.|
   +---------------------------------+-----------------------------------------+
   | ``-d, --digits [6|7|8]``        || Number of digits in generated code.    |
   |                                 || Default: 6                             |
   +---------------------------------+-----------------------------------------+
   | ``-f, --force``                 | Confirm the action without prompting.   |
   +---------------------------------+-----------------------------------------+
   | ``-i, --issuer TEXT``           | Optional. Issuer of the account.        |
   +---------------------------------+-----------------------------------------+
   | ``o, --oath-type [HOTP|TOTP]``  || Time-based (TOTP) or counter-based     |
   |                                 || (HOTP) account. Default: TOTP          |
   +---------------------------------+-----------------------------------------+
   | ``-p, --password TEXT``         || Provide a password to unlock the       |
   |                                 || YubiKey.                               |
   +---------------------------------+-----------------------------------------+
   | ``-P, --period INTEGER``        || Number of seconds a TOTP code is       |
   |                                 || valid.  Default: 30                    |
   +---------------------------------+-----------------------------------------+
   | ``-r, --remember``              | Remember the password on this machine.  |
   +---------------------------------+-----------------------------------------+
   | ``-t, --touch``                 || Require touch on YubiKey to generate   |
   |                                 || code.                                  |
   +---------------------------------+-----------------------------------------+



ykman oath accounts code [OPTIONS] [QUERY]
==========================================

Generate codes from OATH accounts stored on the YubiKey. Accounts of type HOTP or those that require touch, also require a single match to be triggered.


Arguments
----------

.. table::

   +-----------+---------------------------------------------------------------+
   | Argument  | Description                                                   |
   +===========+===============================================================+
   | ``QUERY`` | Provide a query string to match one or more specific accounts.|
   +-----------+---------------------------------------------------------------+


Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+
   | ``-H, --show-hidden``     | Include hidden accounts.                      |
   +---------------------------+-----------------------------------------------+
   | ``-p, --password TEXT``   | Provide a password to unlock the YubiKey.     |
   +---------------------------+-----------------------------------------------+
   | ``-r, --remember``        | Remember the password on this machine.        |
   +---------------------------+-----------------------------------------------+
   | ``-s, --single``          || Ensure only a single match, and output only  |
   |                           || the code.                                    |
   +---------------------------+-----------------------------------------------+



ykman oath accounts delete [OPTIONS] QUERY
==========================================

Delete an account from the YubiKey. 


Arguments
-----------

.. table::

   +-----------+---------------------------------------------------------------+
   | Argument  | Description                                                   |
   +===========+===============================================================+
   | ``QUERY`` || Provide a query string to match a single account, as shown   |
   |           || in :ref:`ykman oath accounts list <ac-list>`.                |
   +-----------+---------------------------------------------------------------+


Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+
   | ``-f, --force``           | Confirm deletion without prompting            |
   +---------------------------+-----------------------------------------------+
   | ``-p, --password TEXT``   | Provide a password to unlock the YubiKey.     |
   +---------------------------+-----------------------------------------------+
   | ``-r, --remember``        | Remember the password on this machine.        |
   +---------------------------+-----------------------------------------------+


.. _ac-list:

ykman oath accounts list [OPTIONS]
==================================

List all accounts stored on the YubiKey.


Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+
   | ``-H, --show-hidden``     | Include hidden accounts.                      |
   +---------------------------+-----------------------------------------------+
   | ``-o, --oath-type``       | Display the OATH type.                        |
   +---------------------------+-----------------------------------------------+
   | ``-p, --password TEXT``   | Provide a password to unlock the YubiKey.     |
   +---------------------------+-----------------------------------------------+
   | ``-P, --period``          | Display the period.                           |
   +---------------------------+-----------------------------------------------+
   | ``-r, --remember``        | Remember the password on this machine.        |
   +---------------------------+-----------------------------------------------+


ykman oath accounts rename [OPTIONS] QUERY NAME
================================================

Rename an account. Requires YubiKey 5.3 or later.


Arguments
----------

.. table::

   +-----------+---------------------------------------------------------------+
   | Argument  | Description                                                   |
   +===========+===============================================================+
   | ``QUERY`` || A query to match a single account, as shown in               |
   |           || :ref:`ykman oath accounts list <ac-list>`.                   |
   +-----------+---------------------------------------------------------------+
   | ``NAME``  || The name of the account. Use format ``<issuer>:<name>``      |
   |           || to specify the issuer.                                       |
   +-----------+---------------------------------------------------------------+


Options
--------

.. table::

   +-------------------------+-------------------------------------------------+
   | Option                  | Description                                     |
   +=========================+=================================================+
   | ``-h, --help``          | Show this message and exit.                     |
   +-------------------------+-------------------------------------------------+
   | ``-f, --force``         | Confirm rename without prompting.               |
   +-------------------------+-------------------------------------------------+
   | ``-p, --password TEXT`` | Provide a password to unlock the YubiKey.       |
   +-------------------------+-------------------------------------------------+
   | ``-r, --remember``      | Remember the password on this machine.          |
   +-------------------------+-------------------------------------------------+


ykman oath accounts uri [OPTIONS] URI
=====================================

Add a new account from an ``otpauth://`` URI. Use a URI to add a new account to the YubiKey.


Arguments
----------

.. table::

   +-----------+---------------------------------------------------------------+
   | Argument  | Description                                                   |
   +===========+===============================================================+
   | ``URI``   | Specify URI path for account.                                 |
   +-----------+---------------------------------------------------------------+


Options
-------

.. table::

   +--------------------------+------------------------------------------------+
   | Option                   | Description                                    |
   +==========================+================================================+
   | ``-h, --help``           | Show this message and exit.                    |
   +--------------------------+------------------------------------------------+
   | ``-f, --force``          | Confirm the action without prompting.          |
   +--------------------------+------------------------------------------------+
   | ``-p, --password TEXT``  | Provide a password to unlock the YubiKey.      |
   +--------------------------+------------------------------------------------+
   | ``-r, --remember``       | Remember the password on this machine.         |
   +--------------------------+------------------------------------------------+
   | ``-t, --touch``          | Require touch on YubiKey to generate code.     |
   +--------------------------+------------------------------------------------+



ykman oath info [OPTIONS]
=========================

Display status of OATH application.


Options
-------

.. table::

   +--------------------------+------------------------------------------------+
   | Option                   | Description                                    |
   +==========================+================================================+
   | ``-h, --help``           | Show this message and exit.                    |
   +--------------------------+------------------------------------------------+



ykman oath reset [OPTIONS]
==========================

Reset all OATH data. This action deletes all accounts and restores factory settings for the OATH application on the YubiKey.


Options
-------

.. table::

   +--------------------------+------------------------------------------------+
   | Option                   | Description                                    |
   +==========================+================================================+
   | ``-h, --help``           | Show this message and exit.                    |
   +--------------------------+------------------------------------------------+
   | ``-f, --force``          | Confirm the action without prompting.          |
   +--------------------------+------------------------------------------------+

----

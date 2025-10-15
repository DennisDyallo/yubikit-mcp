.. HSMauth_Commands.rst


.. _yubihsm-commands-label:

================
HSMauth Commands
================

For a description of YubiHSM Auth, see the *YubiKey 5 Series Technical Manual*, `Protocols and Applications > YubiHSM Auth <https://docs.yubico.com/hardware/yubikey/yk-tech-manual/yk5-apps.html#yubihsm-auth>`_ chapter. 

This chapter describes the ``ykman hsmauth`` commands, not the ``yubishm`` commands. 

For YubiHSM installation, configuration, and ``yubihsm`` commands see the `YubiHSM 2 User Guide <https://docs.yubico.com/hardware/yubihsm-2/hsm-2-user-guide/index.html>`_.


Enable or Disable YubiHSM Auth on a YubiKey
============================================

This section includes the expected output and testing methods.

YubiHSM Auth is available as of firmware version 5.4.X and is disabled by default.


**Enable** YubiHSM Auth by running:

.. code-block::

   ykman config usb --enable HSMAUTH
   YubiHSM Auth successfully enabled.

**Test enablement** by connecting to the YubiHSM with YubiHSM-Shell:

.. code-block::

   yubihsm> session ykopen 1 "default key" "my secret"
   Session authenticated to YubiHSM2.

**Disable** YubiHSM Auth by running:

.. code-block::

   ykman config usb --disable HSMAUTH
   YubiHSM Auth successfully disabled.

**Test disablement** by connecting to the YubiHSM with YubiHSM-Shell:

.. code-block::

   yubihsm> session ykopen 1 "default key" "my secret"
   No access to the YubiKey application YubiHSM Auth.



ykman hsmauth [OPTIONS] COMMAND [ARGS]...
=========================================

Manage the YubiHSM Auth application.

Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+


Commands
---------

.. table::

   +------------------+--------------------------------------------------------+
   | Command          | Description                                            |
   +==================+========================================================+
   | ``access``       | Manage Management Key for YubiHSM Auth.                |
   +------------------+--------------------------------------------------------+
   | ``credentials``  | Manage YubiHSM Auth credentials.                       |
   +------------------+--------------------------------------------------------+
   | ``info``         | Display general status of the YubiHSM Auth application.|
   +------------------+--------------------------------------------------------+
   | ``reset``        | Reset all YubiHSM Auth data.                           |
   +------------------+--------------------------------------------------------+
   




ykman hsmauth access [OPTIONS] COMMAND [ARGS]...
=================================================

Manage the management key for YubiHSM Auth.

Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+


Commands
---------

.. table::

   +--------------------------------+------------------------------------------+
   | Command                        | Description                              |
   +================================+==========================================+
   | ``change-management-password`` | Change the management password.          |
   +--------------------------------+------------------------------------------+



ykman hsmauth access change-management-password
================================================

Change the management password.

Allows you to change the management password. This is required to add and delete YubiHSM Auth credentials stored on the YubiKey.

``ykman hsmauth access change-management-password`` supersedes ``ykman hsmauth access change-management-key``, in ykman version 5.5.

Options
-------

.. table::

   +-----------------------------------+------------------------------------------+
   | Option                            | Description                              |
   +===================================+==========================================+
   | ``-h, --help``                    | Show this message and exit.              |
   +-----------------------------------+------------------------------------------+
   || ``-m, --management-password``    || Current management password.            |
   ||         ``TEXT``                 || Default: b'\x00\x00\x00\x00\x00\x00\x00\|
   |                                   || x00\x00\x00\x00\x00\x00\x00\x00\x00'    |
   +-----------------------------------+------------------------------------------+
   || ``-n, --new-management-password``| Specify the new management password.     |
   ||         ``TEXT``                 |                                          |
   +-----------------------------------+------------------------------------------+
   


ykman hsmauth credentials [OPTIONS] COMMAND [ARGS]...
=====================================================

Manage YubiHSM Auth credentials.

Options
-------

.. table::

   +-----------------------------+---------------------------------------------+
   | Option                      | Description                                 |
   +=============================+=============================================+
   | ``-h, --help``              | Show this message and exit.                 |
   +-----------------------------+---------------------------------------------+


Commands
---------

.. table::

   +-------------------+-------------------------------------------------------+
   | Command           | Description                                           |
   +===================+=======================================================+
   | ``delete``        | Delete a credential.                                  |
   +-------------------+-------------------------------------------------------+
   | ``derive``        | Import a symmetric credential derived from a password.|
   +-------------------+-------------------------------------------------------+
   | ``export``        | Export the public key corresponding to an asymmetric  |
   |                   | credential.                                           |
   +-------------------+-------------------------------------------------------+
   | ``generate``      | Generate an asymmetric credential.                    |
   +-------------------+-------------------------------------------------------+
   | ``import``        | Import an asymmetric credential.                      |
   +-------------------+-------------------------------------------------------+
   | ``list``          | List all credentials.                                 |
   +-------------------+-------------------------------------------------------+
   | ``symmetric``     | Import a symmetric credential.                        |
   +-------------------+-------------------------------------------------------+


ykman hsmauth credentials delete [OPTIONS] LABEL
=================================================

Delete a credential. This deletes a YubiHSM Auth credential from the YubiKey.

Arguments
----------

.. table::

   +------------------+----------------------------------------------------------+
   | Argument         | Description                                              |
   +==================+==========================================================+
   | ``LABEL``        || A label to match a single credential, as shown in       |
   |                  || ``credential list``.                                    |
   +------------------+----------------------------------------------------------+
   

Options
-------

.. table::

   +---------------------------------+--------------------------------------------+
   | Option                          | Description                                |
   +=================================+============================================+
   | ``-h, --help``                  | Show this message and exit.                |
   +---------------------------------+--------------------------------------------+
   || ``-m, --management-password,`` | The management password.                   |
   || ``--management-key TEXT``      |                                            |
   +---------------------------------+--------------------------------------------+
   | ``-f, --force``                 | Confirm the action without prompting.      |
   +---------------------------------+--------------------------------------------+


ykman hsmauth credentials derive [OPTIONS] LABEL
================================================

Import a symmetric credential derived from a password. This imports a symmetric YubiHSM Auth credential by deriving ENC and MAC keys from a password.

Arguments
----------

.. table::

   +------------------+----------------------------------------------------------+
   | Argument         | Description                                              |
   +==================+==========================================================+
   | ``LABEL``        | A label for the YubiHSM Auth credential.                 |
   +------------------+----------------------------------------------------------+


Options
-------

.. table::

   +--------------------------------+--------------------------------------------+
   | Option                         | Description                                |
   +================================+============================================+
   | ``-h, --help``                 | Show this message and exit.                |
   +--------------------------------+--------------------------------------------+
   || ``-d, --derivation-password`` | Derivation password for ENC and MAC keys.  |
   ||       ``TEXT``                |                                            |
   +--------------------------------+--------------------------------------------+
   || ``-c, --credential-password`` | Password to protect credential.            |
   ||       ``TEXT``                |                                            |
   +--------------------------------+--------------------------------------------+
   || ``-m, --management-password,``| The management password.                   |
   || ``--management-key TEXT``     |                                            |
   +--------------------------------+--------------------------------------------+
   | ``-t, --touch``                || Requires touch on YubiKey to access       |
   |                                || credential.                               |
   +--------------------------------+--------------------------------------------+



ykman hsmauth credentials export [OPTIONS] LABEL PUBLIC-KEY
============================================================

Export the public key corresponding to an asymmetric credential. This exports the long-term public key corresponding to the asymmetric YubiHSM Auth credential stored on the YubiKey.


Arguments
----------

.. table::

   +------------------+------------------------------------------------------------+
   | Argument         | Description                                                |
   +==================+============================================================+
   | ``LABEL``        | A label for the YubiHSM Auth credential.                   |
   +------------------+------------------------------------------------------------+
   | ``PUBLIC-KEY``   || File to write the public key to.                          |
   |                  || Use ``-`` to use ``stdout``.                              |
   +------------------+------------------------------------------------------------+

Options
-------

.. table::

   +--------------------------------+--------------------------------------------+
   | Option                         | Description                                |
   +================================+============================================+
   | ``-h, --help``                 | Show this message and exit.                |
   +--------------------------------+--------------------------------------------+
   | ``-F, --format [PEM|DER]``     | Encoding format.  Default: PEM             |
   +--------------------------------+--------------------------------------------+



ykman hsmauth credentials generate [OPTIONS] LABEL
==================================================

Generate an asymmetric credential. This generates an asymmetric YubiHSM Auth credential (private key) on the YubiKey.

Arguments
----------

.. table::

   +------------------+----------------------------------------------------------+
   | Argument         | Description                                              |
   +==================+==========================================================+
   | ``LABEL``        | A label for the YubiHSM Auth credential.                 |
   +------------------+----------------------------------------------------------+


Options
-------

.. table::

   +------------------------------------+--------------------------------------+
   | Option                             | Description                          |
   +====================================+======================================+
   | ``-h, --help``                     | Show this message and exit.          |
   +------------------------------------+--------------------------------------+
   | ``-c, --credential-password TEXT`` | Password to protect credential.      |
   +------------------------------------+--------------------------------------+
   || ``-m, --management-password,``    | The management password.             |
   || ``--management-key TEXT``         |                                      |
   +------------------------------------+--------------------------------------+
   | ``-t, --touch``                    | Requires touch on YubiKey to access  |
   |                                    | credential.                          |
   +------------------------------------+--------------------------------------+



ykman hsmauth credentials import [OPTIONS] LABEL PRIVATE-KEY
=============================================================

Import an asymmetric credential. This imports a private key as an asymmetric YubiHSM Auth credential to the YubiKey.


Arguments
----------

.. table::

   +------------------+----------------------------------------------------------+
   | Argument         | Description                                              |
   +==================+==========================================================+
   | ``LABEL``        | A label for the YubiHSM Auth credential.                 |
   +------------------+----------------------------------------------------------+
   | ``PRIVATE-KEY``  || File containing the private key.                        |
   |                  || Use ``-`` to use ``stdin``.                             |
   +------------------+----------------------------------------------------------+


Options
-------

.. table::

   +------------------------------------+----------------------------------------+
   | Option                             | Description                            |
   +====================================+========================================+
   | ``-h, --help``                     | Show this message and exit.            |
   +------------------------------------+----------------------------------------+
   | ``-c, --credential-password TEXT`` | Password to protect credential.        |
   +------------------------------------+----------------------------------------+
   || ``-m, --management-password,``    | The management password.               |
   || ``--management-key TEXT``         |                                        |
   +------------------------------------+----------------------------------------+
   | ``-p, --password TEXT``            || Password used to decrypt the private  |
   |                                    || key.                                  |
   +------------------------------------+----------------------------------------+
   | ``-t, --touch``                    || Requires touch on YubiKey to access   |
   |                                    || credential.                           |
   +------------------------------------+----------------------------------------+


ykman hsmauth credentials list [OPTIONS]
========================================

List all credentials stored on the YubiKey.

Options
-------

.. table::

   +--------------------------------+--------------------------------------------+
   | Option                         | Description                                |
   +================================+============================================+
   | ``-h, --help``                 | Show this message and exit.                |
   +--------------------------------+--------------------------------------------+


ykman hsmauth credentials symmetric [OPTIONS] LABEL
===================================================

Import a symmetric credential. This imports an ENC and MAC key as a symmetric YubiHSM Auth credential on the YubiKey.

Arguments
----------

.. table::

   +------------------+----------------------------------------------------------+
   | Argument         | Description                                              |
   +==================+==========================================================+
   | ``LABEL``        | A label for the YubiHSM Auth credential.                 |
   +------------------+----------------------------------------------------------+


Options
-------

.. table::

   +-------------------------------------+---------------------------------------+
   | Option                              | Description                           |
   +=====================================+=======================================+
   | ``-h, --help``                      | Show this message and exit.           |
   +-------------------------------------+---------------------------------------+
   | ``-c, --credential-password TEXT``  | Password to protect credential.       |
   +-------------------------------------+---------------------------------------+
   | ``-E, --enc-key TEXT``              | The ENC key.                          |
   +-------------------------------------+---------------------------------------+
   | ``-g, --generate``                  || Generate a random encryption and MAC |
   |                                     || key.                                 |
   +-------------------------------------+---------------------------------------+
   || ``-m, --management-password,``     | The management password.              |
   || ``--management-key TEXT``          |                                       |
   +-------------------------------------+---------------------------------------+
   | ``-M, --mac-key TEXT``              | The MAC key.                          |
   +-------------------------------------+---------------------------------------+
   | ``-t, --touch``                     | Requires touch on YubiKey to access   |
   |                                     | credential.                           |
   +-------------------------------------+---------------------------------------+
  
  
  
ykman hsmauth info [OPTIONS]
=============================

Display general status of the YubiHSM Auth application.

Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+


ykman hsmauth reset [OPTIONS]
=============================

Reset all YubiHSM Auth data.

This action wipes all data and restores factory setting for the YubiHSM Auth application on the YubiKey.

Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+
   | ``-f, --force``| Confirm the action without prompting.                    |
   +----------------+----------------------------------------------------------+
 
 
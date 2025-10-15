.. OTP_Commands.rst

.. _opt-commands-label:

==================
OTP Commands
==================

Acronyms and their definitions are listed at the bottom of the :ref:`base-commands-label` page.


ykman otp [OPTIONS] COMMAND [ARGS]...
======================================

Manage YubiOTP application. 

The YubiKey provides two keyboard-based slots that can each be configured with a credential. Several credential types are supported. 

A slot configuration can be write-protected with an access code. This prevents the configuration from being overwritten without the access code being provided.

.. Note:: Mode-switching the YubiKey is not possible when a slot is configured with an access code.

To provide an access code to commands which require it, use the ``--access-code`` option. This option must be given directly after the ``otp`` command and before any sub-command.


Examples
--------

**Swap the configurations** between the two slots:

.. code-block::

   $ ykman otp swap

Program a **random challenge-response** credential to slot 2:

.. code-block::

   $ ykman otp chalresp --generate 2

Program a Yubico **OTP credential** to slot 1, using the serial as public ID:

.. code-block::

   $ ykman otp yubiotp 1 --serial-public-id

Program a random 38 character **static password** to slot 2:

.. code-block::

   $ ykman otp static --generate 2 --length 38

**Remove** a currently set access code from slot 2:

.. code-block::

   $ ykman otp --access-code 0123456789ab settings 2 --delete-access-code

Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+
   | ``--access-code HEX`` || A 6-byte access code. Enter ``-`` to prompt for  |
   |                       || input.                                           |
   +-----------------------+---------------------------------------------------+


Commands
--------

.. table::

   +---------------+-----------------------------------------------------------+
   | Command       | Description                                               |
   +===============+===========================================================+
   | ``calculate`` | Perform a challenge-response operation.                   |
   +---------------+-----------------------------------------------------------+
   | ``chalresp``  | Program a challenge-response credential.                  |
   +---------------+-----------------------------------------------------------+
   | ``delete``    | Deletes the configuration stored in a slot.               |
   +---------------+-----------------------------------------------------------+
   | ``hotp``      | Program an HMAC-SHA1 OATH-HOTP credential.                |
   +---------------+-----------------------------------------------------------+
   | ``info``      | Display general status of the YubiKey OTP slots.          |
   +---------------+-----------------------------------------------------------+
   | ``ndef``      | Configure a slot to be used over NDEF (NFC).              |
   +---------------+-----------------------------------------------------------+
   | ``settings``  | Update the settings for a slot.                           |
   +---------------+-----------------------------------------------------------+
   | ``static``    | Configure a static password.                              |
   +---------------+-----------------------------------------------------------+
   | ``swap``      | Swaps the two slot configurations.                        |
   +---------------+-----------------------------------------------------------+
   | ``yubiotp``   | Program a Yubico OTP credential.                          |
   +---------------+-----------------------------------------------------------+


ykman otp calculate [OPTIONS] {1|2} [CHALLENGE]
================================================

Perform a challenge-response operation to a YubiKey slot. Send a challenge (in hex) to a YubiKey slot with a challenge-response credential and read the response. Supports output as an OATH-TOTP code.

Arguments
----------

.. table::

   +----------------+----------------------------------------------------------+
   | Argument       | Description                                              |
   +================+==========================================================+
   | ``CHALLENGE``  || Challenge default is hex. For base32, use ``--totp``    |
   |                || setting.                                                |
   +----------------+----------------------------------------------------------+
   | ``1, 2``       | Select the slot for the action.                          |
   +----------------+----------------------------------------------------------+


Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+
   | ``-d, --digits [6|8]``|| Number of digits in generated TOTP code. Ignored |
   |                       || unless ``--totp`` is set.  Default: ``6``        |
   +-----------------------+---------------------------------------------------+
   | ``-T, --totp``        || Generate a TOTP code, use the current time if    |
   |                       || challenge is omitted.                            |
   +-----------------------+---------------------------------------------------+


ykman otp chalresp [OPTIONS] {1|2} [KEY]
==========================================

Program a challenge-response credential to a YubiKey slot 1 or 2.


Arguments
----------

.. table::

   +----------+----------------------------------------------------------------+
   | Argument | Description                                                    |
   +==========+================================================================+
   | ``KEY``  || Provide key in hex. For base32, use ``--totp``  setting.      |
   |          || If ``KEY`` is not specified, an interactive prompt asks       |
   |          || for it.                                                       |
   +----------+----------------------------------------------------------------+
   | ``1, 2`` | Select the slot for the action.                                |
   +----------+----------------------------------------------------------------+


Options
-------

.. table::

   +--------------------+------------------------------------------------------+
   | Option             | Description                                          |
   +====================+======================================================+
   | ``-h, --help``     | Show this message and exit.                          |
   +--------------------+------------------------------------------------------+
   | ``-f, --force``    | Confirm the action without prompting.                |
   +--------------------+------------------------------------------------------+
   | ``-g, --generate`` || Generate a random secret key. Cannot be used with   |
   |                    || ``KEY`` argument.                                   |
   +--------------------+------------------------------------------------------+
   | ``-t, --touch``    || Require touch on the YubiKey to generate a response.|
   +--------------------+------------------------------------------------------+
   | ``-T, --totp``     || Use a base32 encoded key for TOTP credentials.      |
   |                    || Optionally, can be padded.                          |
   +--------------------+------------------------------------------------------+



ykman otp delete [OPTIONS] {1|2}
=================================

Deletes the configuration for the YubiKey in the specified slot, 1 or 2. 

Arguments
----------

.. table::

   +----------+----------------------------------------------------------------+
   | Argument | Description                                                    |
   +==========+================================================================+
   | ``1, 2`` | Select the slot for the action.                                |
   +----------+----------------------------------------------------------------+


Options
-------

.. table::

   +--------------------+------------------------------------------------------+
   | Option             | Description                                          |
   +====================+======================================================+
   | ``-h, --help``     | Show this message and exit.                          |
   +--------------------+------------------------------------------------------+
   | ``-f, --force``    | Confirm the action without prompting.                |
   +--------------------+------------------------------------------------------+



ykman otp hotp [OPTIONS] {1|2} [KEY]
=====================================

Program an HMAC-SHA1 OATH-HOTP credential for YubiKey in slot 1 or 2. 

The YubiKey can be configured to output an OATH Token Identifier as a prefix to the OTP itself, which consists of OMP+TT+MUI. Using the ``--identifier`` option to specify: 

* OMP+TT as 4 characters
* MUI as 8 characters
* full OMP+TT+MUI as 12 characters. 

If ``--identifier`` is omitted, the default values are:

* OMP+TT - ``ubhe``
* MUI - the YubiKey serial number


Arguments
----------

.. table::

   +------------+--------------------------------------------------------------+
   | Argument   | Description                                                  |
   +============+==============================================================+
   | ``KEY``    || A key given in hex.                                         |
   |            || If ``KEY`` is not specified, an interactive prompt asks     |
   |            || for it.                                                     |
   +------------+--------------------------------------------------------------+
   | ``1, 2``   | Select the slot for the action.                              |
   +------------+--------------------------------------------------------------+


Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+
   | ``-d, --digits [6|8]``    || Number of digits in generated code.          |
   |                           || Default: ``6``                               |
   +---------------------------+-----------------------------------------------+
   | ``-c, --counter INTEGER`` | Initial counter value.                        |
   +---------------------------+-----------------------------------------------+
   | ``-f, --force``           | Confirm the action without prompting.         |
   +---------------------------+-----------------------------------------------+
   | ``-i, --identifier TEXT`` | Token identifier.                             |
   +---------------------------+-----------------------------------------------+
   | ``--no-enter``            || Do not send an **Enter** keystroke after     |
   |                           || outputting the code.                         |
   +---------------------------+-----------------------------------------------+
   


ykman otp info [OPTIONS]
=========================

Display general status of YubiKey OPT slots.


Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+


ykman otp ndef [OPTIONS] {1|2}
===============================

Configure slot 1 or 2 to be used over NDEF (NFC). 

If ``--prefix`` is not specified, default values are used, based on type:

* URI - "https://my.yubico.com/yk/#"
* TEXT - an empty string

Arguments
----------

.. table::

   +----------+----------------------------------------------------------------+
   | Argument | Description                                                    |
   +==========+================================================================+
   | ``1, 2`` | Select the slot for the action.                                |
   +----------+----------------------------------------------------------------+


Options
-------

.. table::

   +--------------------------------+------------------------------------------+
   | Option                         | Description                              |
   +================================+==========================================+
   | ``-h, --help``                 | Show this message and exit.              |
   +--------------------------------+------------------------------------------+
   | ``-p, --prefix TEXT``          || Added before the NDEF payload.          |
   |                                || Typically a URI.                        |
   +--------------------------------+------------------------------------------+
   | ``-t, --ndef-type [TEXT|URI]`` | NDEF payload type  Default: URI          |
   +--------------------------------+------------------------------------------+



ykman otp settings [OPTIONS] {1|2}
===================================

Update the settings for YubiKey in slot 1 or 2. Change the settings for a slot without changing the stored secret. All settings not specified are written with default values.

Arguments
----------

.. table::

   +----------+----------------------------------------------------------------+
   | Argument | Description                                                    |
   +==========+================================================================+
   | ``1, 2`` | Select the slot for the action.                                |
   +----------+----------------------------------------------------------------+


Options
-------

.. table::

   +-------------------------------+-------------------------------------------+
   | Option                        | Description                               |
   +===============================+===========================================+
   | ``-h, --help``                | Show this message and exit.               |
   +-------------------------------+-------------------------------------------+
   | ``-A, --new-access-code HEX`` || Set a new 6-byte access code for         |
   |                               || the slot.                                |
   |                               || Use ``-`` as value to prompt for input.  |
   +-------------------------------+-------------------------------------------+
   | ``--delete-access-code``      | Remove access code from the slot.         |
   +-------------------------------+-------------------------------------------+
   | ``--enter / --no-enter``      || Send **Enter** keystroke after           |
   |                               || slot output. Default: ``enter``          |
   +-------------------------------+-------------------------------------------+
   | ``-f, --force``               | Confirm the action without prompting.     |
   +-------------------------------+-------------------------------------------+
   | ``-p, --pacing [0|20|40|60]`` || Throttle output speed by adding a delay  |
   |                               || (in ms) between characters emitted.      |
   |                               || Default: ``0``                           |
   +-------------------------------+-------------------------------------------+
   | ``--use-numeric-keypad``      || Use scan codes for numeric keypad when   |
   |                               || sending  digits. Helps with some         |
   |                               || keyboard layouts. Default: ``False``     |
   +-------------------------------+-------------------------------------------+


ykman otp static [OPTIONS] {1|2} [PASSWORD]
============================================

Configure a static password for YubiKey in slot 1 or 2. To avoid problems with different keyboard layouts, the following characters (upper and lower case) are allowed by default:

   ``c b d e f g h i j k l n r t u v``

Use the ``--keyboard-layout`` option to allow more characters based on preferred keyboard layout.


Arguments
----------

.. table::

   +--------------+------------------------------------------------------------+
   | Argument     | Description                                                |
   +==============+============================================================+
   | ``PASSWORD`` | Specify if required.                                       |
   +--------------+------------------------------------------------------------+
   | ``1, 2``     | Select the slot for the action.                            |
   +--------------+------------------------------------------------------------+


Options
-------

.. table::

   +-------------------------------+-------------------------------------------+
   | Option                        | Description                               |
   +===============================+===========================================+
   | ``-h, --help``                | Show this message and exit.               |
   +-------------------------------+-------------------------------------------+
   | ``-f, --force``               | Confirm the action without prompting.     |
   +-------------------------------+-------------------------------------------+
   | ``-g, --generate``            | Generate a random password.               |
   +-------------------------------+-------------------------------------------+
   || ``-k, --keyboard-layout``    || Keyboard layout to use for the static    |
   || ``[MODHEX|US|UK|DE|FR|``     || password. Default: ``MODHEX``            |
   || ``IT|BEPO|NORMAN]``          ||                                          |
   +-------------------------------+-------------------------------------------+
   | ``-l, --length LENGTH``       || Length of generated password.            |
   |                               || Default: 38;1<=x<=38                     |
   +-------------------------------+-------------------------------------------+
   | ``--no-enter``                || Do not send an **Enter** keystroke after |
   |                               || outputting the password.                 |
   +-------------------------------+-------------------------------------------+



ykman otp swap [OPTIONS]
=========================

Swaps the two slot configurations.

Options
-------

.. table::

   +-----------------+---------------------------------------------------------+
   | Option          | Description                                             |
   +=================+=========================================================+
   | ``-h, --help``  |  Show this message and exit.                            |
   +-----------------+---------------------------------------------------------+
   | ``-f, --force`` | Confirm the action without prompting.                   |
   +-----------------+---------------------------------------------------------+



ykman otp yubiotp [OPTIONS] {1|2}
==================================

Program a Yubico OTP credential for YubiKey in slot 1 or 2.


Arguments
----------

.. table::

   +----------+----------------------------------------------------------------+
   | Argument | Description                                                    |
   +==========+================================================================+
   | ``1, 2`` | Select the slot for the action.                                |
   +----------+----------------------------------------------------------------+


Options
-------

.. table::

   +----------------------------------+----------------------------------------+
   | Option                           | Description                            |
   +==================================+========================================+
   | ``-h, --help``                   | Show this message and exit.            |
   +----------------------------------+----------------------------------------+
   | ``-f, --force``                  | Confirm the action without prompting.  |
   +----------------------------------+----------------------------------------+
   | ``-k, --key HEX``                | 16-byte secret key.                    |
   +----------------------------------+----------------------------------------+
   | ``-g, --generate-private-id``    || Generate a random private ID. Cannot  |
   |                                  || be used with  ``--private-id``.       |
   +----------------------------------+----------------------------------------+
   | ``-G, --generate-key``           || Generate a random secret key. Cannot  |
   |                                  || be used with ``--key``.               |
   +----------------------------------+----------------------------------------+
   | ``--no-enter``                   || Do not send an **Enter** keystroke    |
   |                                  || after emitting the OTP.               |
   +----------------------------------+----------------------------------------+
   | ``-O, --config-output FILENAME`` || Output configuration to a file        |
   |                                  || Existing files are appended.          |
   +----------------------------------+----------------------------------------+
   | ``-P, --public-id MODHEX``       || Public identifier prefix.             |
   +----------------------------------+----------------------------------------+ 
   | ``-p, --private-id HEX``         || 6-byte private identifier.            |
   +----------------------------------+----------------------------------------+
   | ``-S, --serial-public-id``       || Use YubiKey serial number as public   |
   |                                  || ID. Cannot be used with               |
   |                                  || ``--public-id``.                      |
   +----------------------------------+----------------------------------------+
   | ``-u, --upload``                 || Upload credential to YubiCloud. This  |
   |                                  || opens a browser. Cannot be used with  |
   |                                  || ``--force``.                          |
   +----------------------------------+----------------------------------------+


----

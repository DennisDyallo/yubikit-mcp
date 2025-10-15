.. Base_Commands.rst

.. _base-commands-label:

===============
Base Commands
===============

The base commands are those that do not apply to any specific protocol. However, they do apply to the different connection methods such as USB and NFC.

See the bottom of this page for acronyms and their definitions.


.. include:: includes/ykman.rst


ykman config [OPTIONS] COMMAND [ARGS]...
========================================

Configure the YubiKey, enable or disable applications. The applications can be enabled and disabled independently over different transports (USB and NFC). The configuration can also be protected by a lock code.

Examples
--------

* Disable PIV over NFC:

  .. code-block::

    $ ykman config nfc --disable PIV

* Enable all applications over USB:

  .. code-block::

    $ ykman config usb --enable-all

* Generate and set a random application lock code:

  .. code-block::

    $ ykman config set-lock-code --generate


Options
-------

.. table::

   +------------------------------+-----------------------------------------------+
   | Option                       | Description                                   |
   +==============================+===============================================+
   | ``-h, --help``               | Show this message and exit.                   |
   +------------------------------+-----------------------------------------------+


Commands
--------

.. table::

   +-------------------+-------------------------------------------------------+
   | Commmand          | Description                                           |
   +===================+=======================================================+
   | ``mode``          | Manage connection modes (USB interfaces).             |
   +-------------------+-------------------------------------------------------+
   | ``nfc``           | Enable or disable applications over NFC.              |
   +-------------------+-------------------------------------------------------+
   | ``reset``         | Reset all YubiKey data.                               |
   +-------------------+-------------------------------------------------------+
   | ``set-lock-code`` | Set or change the configuration lock code.            |
   +-------------------+-------------------------------------------------------+
   | ``usb``           | Enable or disable applications over USB.              |
   +-------------------+-------------------------------------------------------+


ykman config mode [OPTIONS] MODE
================================

Manage connection modes (USB Interfaces). This command is generally used with YubiKeys prior to the 5 series. Use ``ykman config usb`` for more granular control on YubiKey 5 and later. Get the current connection mode of the YubiKey, or set it to ``MODE``. 


Examples
--------

* Set the OTP and FIDO mode:

  .. code-block::

     $ ykman config mode OTP+FIDO

* Set the CCID only mode and use touch to eject the smart card:

  .. code-block::

     $ ykman config mode CCID --touch-eject


Arguments
----------

.. table::

   +------------+--------------------------------------------------------------+
   | Argument   | Description                                                  |
   +============+==============================================================+
   | ``MODE``   || ``MODE`` can be a string, such as ``OTP+FIDO+CCID``, or a   |
   |            || shortened form: ``o+f+c``. It can also be a mode number.    |
   +------------+--------------------------------------------------------------+


Options
-------

.. table::

   +---------------------------------+-----------------------------------------+
   | Option                          | Description                             |
   +=================================+=========================================+
   | ``-h, --help``                  | Show this message and exit.             |
   +---------------------------------+-----------------------------------------+
   | ``--autoeject-timeout SECONDS`` || When set, the smartcard automatically  |
   |                                 || ejects after the given time. Implies   |
   |                                 || ``--touch-eject`` (CCID mode only).    |
   +---------------------------------+-----------------------------------------+
   | ``--chalresp-timeout SECONDS``  || Sets the timeout when waiting for touch|
   |                                 || for challenge response.                |
   +---------------------------------+-----------------------------------------+
   | ``-f, --force``                 | Confirm the action without prompting.   |
   +---------------------------------+-----------------------------------------+
   | ``--touch-eject``               || When set, the button toggles the state |
   |                                 || the smartcard between ejected and      |
   |                                 || inserted (CCID mode only).             |
   +---------------------------------+-----------------------------------------+


ykman config nfc [OPTIONS]
===========================

Enable or disable applications over NFC.


Options
-------

.. table::

   +------------------------------------+--------------------------------------+
   | Option                             | Description                          |
   +====================================+======================================+
   | ``-h, --help``                     | Show this message and exit.          |
   +------------------------------------+--------------------------------------+
   | ``-a, --enable-all``               | Enable all applications.             |
   +------------------------------------+--------------------------------------+
   || ``-d, --disable [OTP|U2F|FIDO2|`` || Disable applications.               |
   || ``OATH|PIV|OPENPGP|HSMAUTH]``     ||                                     |
   +------------------------------------+--------------------------------------+
   | ``-D, --disable-all``              | Disable all applications.            |
   +------------------------------------+--------------------------------------+
   || ``-e, --enable [OTP|U2F|FIDO2|``  || Enable applications.                |
   || ``OATH|PIV|OPENPGP|HSMAUTH]``     ||                                     |
   +------------------------------------+--------------------------------------+
   | ``-f, --force``                    | Confirm the action without prompting.|
   +------------------------------------+--------------------------------------+
   | ``-l, --list``                     | List enabled applications.           |
   +------------------------------------+--------------------------------------+
   | ``-L, --lock-code HEX``            || Current application configuration   |
   |                                    || lock code.                          |
   +------------------------------------+--------------------------------------+
   | ``-R, --restrict``                 || Disable NFC for transport.          |
   |                                    || Re-enable Restricted NFC mode.      |
   |                                    || Available for YubiKeys with         |
   |                                    || firmware version 5.7 and later.     |
   +------------------------------------+--------------------------------------+


ykman config reset [OPTIONS]
===================================

Reset all YubiKey data.

This command is only used with the YubiKey Bio Multi-protocol Edition.

This action wipes all data and restores factory settings for all applications on the YubiKey.

Options
--------

.. table::

   +------------------------------------+--------------------------------------+
   | Option                             | Description                          |
   +====================================+======================================+
   | ``-h, --help``                     | Show this message and exit.          |
   +------------------------------------+--------------------------------------+
   | ``-f, --force``                    | Confirm the action without prompting.|
   +------------------------------------+--------------------------------------+
   


.. _set-lock-code-label:

ykman config set-lock-code [OPTIONS]
====================================

Set or change the configuration lock code. The configuration lock code only applies to the management application. A lock code may be used to protect the application configuration. The lock code must be a 32 characters (16 bytes) hex value. 

Once this code is set, if the user attempts to toggle the on/off state of any of the applications on the key, they are prompted for the configuration lock code. It is only toggling that triggers this; no such prompt appears if a user adds or removes an OATH-TOTP credential, for example.

This command was introduced with firmware version 5.0.


Options
-------

.. table::

   +-----------------------------+----------------------------------------------+
   | Option                      | Description                                  |
   +=============================+==============================================+
   | ``-h, --help``              | Show this message and exit.                  |
   +-----------------------------+----------------------------------------------+
   | ``-c, --clear``             | Clear the lock code.                         |
   +-----------------------------+----------------------------------------------+
   | ``-f, --force``             | Confirm the action without prompting.        |
   +-----------------------------+----------------------------------------------+
   | ``-g, --generate``          || Generate a random lock code. Cannot use     |
   |                             || with ``--new-lock-code``.                   |
   +-----------------------------+----------------------------------------------+
   | ``-l, --lock-code HEX``     | Current lock code.                           |
   +-----------------------------+----------------------------------------------+
   | ``-n, --new-lock-code HEX`` | New lock code. Cannot use with ``--generate``|
   +-----------------------------+----------------------------------------------+


ykman config usb [OPTIONS]
==========================

Enable or disable applications over USB.


Options
-------

.. table::

   +------------------------------------+--------------------------------------+
   | Option                             | Description                          |
   +====================================+======================================+
   | ``-h, --help``                     | Show this message and exit.          |
   +------------------------------------+--------------------------------------+
   | ``-a, --enable-all``               | Enable all applications.             |
   +------------------------------------+--------------------------------------+
   | ``--autoeject-timeout SECONDS``    || When set the smartcard automatically|
   |                                    || ejects after the specified time.    |
   |                                    || Used with ``--touch-eject``.        |
   +------------------------------------+--------------------------------------+
   | ``--chalresp-timeout SECONDS``     || Sets the timeout when waiting for   |
   |                                    || touch response to the challenge-    |
   |                                    || response from the OTP application.  |
   +------------------------------------+--------------------------------------+
   || ``-d, --disable [OTP|U2F|FIDO2|`` || Disable applications.               |
   || ``OATH|PIV|OPENPGP|HSMAUTH]``     ||                                     |
   +------------------------------------+--------------------------------------+
   || ``-e, --enable [OTP|U2F|FIDO2|``  || Enable applications.                |
   || ``OATH|PIV|OPENPGP|HSMAUTH]``     ||                                     |
   +------------------------------------+--------------------------------------+
   | ``-f, --force``                    | Confirm the action without prompting.|
   +------------------------------------+--------------------------------------+
   | ``-l, --list``                     | List enabled applications.           |
   +------------------------------------+--------------------------------------+
   | ``-L, --lock-code HEX``            || Current application configuration   |
   |                                    || lock code.                          |
   +------------------------------------+--------------------------------------+
   | ``--no-touch-eject``               | Disable touch eject (CCID only).     |
   +------------------------------------+--------------------------------------+
   | ``--touch-eject``                  || When set, the button toggles the    |
   |                                    || state of the smartcard between      |
   |                                    || ejected and inserted (CCID only).   |
   +------------------------------------+--------------------------------------+


.. include:: includes/ykman-info.rst



ykman list [OPTIONS]
====================

List connected YubiKeys.


Options
-------

.. table::

   +-------------------+-------------------------------------------------------+
   | Option            | Description                                           |
   +===================+=======================================================+
   | ``-h, --help``    | Show this message and exit.                           |
   +-------------------+-------------------------------------------------------+
   | ``-r, --readers`` | List available smart card readers.                    |
   +-------------------+-------------------------------------------------------+
   | ``-s, --serials`` || Output only serial numbers of the connected YubiKeys,|
   |                   || one per line. Devices without serial numbers are not |
   |                   || listed.                                              |
   +-------------------+-------------------------------------------------------+



ykman script [OPTIONS] FILE [ARGUMENTS]
========================================

Run a Python script.

.. WARNING:: Never run a script without fully understanding what it does! Scripts are very powerful, and have the power to harm to both your YubiKey and your computer. ONLY run scripts that you fully trust!

Arguments can be passed to the script by adding them after the end of the command. These are accessible inside the script as ``sys.argv``, with the script name as the initial value. For more information on scripting, see `sys.argv in the Python.org documentation <https://docs.python.org/3/library/sys.html#sys.argv>`_.

Examples
---------

Run the file ``myscript.py``, passing arguments ``123456`` and ``indata.csv``:

.. code-block::

   $ ykman script myscript.py 123456 indata.csv

Options
-------

.. table::

   +----------------------------+---------------------------------------------+
   | Option                     | Description                                 |
   +============================+=============================================+
   | ``-h, --help``             | Show this message and exit.                 |
   +----------------------------+---------------------------------------------+
   | ``-f, --force``            | Confirm the action without prompting.       |
   +----------------------------+---------------------------------------------+
   | ``-s, --site-dir DIR``     || Specify additional path(s) from which to   |
   |                            || load Python modules.                       |
   +----------------------------+---------------------------------------------+
   

.. include:: includes/acronyms.rst

----

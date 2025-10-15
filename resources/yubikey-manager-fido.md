.. FIDO_Commands.rst

=============
FIDO Commands
=============

On Windows, FIDO operations are privileged. Therefore you must run Command Prompt or PowerShell as administrator in order to be able to run commands that begin with ``ykman fido``.

Acronyms and their definitions are listed at the bottom of the :ref:`base-commands-label` page.



ykman fido [OPTIONS] COMMAND [ARGS]...
======================================

Manage FIDO applications.


Examples
--------

* Reset the FIDO (FIDO2 and U2F) applications:

  .. code-block::

     $ ykman fido reset

* Change the FIDO2 PIN from 123456 to 654321:

  .. code-block::

     $ ykman fido access change-pin --pin 123456 --new-pin 654321


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
   | ``access``       | Manage the PIN for FIDO.                               |
   +------------------+--------------------------------------------------------+
   | ``config``       | Manage FIDO configuration.                             |
   +------------------+--------------------------------------------------------+
   | ``credentials``  | Manage discoverable (resident) credentials.            |
   +------------------+--------------------------------------------------------+
   | ``fingerprints`` | Manage fingerprints.                                   |
   +------------------+--------------------------------------------------------+
   | ``info``         | Display status of FIDO2 application.                   |
   +------------------+--------------------------------------------------------+
   | ``reset``        | Reset all FIDO applications.                           |
   +------------------+--------------------------------------------------------+



ykman fido access [OPTIONS] COMMAND [ARGS]...
==============================================

Manage the PIN for FIDO.


Options
-------

.. table::

   +-----------------+---------------------------------------------------------+
   | Option          | Description                                             |
   +=================+=========================================================+
   | ``-h, --help``  | Show this message and exit.                             |
   +-----------------+---------------------------------------------------------+


Commands
--------

.. table::

   +-------------------+--------------------------------------------------------+
   | Command           | Description                                            |
   +===================+========================================================+
   | ``change-pin``    | Set or change the PIN code.                            |
   +-------------------+--------------------------------------------------------+
   | ``force-change``  || Force the PIN to be changed to a new value before use.|
   |                   || Command introduced in ykman (CLI) version 5.3.0.      |
   +-------------------+--------------------------------------------------------+
   | ``set-min-length``|| Set the minimum length allowed for PIN.               |
   |                   || Command introduced in ykman (CLI) version 5.3.0.      |
   +-------------------+--------------------------------------------------------+
   | ``verify-pin``    | Verify the FIDO PIN against a YubiKey.                 |
   +-------------------+--------------------------------------------------------+


ykman fido access change-pin [OPTIONS]
======================================

Set or change the PIN code.

The FIDO2 PIN must be at least 4 characters, and supports any type of alphanumeric characters. Some YubiKeys can be configured to require a longer PIN.

On YubiKey FIPS (4 Series), a PIN can be set for FIDO U2F. That PIN must be at least 6 characters.


Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+
   | ``-n, --new-pin TEXT`` | A new PIN.                                       |
   +------------------------+--------------------------------------------------+
   | ``-P, --pin TEXT``     | Current PIN code.                                |
   +------------------------+--------------------------------------------------+
   | ``-u, --u2f``          || Set FIDO U2F PIN instead of FIDO2 PIN.          |
   |                        || Applies to YubiKey FIPS only.                   |
   +------------------------+--------------------------------------------------+



ykman fido access force-change [OPTIONS]
========================================

Force the PIN to be changed to a new value before use.

Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+
   | ``-P, --pin TEXT``     | PIN code.                                        |
   +------------------------+--------------------------------------------------+



ykman fido access set-min-length [OPTIONS] LENGTH
==================================================

Set the minimum length allowed for the PIN.

Use the ``--rp`` option to specify which Relying Part (RPs) are allowed to request this information.

Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+
   | ``-P, --pin TEXT``     | PIN code.                                        |
   +------------------------+--------------------------------------------------+
   | ``-R, --rp-id TEXT``   | RP ID to allow.                                  |
   +------------------------+--------------------------------------------------+



ykman fido access unlock [OPTIONS] (Deprecated)
================================================

**Yubico replaced the ``unlock`` command with the ``verify-pin`` command.**

Verify U2F PIN for YubiKey FIPS. Unlock the YubiKey FIPS and allow U2F registration.


Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+
   | ``-P, --pin TEXT``     | Current PIN code.                                |
   +------------------------+--------------------------------------------------+



ykman fido access verify-pin [OPTIONS]
=======================================

Verify the FIDO PIN against a YubiKey. For YubiKeys supporting FIDO2 this resets the ``retries`` counter of the PIN. For YubiKey FIPS (4 Series) this unlocks the session, allowing U2F registration.


Options
--------

.. table::

   +---------------------+-----------------------------------------------------+
   | Option              | Description                                         |
   +=====================+=====================================================+
   | ``-h, --help``      | Show this message and exit.                         |
   +---------------------+-----------------------------------------------------+
   | ``-P, --pin TEXT``  | Current PIN code.                                   |
   +---------------------+-----------------------------------------------------+



ykman fido config [OPTIONS] COMMAND [ARGS]...
==============================================

Manage FIDO configuration.


Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+


Commands
---------

.. table::

   +---------------------------+-----------------------------------------------+
   | Command                   | Description                                   |
   +===========================+===============================================+
   | ``enable-ep-attestation`` || Enables Enterprise Attestation for           |
   |                           || Authenticators pre-configured to support it. |
   |                           || Command introduced in ykman (CLI) v5.3.0.    |
   +---------------------------+-----------------------------------------------+
   | ``toggle-always-uv``      || Toggles the state of Always Require User     |
   |                           || Verification.                                |
   |                           || Command introduced in ykman (CLI) v5.3.0.    |
   +---------------------------+-----------------------------------------------+


ykman fido config enable-ep-attestation [OPTIONS]
=================================================

Enables Enterprise Attestation for Authenticators pre-configured to support it.

Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+
   | ``-P, --pin TEXT``     | PIN code.                                        |
   +------------------------+--------------------------------------------------+



ykman fido config toggle-always-uv [OPTIONS]
=============================================

Toggles the state of Always Require User Verification.

Options
-------

.. table::

   +------------------------+--------------------------------------------------+
   | Option                 | Description                                      |
   +========================+==================================================+
   | ``-h, --help``         | Show this message and exit.                      |
   +------------------------+--------------------------------------------------+
   | ``-P, --pin TEXT``     | PIN code.                                        |
   +------------------------+--------------------------------------------------+



ykman fido credentials [OPTIONS] COMMAND [ARGS]...
===================================================

Manage discoverable (resident) credentials. This command lets you manage credentials stored on your YubiKey. Credential management is only available when a FIDO PIN is set on the YubiKey.

.. Note:: Managing credentials requires having a PIN. Set a PIN before trying to manage credentials.


Examples
--------

* List stored credentials (providing PIN via argument):

  .. code-block::

     $ ykman fido credentials list --pin 123456

* Delete a credential by user name (PIN is prompted for):

  .. code-block::

     $ ykman fido credentials delete example_user


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

   +-------------+-------------------------------------------------------------+
   | Command     | Description                                                 |
   +=============+=============================================================+
   | ``delete``  | Delete a resident credential.                               |
   +-------------+-------------------------------------------------------------+
   | ``list``    | List resident credentials.                                  |
   +-------------+-------------------------------------------------------------+



ykman fido credentials delete [OPTIONS] CREDENTIAL_ID
======================================================

Delete a credential. List stored credential IDs using the ``list`` subcommand.


Arguments
----------

.. table::

   +--------------------+--------------------------------------------------------+
   | Argument           | Description                                            |
   +====================+========================================================+
   | ``CREDENTIAL_ID``  | A unique substring match of a Credential ID.           |
   +--------------------+--------------------------------------------------------+


Options
--------

.. table::

   +--------------------+------------------------------------------------------+
   | Option             | Description                                          |
   +====================+======================================================+
   | ``-h, --help``     | Show this message and exit.                          |
   +--------------------+------------------------------------------------------+
   | ``-f, --force``    | Confirm deletion without prompting.                  |
   +--------------------+------------------------------------------------------+
   | ``-P, --pin TEXT`` | PIN code.                                            |
   +--------------------+------------------------------------------------------+



ykman fido credentials list [OPTIONS]
=====================================

List credentials. Shows a list of credentials stored on the YubiKey.

The ``--csv`` flag returns more complete information about each credential, in CSV (comma separated values) format.


Options
-------

.. table::

   +---------------------+-----------------------------------------------------+
   | Option              | Description                                         |
   +=====================+=====================================================+
   | ``-h, --help``      | Show this message and exit.                         |
   +---------------------+-----------------------------------------------------+
   | ``-c, --csv``       | Returns full credential information in CSV format.  |
   +---------------------+-----------------------------------------------------+
   | ``-P, --pin TEXT``  | PIN code.                                           |
   +---------------------+-----------------------------------------------------+



ykman fido fingerprints [OPTIONS] COMMAND [ARGS]...
====================================================

Manage fingerprints. Requires a YubiKey with fingerprint sensor. Fingerprint management is available only when a FIDO PIN is set on the YubiKey.


Examples
---------

* Register a new fingerprint (providing PIN via argument):

  .. code-block::

     $ ykman fido fingerprints add "Left thumb" --pin 123456

* List already stored fingerprints (providing PIN via argument):

  .. code-block::

     $ ykman fido fingerprints list --pin 123456

* Delete a stored fingerprint with ID "f691" (PIN is prompted for):

  .. code-block::

     $ ykman fido fingerprints delete f691


Options
--------

.. table::

   +------------------+--------------------------------------------------------+
   | Option           | Description                                            |
   +==================+========================================================+
   | ``-h, --help``   | Show this message and exit.                            |
   +------------------+--------------------------------------------------------+


Commands
--------

.. table::

   +------------------+--------------------------------------------------------+
   | Command          | Description                                            |
   +==================+========================================================+
   | ``add``          | Add a new fingerprint.                                 |
   +------------------+--------------------------------------------------------+
   | ``delete``       | Delete a fingerprint.                                  |
   +------------------+--------------------------------------------------------+
   | ``list``         | List registered fingerprint.                           |
   +------------------+--------------------------------------------------------+
   | ``rename``       | Set the label for a fingerprint.                       |
   +------------------+--------------------------------------------------------+



ykman fido fingerprints add [OPTIONS] NAME
===========================================

Add a new fingerprint.


Arguments
----------

.. table::

   +--------------+------------------------------------------------------------+
   | Argument     | Description                                                |
   +==============+============================================================+
   | ``NAME``     || Short readable name for the fingerprint.                  |
   |              || For example, "Left thumb".                                |
   +--------------+------------------------------------------------------------+


Options
--------

.. table::

   +---------------------+-----------------------------------------------------+
   | Option              | Description                                         |
   +=====================+=====================================================+
   | ``-h, --help``      | Show this message and exit.                         |
   +---------------------+-----------------------------------------------------+
   | ``-P, --pin TEXT``  | PIN code.                                           |
   +---------------------+-----------------------------------------------------+



ykman fido fingerprints delete [OPTIONS] ID
===========================================

Delete a fingerprint. Delete a fingerprint from the YubiKey by its ID. To view the YuibiKey ID, run the ``ykman fido fingerprints list`` command. 


Arguments
----------

.. table::

   +-----------+---------------------------------------------------------------+
   | Argument  | Description                                                   |
   +===========+===============================================================+
   | ``ID``    | To see the ID run the ``fingerprints list`` subcommand.       |
   +-----------+---------------------------------------------------------------+


Options
--------

.. table::

   +---------------------+-----------------------------------------------------+
   | Option              | Description                                         |
   +=====================+=====================================================+
   | ``-h, --help``      | Show this message and exit.                         |
   +---------------------+-----------------------------------------------------+
   | ``-f, --force``     | Confirm deletion without prompting.                 |
   +---------------------+-----------------------------------------------------+
   | ``-P, --pin TEXT``  | PIN code.                                           |
   +---------------------+-----------------------------------------------------+



ykman fido fingerprints list [OPTIONS]
======================================

List registered fingerprint. Lists fingerprints by ID and (if available) label.


Options
--------

.. table::

   +---------------------+-----------------------------------------------------+
   | Option              | Description                                         |
   +=====================+=====================================================+
   | ``-h, --help``      | Show this message and exit.                         |
   +---------------------+-----------------------------------------------------+
   | ``-P, --pin TEXT``  | PIN code.                                           |
   +---------------------+-----------------------------------------------------+



ykman fido fingerprints rename [OPTIONS] ID NAME
================================================

Set the label for a fingerprint.


Arguments
----------

.. table::

   +--------------+------------------------------------------------------------+
   | Argument     | Description                                                |
   +==============+============================================================+
   | ``ID``       || The ID of the fingerprint to rename.                      |
   |              || See ``fingerprints list``.                                |
   +--------------+------------------------------------------------------------+
   | ``NAME``     || Short readable name for the fingerprint.                  |
   |              || For example, "Left thumb".                                |
   +--------------+------------------------------------------------------------+


Options:
--------

.. table::

   +---------------------+-----------------------------------------------------+
   | Option              | Description                                         |
   +=====================+=====================================================+
   | ``-h, --help``      | Show this message and exit.                         |
   +---------------------+-----------------------------------------------------+
   | ``-P, --pin TEXT``  | PIN code.                                           |
   +---------------------+-----------------------------------------------------+




.. include:: includes/ykman-fido-info.rst


.. include:: includes/ykman-fido-reset.rst


----

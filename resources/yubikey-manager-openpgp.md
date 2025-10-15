.. OpenPGP_Commands.rst

.. _openpgp-commands-label:

================
OpenPGP Commands
================

Acronyms and their definitions are listed at the bottom of the :ref:`base-commands-label` page.


ykman openpgp [OPTIONS] COMMAND [ARGS]...
=========================================

Manage OpenPGP application.


Examples
--------

**Set the retries** for PIN, Reset Code and Admin PIN to 10:

.. code-block::

  $ ykman openpgp access set-retries 10 10 10

**Require touch** to use the authentication key:

.. code-block::

  $ ykman openpgp keys set-touch aut on


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

   +------------------+--------------------------------------------------------+
   | Command          | Description                                            |
   +==================+========================================================+
   | ``access``       | Manage PIN, Reset Code, and Admin PIN.                 |
   +------------------+--------------------------------------------------------+
   | ``certificates`` | Manage certificates.                                   |
   +------------------+--------------------------------------------------------+
   | ``info``         | Display general status of the OpenPGP application.     |
   +------------------+--------------------------------------------------------+
   | ``keys``         | Manage private keys.                                   |
   +------------------+--------------------------------------------------------+
   | ``reset``        | Reset all OpenPGP data.                                |
   +------------------+--------------------------------------------------------+


ykman openpgp access [OPTIONS] COMMAND [ARGS]...
=================================================

Manage PIN, Reset Code, and Admin PIN.


Options
--------

.. table::

   +------------------+--------------------------------------------------------+
   | Option           | Description                                            |
   +==================+========================================================+
   | ``-h, --help``   | Show this message and exit.                            |
   +------------------+--------------------------------------------------------+


Commands
---------

.. table::

   +--------------------------+------------------------------------------------+
   | Command                  | Description                                    |
   +==========================+================================================+
   | ``change-admin-pin``     | Change the Admin PIN.                          |
   +--------------------------+------------------------------------------------+
   | ``change-pin``           | Change the User PIN.                           |
   +--------------------------+------------------------------------------------+
   | ``change-reset-code``    | Change the Reset Code.                         |
   +--------------------------+------------------------------------------------+
   | ``set-retries``          | Set the number of retry attempts for the user. |
   +--------------------------+------------------------------------------------+
   | ``set-signature-policy`` | Set the Signature PIN policy.                  |
   +--------------------------+------------------------------------------------+
   | ``unblock-pin``          | Unblock the PIN using Reset Code or Admin PIN. |
   +--------------------------+------------------------------------------------+


ykman openpgp access change-admin-pin [OPTIONS]
===============================================

Change the Admin PIN. The Admin PIN has a minimum length of 8, and supports any type of alphanumeric characters.

Options
--------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-a, --admin-pin TEXT``     | Current Admin PIN.                         |
   +------------------------------+--------------------------------------------+
   | ``-n, --new-admin-pin TEXT`` | New Admin PIN.                             |
   +------------------------------+--------------------------------------------+
  


ykman openpgp access change-pin [OPTIONS]
=========================================

Change the User PIN. The PIN has a minimum length of 6, and supports any type of alphanumeric characters. PIN minimum length for YubiKey FIPS 5.7.+ when not using Key Derivation Function (KDF) is 8. 

Options
--------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-n, --new-pin TEXT``       | A new PIN.                                 |
   +------------------------------+--------------------------------------------+
   | ``-P, --pin TEXT``           | Current PIN code.                          |
   +------------------------------+--------------------------------------------+
  
 

ykman openpgp access change-reset-code [OPTIONS]
=================================================

Change the Reset Code. The Reset Code has a minimum length of 6, and supports any type of alphanumeric characters.

Options
--------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-a, --admin-pin TEXT``     | Admin PIN.                                 |
   +------------------------------+--------------------------------------------+
   | ``-r, --reset-code TEXT``    | A new Reset Code.                          |
   +------------------------------+--------------------------------------------+
  


ykman openpgp access set-retries [OPTIONS] PIN-RETRIES RESET-CODE-RETRIES ADMIN-PIN-RETRIES
===========================================================================================

Set the number of retry attempts for the user PIN, Reset Code, and Admin PIN.


Arguments
----------

.. table::

   +------------------------+--------------------------------------------------+
   | Argument               | Description                                      |
   +========================+==================================================+
   | ``PIN-RETRIES``        | Set number of retries for PIN attempts.          |
   +------------------------+--------------------------------------------------+
   | ``RESET-CODE-RETRIES`` | Set number of retries for Reset Code attempts.   |
   +------------------------+--------------------------------------------------+
   | ``ADMIN-PIN-RETRIES``  | Set number of retries for Admin PIN attempts.    |
   +------------------------+--------------------------------------------------+


Options
--------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+
   | ``-a, --admin-pin TEXT``  | Admin PIN for OpenPGP.                        |
   +---------------------------+-----------------------------------------------+
   | ``-f, --force``           | Confirm the action without prompting.         |
   +---------------------------+-----------------------------------------------+


ykman openpgp access set-signature-policy [OPTIONS] POLICY
==========================================================

Set the Signature PIN policy. The Signature PIN policy is used to control whether the PIN is always required when using the Signature key, or if it is required only once per session.

Arguments
----------

.. table::

   +------------------------+--------------------------------------------------+
   | Argument               | Description                                      |
   +========================+==================================================+
   | ``POLICY``             | Signature PIN policy to set (always, once).      |
   +------------------------+--------------------------------------------------+


Options
--------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-a, --admin-pin TEXT``     | Admin PIN for OpenPGP.                     |
   +------------------------------+--------------------------------------------+



ykman openpgp access unblock-pin [OPTIONS]
==========================================

Unblock the PIN, using Reset Code or Admin PIN. 

If the PIN is lost or blocked you can reset it to a new value using the Reset Code. Alternatively, the Admin PIN can be used with the ``-a, --admin-pin`` option, instead of the Reset Code.

The new PIN has a minimum length of 6, and supports any type of alphanumeric characters.


Options
--------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-a, --admin-pin TEXT``     || Admin PIN. Use ``-`` as a value to        |
   |                              || prompt for input.                         |
   +------------------------------+--------------------------------------------+
   | ``-n, --new-pin TEXT``       | A new PIN.                                 |
   +------------------------------+--------------------------------------------+
   | ``-r, --reset-code TEXT``    | Reset Code.                                |
   +------------------------------+--------------------------------------------+



ykman openpgp certificates [OPTIONS] COMMAND [ARGS]...
=======================================================

Manage certificates.

Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+


Commands
---------

.. table::

   +---------------------------+-----------------------------------------------+
   | Command                   | Description                                   |
   +===========================+===============================================+
   | ``delete``                | Delete an OpenPGP certificate.                |
   +---------------------------+-----------------------------------------------+
   | ``export``                | Export an OpenPGP certificate.                |
   +---------------------------+-----------------------------------------------+
   | ``import``                | Import an OpenPGP certificate.                |
   +---------------------------+-----------------------------------------------+



ykman openpgp certificates delete [OPTIONS] KEY
===============================================

Delete an OpenPGP certificate.


Arguments
---------

.. table::

   +---------------+-----------------------------------------------------------+
   | Argument      | Description                                               |
   +===============+===========================================================+
   | ``KEY``       || Key slot to delete certificate from ``sig``, ``enc``,    |
   |               || ``aut``,  or ``att``.                                    |
   +---------------+-----------------------------------------------------------+


Options
-------

.. table::

   +---------------------------+-----------------------------------------------+
   | Option                    | Description                                   |
   +===========================+===============================================+
   | ``-h, --help``            | Show this message and exit.                   |
   +---------------------------+-----------------------------------------------+
   | ``-a, --admin-pin TEXT``  | Admin PIN for OpenPGP.                        |
   +---------------------------+-----------------------------------------------+



ykman openpgp certificates export [OPTIONS] KEY CERTIFICATE
===========================================================

Export an OpenPGP certificate.


Arguments
---------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``CERTIFICATE``  || File to write certificate to. Use ``-`` to use        |
   |                  || ``stdout``.                                           |
   +------------------+--------------------------------------------------------+
   | ``KEY``          || Key slot to read from (``sig``, ``enc``, ``aut``,     |
   |                  || or ``att``).                                          |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +-----------------------------+---------------------------------------------+
   | Option                      | Description                                 |
   +=============================+=============================================+
   | ``-h, --help``              | Show this message and exit.                 |
   +-----------------------------+---------------------------------------------+
   | ``-F, --format [PEM|DER]``  | Encoding format.  Default: ``PEM``          |
   +-----------------------------+---------------------------------------------+



ykman openpgp certificates import [OPTIONS] KEY CERTIFICATE
===========================================================

Import an OpenPGP certificate.


Arguments
---------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``CERTIFICATE``  || File containing the certificate. Use ``-`` to         |
   |                  || use ``stdin``.                                        |
   +------------------+--------------------------------------------------------+
   | ``KEY``          || Key slot to import certificate to (``sig``, ``enc``,  |
   |                  || ``aut``, or ``att``).                                 |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +-----------------------------+---------------------------------------------+
   | Option                      | Description                                 |
   +=============================+=============================================+
   | ``-h, --help``              | Show this message and exit.                 |
   +-----------------------------+---------------------------------------------+
   | ``-a, --admin-pin TEXT``    | Admin PIN for OpenPGP.                      |
   +-----------------------------+---------------------------------------------+


ykman openpgp info [OPTIONS]
============================

Display status of OpenPGP application.


Options
-------

.. table::

   +----------------+----------------------------------------------------------+
   | Option         | Description                                              |
   +================+==========================================================+
   | ``-h, --help`` | Show this message and exit.                              |
   +----------------+----------------------------------------------------------+



ykman openpgp keys [OPTIONS] COMMAND [ARGS]...
==============================================

Manage private keys.


Options
--------

.. table::

   +-----------------------------+---------------------------------------------+
   | Option                      | Description                                 |
   +=============================+=============================================+
   | ``-h, --help``              | Show this message and exit.                 |
   +-----------------------------+---------------------------------------------+


Commands
---------

.. table::

   +------------------+--------------------------------------------------------+
   | Command          | Description                                            |
   +==================+========================================================+
   | ``attest``       | Generate an attestation certificate for a key.         |
   +------------------+--------------------------------------------------------+
   | ``import``       | Import a private key for OpoenPGP attestation.         |
   +------------------+--------------------------------------------------------+
   | ``info``         | Show metadata about a private key.                     |
   +------------------+--------------------------------------------------------+
   | ``set-touch``    | Set touch policy for OpenPGP keys.                     |
   +------------------+--------------------------------------------------------+



ykman openpgp keys attest [OPTIONS] KEY CERTIFICATE
===================================================

Generate an attestation certificate for a key. Attestation is used to show that an asymmetric key was generated on the YubiKey and therefore does not exist outside the device.


Arguments
---------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``KEY``         | Key slot to attest (``sig``, ``enc``, ``aut``).         |
   +-----------------+---------------------------------------------------------+
   | ``CERTIFICATE`` || File to write attestation certificate to. Use ``-``    |
   |                 || to use ``stdout``.                                     |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-F, --format [PEM|DER]``   | Encoding format.  Default: ``PEM``         |
   +------------------------------+--------------------------------------------+
   | ``-P, --pin TEXT``           | PIN code.                                  |
   +------------------------------+--------------------------------------------+



ykman openpgp keys import [OPTIONS] KEY PRIVATE-KEY
===================================================

Import a private key for OpenPGP attestation.

The attestation key is by default pre-generated during production with a Yubico-issued key and certificate.

.. WARNING:: This private key cannot be recovered once overwritten!


Arguments
---------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``KEY``         | Key slot to import to. Only ``att`` is supported.       |
   +-----------------+---------------------------------------------------------+
   | ``PRIVATE-KEY`` || File containing the private key. Use ``-`` to          |
   |                 || use ``stdin``.                                         |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+
   | ``-a, --admin-pin TEXT``     | Admin PIN for OpenPGP.                     |
   +------------------------------+--------------------------------------------+



ykman openpgp keys info  [OPTIONS] KEY
===================================================

Shows metadata about a private key.

This shows what type of key is stored in a specific slot, whether it was imported into the YubiKey, or generated on-chip, and what the Touch policy is for using the key.


Arguments
---------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``KEY``         | Key slot to set (``sig``, ``dec``, ``enc``, ``aut``).   |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +------------------------------+--------------------------------------------+
   | Option                       | Description                                |
   +==============================+============================================+
   | ``-h, --help``               | Show this message and exit.                |
   +------------------------------+--------------------------------------------+



ykman openpgp keys set-touch [OPTIONS] KEY POLICY
=================================================

Set touch policy for OpenPGP keys. The touch policy is used to require user interaction for all operations using the private key on the YubiKey. The touch policy is set individually for each key slot. 

To see the current touch policy, run:

.. code-block::

   $ ykman openpgp info


.. WARNING:: Setting the touch policy of the attestation key to "fixed" cannot
  be undone without replacing the attestation private key.

Arguments
---------

.. table::

   +-------------+-------------------------------------------------------------+
   | Argument    | Description                                                 |
   +=============+=============================================================+
   | ``KEY``     | Key slot to set (``sig``, ``enc``, ``aut`` or ``att``).     |
   +-------------+-------------------------------------------------------------+
   | ``POLICY``  | Touch policy to set (``on``, ``off``, ``fixed``, ``cached`` |
   |             | or ``cached-fixed``).                                       |
   +-------------+-------------------------------------------------------------+


Touch Policies
---------------

.. table::

   +------------------+--------------------------------------------------------+
   | Policy           | Description                                            |
   +==================+========================================================+
   | ``Cached``       | Touch required, cached for 15s after use.              |
   +------------------+--------------------------------------------------------+
   | ``Cached-Fixed`` || Touch required, cached for 15s after use, cannot be   |
   |                  || disabled without deleting the private key.            |
   +------------------+--------------------------------------------------------+
   | ``Fixed``        || Touch required, cannot be disabled without deleting   |
   |                  || the private key.                                      |
   +------------------+--------------------------------------------------------+
   | ``Off``          | No touch required. (Default)                           |
   +------------------+--------------------------------------------------------+
   | ``On``           | Touch required.                                        |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +--------------------------+------------------------------------------------+
   | Option                   | Description                                    |
   +==========================+================================================+
   | ``-h, --help``           | Show this message and exit.                    |
   +--------------------------+------------------------------------------------+
   | ``-a, --admin-pin TEXT`` | Admin PIN for OpenPGP.                         |
   +--------------------------+------------------------------------------------+
   | ``-f, --force``          | Confirm the action without prompting.          |
   +--------------------------+------------------------------------------------+


ykman openpgp reset [OPTIONS]
=============================

Reset OpenPGP application. This action wipes all OpenPGP data, and sets all PINs to their default values.

The attestation key and certificate are not reset.

Options
-------

.. table::

   +------------------+--------------------------------------------------------+
   | Option           | Description                                            |
   +==================+========================================================+
   | ``-h, --help``   | Show this message and exit.                            |
   +------------------+--------------------------------------------------------+
   | ``-f, --force``  | Confirm the action without prompting.                  |
   +------------------+--------------------------------------------------------+


----

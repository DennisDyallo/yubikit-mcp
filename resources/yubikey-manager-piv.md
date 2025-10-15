.. PIV_Commands.rst

.. _piv-commands-label:

============
PIV Commands
============

Acronyms and their definitions are listed at the bottom of the :ref:`base-commands-label` page.


ykman piv [OPTIONS] COMMAND [ARGS]...
=====================================

Manage the PIV Application.


Examples
--------

**Generate** an ECC P-256 private key and a self-signed certificate in slot 9a:

.. code-block::

   $ ykman piv keys generate --algorithm ECCP256 9a pubkey.pem
   $ ykman piv certificates generate --subject "CN=yubico" 9a pubkey.pem

**Change the PIN** from 123456 to 654321:

.. code-block::

   $ ykman piv access change-pin --pin 123456 --new-pin 654321

**Reset all PIV data** and restore default settings:

.. code-block::

   $ ykman piv reset


Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+


Commands
--------

.. table::

   +-------------------+-------------------------------------------------------+
   | Command           | Description                                           |
   +===================+=======================================================+
   | ``access``        | Manage PIN, PUK, and Management Key.                  |
   +-------------------+-------------------------------------------------------+
   | ``certificates``  | Manage certificates.                                  |
   +-------------------+-------------------------------------------------------+
   | ``info``          | Display general status of the PIV application.        |
   +-------------------+-------------------------------------------------------+
   | ``keys``          | Manage private keys.                                  |
   +-------------------+-------------------------------------------------------+
   | ``objects``       | Manage PIV data objects.                              |
   +-------------------+-------------------------------------------------------+
   | ``reset``         | Reset all PIV data.                                   |
   +-------------------+-------------------------------------------------------+



ykman piv access [OPTIONS] COMMAND [ARGS]...
============================================

Manage PIN, PUK, and Management Key.


Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+


Commands
--------

.. table::

   +---------------------------+-----------------------------------------------+
   | Command                   | Description                                   |
   +===========================+===============================================+
   | ``change-management-key`` | Change the management key.                    |
   +---------------------------+-----------------------------------------------+
   | ``change-pin``            | Change the PIN code.                          |
   +---------------------------+-----------------------------------------------+
   | ``change-puk``            | Change the PUK code.                          |
   +---------------------------+-----------------------------------------------+
   | ``set-retries``           | Set the number of PIN and PUK retry attempts. |
   +---------------------------+-----------------------------------------------+
   | ``unblock-pin``           | Unblock the PIN (using the PUK).              |
   +---------------------------+-----------------------------------------------+


ykman piv access change-management-key [OPTIONS]
================================================

Change the management key. Management functionality is guarded by a management key. This key is required for administrative tasks, such as generating key pairs. A random key may be generated and stored on the YubiKey, protected by PIN.

.. Note:: With the release of the 5.7 YubiKey firmware version, Advanced Encryption Standard 192 bit (AES-192) is the default **security type** for the PIV management key. Triple Data Encryption Standard (TDES or 3DES) is the default security type for YubiKey firmware versions older than 5.7. 

          The default **value** is the same for all firmware versions, regardless of the security type. For this value as well as the default PIN and PUK codes, see the `"General Information" section of "Yubico PIV Tool" on our developer site <https://developers.yubico.com/yubico-piv-tool/YubiKey_PIV_introduction.html#:~:text=General%20information,key%20(9B)%20is%20010203040506070801020304050607080102030405060708>`_.


Options
-------

.. table::

   +-----------------------------------+--------------------------------------------+
   | Option                            | Description                                |
   +===================================+============================================+
   | ``-h, --help``                    | Show this message and exit.                |
   +-----------------------------------+--------------------------------------------+
   || ``-a, --algorithm [TDES|``       || Management key algorithm.                 |
   || ``AES128|AES192|AES256]``        || Default v5.7: ``AES-192``                 |
   |                                   || Default pre-v.5.7: ``TDES``               |
   +-----------------------------------+--------------------------------------------+
   | ``-f, --force``                   | Confirm the action without prompting.      |
   +-----------------------------------+--------------------------------------------+
   | ``-g, --generate``                || Generate a random management key.         |
   |                                   || Implied by ``--protect`` unless           |
   |                                   || ``--new-management-key`` is also          |
   |                                   || given. Cannot be used  with               |
   |                                   || ``--new-management-key``.                 |
   +-----------------------------------+--------------------------------------------+
   | ``-m, --management-key TEXT``     | Current management key. TEXT=identifier.   |
   +-----------------------------------+--------------------------------------------+
   | ``-n, --new-management-key TEXT`` | Set a new management key. TEXT=identifier. |
   +-----------------------------------+--------------------------------------------+
   | ``-p, --protect``                 || Store new management key on the           |
   |                                   || YubiKey, protected by PIN. A random       |
   |                                   || key is used if no key is provided.        |
   +-----------------------------------+--------------------------------------------+
   | ``-P, --pin TEXT``                | PIN code.                                  |
   +-----------------------------------+--------------------------------------------+
   | ``-t, --touch``                   || Require touch on YubiKey when             |
   |                                   || prompted for management key.              |
   +-----------------------------------+--------------------------------------------+



ykman piv access change-pin [OPTIONS]
=====================================

Change the PIN code. The PIN must be between 6 and 8 alphanumeric characters. For cross-platform compatibility, numeric PINs are recommended.


Options
-------

.. table::

   +-----------------------------------+---------------------------------------+
   | Option                            | Description                           |
   +===================================+=======================================+
   | ``-h, --help``                    | Show this message and exit.           |
   +-----------------------------------+---------------------------------------+
   | ``-n, --new-pin TEXT``            | Set a new PIN.                        |
   +-----------------------------------+---------------------------------------+
   | ``-P, --pin TEXT``                | Current PIN code.                     |
   +-----------------------------------+---------------------------------------+



ykman piv access change-puk [OPTIONS]
=====================================

Change the PUK code. If the PIN is lost or blocked it can be reset using a PUK. The PUK must be between 6 and 8 bytes long and can be any type of alphanumeric character.


Options
-------

.. table::

   +-----------------------------------+---------------------------------------+
   | Option                            | Description                           |
   +===================================+=======================================+
   | ``-h, --help``                    | Show this message and exit.           |
   +-----------------------------------+---------------------------------------+
   | ``-n, --new-puk TEXT``            | Set a new PUK code.                   |
   +-----------------------------------+---------------------------------------+
   | ``-p, --puk TEXT``                | Current PUK code.                     |
   +-----------------------------------+---------------------------------------+



ykman piv access set-retries [OPTIONS] PIN-RETRIES PUK-RETRIES
==============================================================

Set the number of PIN and PUK retry attempts.

.. NOTE:: This resets the PIN and PUK to their factory defaults.


Arguments
----------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``PIN-RETRIES`` | Set number of retries for PIN attempts.                 |
   +-----------------+---------------------------------------------------------+
   | ``PUK-RETRIES`` | Set number of retries for PUK attempts.                 |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +-----------------------------------+----------------------------------------+
   | Option                            | Description                            |
   +===================================+========================================+
   | ``-h, --help``                    | Show this message and exit.            |
   +-----------------------------------+----------------------------------------+
   | ``-f, --force``                   | Confirm the action without prompting.  |
   +-----------------------------------+----------------------------------------+
   | ``-m, --management-key TEXT``     | The management key. TEXT=identifier.   |
   +-----------------------------------+----------------------------------------+
   | ``-P, --pin TEXT``                | PIN code.                              |
   +-----------------------------------+----------------------------------------+



ykman piv access unblock-pin [OPTIONS]
======================================

Unblock the PIN, using PUK.


Options
-------

.. table::

   +-----------------------------------+---------------------------------------+
   | Option                            | Description                           |
   +===================================+=======================================+
   | ``-h, --help``                    | Show this message and exit.           |
   +-----------------------------------+---------------------------------------+
   | ``-n, --new-pin NEW-PIN``         | Set a new PIN code.                   |
   +-----------------------------------+---------------------------------------+
   | ``-p, --puk TEXT``                | Current PUK code.                     |
   +-----------------------------------+---------------------------------------+


ykman piv certificates [OPTIONS] COMMAND [ARGS]...
==================================================

Manage certificates.


Options
-------

.. table::

   +-----------------------------------+---------------------------------------+
   | Option                            | Description                           |
   +===================================+=======================================+
   | ``-h, --help``                    | Show this message and exit.           |
   +-----------------------------------+---------------------------------------+


Commands
--------

.. table::

   +--------------+------------------------------------------------------------+
   | Option       | Description                                                |
   +==============+============================================================+
   | ``delete``   | Delete a certificate.                                      |
   +--------------+------------------------------------------------------------+
   | ``export``   | Export an X.509 certificate.                               |
   +--------------+------------------------------------------------------------+
   | ``generate`` | Generate a self-signed X.509 certificate.                  |
   +--------------+------------------------------------------------------------+
   | ``import``   | Import an X.509 certificate.                               |
   +--------------+------------------------------------------------------------+
   | ``request``  | Generate a Certificate Signing Request (CSR).              |
   +--------------+------------------------------------------------------------+


ykman piv certificates delete [OPTIONS] SLOT
============================================

Delete a certificate from a PIV slot on the YubiKey.


Arguments
---------

.. table::

   +-----------------------------------+---------------------------------------+
   | Argument                          | Description                           |
   +===================================+=======================================+
   | ``SLOT``                          | PIV slot of the certificate.          |
   +-----------------------------------+---------------------------------------+


Options
-------

.. table::

   +-----------------------------------+---------------------------------------+
   | Option                            | Description                           |
   +===================================+=======================================+
   | ``-h, --help``                    | Show this message and exit.           |
   +-----------------------------------+---------------------------------------+
   | ``-m, --management-key TEXT``     | The management key. TEXT=identifier.  |
   +-----------------------------------+---------------------------------------+
   | ``-P, --pin TEXT``                | PIN code.                             |
   +-----------------------------------+---------------------------------------+



ykman piv certificates export [OPTIONS] SLOT CERTIFICATE
========================================================

Export an X.509 certificate. Reads a certificate from one of the PIV slots on the YubiKey.


Arguments
---------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``SLOT``        | PIV slot of the certificate.                            |
   +-----------------+---------------------------------------------------------+
   | ``CERTIFICATE`` || File to write certificate to. Use ``-`` to             |
   |                 || use ``stdout``.                                        |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +-----------------------------------+---------------------------------------+
   | Option                            | Description                           |
   +===================================+=======================================+
   | ``-h, --help``                    | Show this message and exit.           |
   +-----------------------------------+---------------------------------------+
   | ``-F, --format [PEM|DER]``        | Encoding format.  Default: ``PEM``    |
   +-----------------------------------+---------------------------------------+



ykman piv certificates generate [OPTIONS] SLOT PUBLIC-KEY
=========================================================

Generate a self-signed X.509 certificate. A self-signed certificate is generated and written to one of the slots on the YubiKey. A private key must already be present in the corresponding key slot.


Arguments
---------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``SLOT``        | PIV slot of the certificate.                            |
   +-----------------+---------------------------------------------------------+
   | ``PUBLIC-KEY``  || File containing a public key. Use ``-`` to use         |
   |                 || ``stdin``.                                             |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +---------------------------------+-----------------------------------------+
   | Option                          |     Description                         |
   +=================================+=========================================+
   | ``-h, --help``                  | Show this message and exit.             |
   +---------------------------------+-----------------------------------------+
   || ``-a, --hash-algorithm``       || Hash algorithm. Default: SHA256        |
   || ``[SHA256|SHA384|SHA512]``     || SHA1 deprecated in v5.5.               |
   +---------------------------------+-----------------------------------------+
   | ``-d, --valid-days INTEGER``    || Number of days until the certificate   |
   |                                 || expires. Default: ``365``              |
   +---------------------------------+-----------------------------------------+
   | ``-m, --management-key TEXT``   |The management key. TEXT=identifier.     |
   +---------------------------------+-----------------------------------------+
   | ``-P, --pin TEXT``              | PIN code.                               |
   +---------------------------------+-----------------------------------------+
   | ``-s, --subject TEXT``          || Required. Subject for the certificate, |
   |                                 || as an RFC 4514 string.                 |
   +---------------------------------+-----------------------------------------+


ykman piv certificates import [OPTIONS] SLOT CERTIFICATE
========================================================

Import an X.509 certificate. Write a certificate to one of the PIV slots on the YubiKey.


Arguments
---------

.. table::

   +-----------------+---------------------------------------------------------+
   | Argument        | Description                                             |
   +=================+=========================================================+
   | ``SLOT``        | PIV slot of the certificate.                            |
   +-----------------+---------------------------------------------------------+
   | ``CERTIFICATE`` || File containing the certificate. Use ``-`` to          |
   |                 || use ``stdin``.                                         |
   +-----------------+---------------------------------------------------------+


Options
-------

.. table::

   +-------------------------------+-------------------------------------------+
   | Option                        |     Description                           |
   +===============================+===========================================+
   | ``-h, --help``                | Show this message and exit.               |
   +-------------------------------+-------------------------------------------+
   | ``-c, --compress``            | Compresses the certificate before storing.|
   +-------------------------------+-------------------------------------------+
   | ``-m, --management-key TEXT`` | The management key. TEXT=identifier.      |
   +-------------------------------+-------------------------------------------+
   | ``-p, --password TEXT``       || A password might be needed to decrypt    |
   |                               || the data.                                |
   +-------------------------------+-------------------------------------------+
   | ``-P, --pin TEXT``            | PIN code.                                 |
   +-------------------------------+-------------------------------------------+
   | ``-v, --verify``              || Verify that the certificate matches the  |
   |                               || private key in the slot.                 |
   +-------------------------------+-------------------------------------------+



ykman piv certificates request [OPTIONS] SLOT PUBLIC-KEY CSR
============================================================

Generate a Certificate Signing Request (CSR). A private key must already be present in the corresponding key slot.


Arguments
---------

.. table::

   +----------------+----------------------------------------------------------+
   | Argument       | Description                                              |
   +================+==========================================================+
   | ``CSR``        | File to write CSR to. Use ``-`` to use ``stdout``.       |
   +----------------+----------------------------------------------------------+
   | ``PUBLIC-KEY`` || File containing a public key. Use ``-`` to use          |
   |                || ``stdin``.                                              |
   +----------------+----------------------------------------------------------+
   | ``SLOT``       | PIV slot of the certificate.                             |
   +----------------+----------------------------------------------------------+


Options
-------

.. table::

   +----------------------------------+----------------------------------------+
   | Option                           |     Description                        |
   +==================================+========================================+
   | ``-h, --help``                   | Show this message and exit.            |
   +----------------------------------+----------------------------------------+
   || ``-a, --hash-algorithm``        || Hash algorithm.  Default: SHA256      |
   || ``[SHA256|SHA384|SHA512]``      || SHA1 deprecated in v5.5.              |
   +----------------------------------+----------------------------------------+
   | ``-P, --pin TEXT``               | PIN code.                              |
   +----------------------------------+----------------------------------------+
   | ``-s, --subject TEXT``           || Required. Subject for the requested   |
   |                                  || certificate, as an RFC 4514 string.   |
   +----------------------------------+----------------------------------------+


ykman piv info [OPTIONS]
========================

Display general status of PIV application.


Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+


ykman piv keys [OPTIONS] COMMAND [ARGS]...
==========================================

Manage private keys.


Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+


Commands
--------

.. table::

   +---------------+-----------------------------------------------------------+
   | Command       | Description                                               |
   +===============+===========================================================+
   | ``attest``    | Generate an attestation certificate for a key pair.       |
   +---------------+-----------------------------------------------------------+
   | ``delete``    | Delete a key.                                             |
   +---------------+-----------------------------------------------------------+
   | ``export``    | Export a public key corresponding to a stored private key.|
   +---------------+-----------------------------------------------------------+
   | ``generate``  | Generate an asymmetric key pair.                          |
   +---------------+-----------------------------------------------------------+
   | ``import``    | Import a private key from file.                           |
   +---------------+-----------------------------------------------------------+
   | ``info``      | Show metadata about a private key.                        |
   +---------------+-----------------------------------------------------------+
   | ``move``      | Moves a key.                                              |
   +---------------+-----------------------------------------------------------+



ykman piv keys attest [OPTIONS] SLOT CERTIFICATE
================================================

Generate an attestation certificate for a key pair. Attestation is used to show that an asymmetric key was generated on the YubiKey and therefore does not exist outside the device.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``CERTIFICATE``  || File to write attestation certificate to. Use ``-``   |
   |                  || to use ``stdout``.                                    |
   +------------------+--------------------------------------------------------+
   | ``SLOT``         | PIV slot of the private key.                           |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +----------------------------+----------------------------------------------+
   | Option                     | Description                                  |
   +============================+==============================================+
   | ``-h, --help``             | Show this message and exit.                  |
   +----------------------------+----------------------------------------------+
   | ``-F, --format [PEM|DER]`` | Encoding format.  Default: ``PEM``           |
   +----------------------------+----------------------------------------------+


ykman piv keys delete [OPTIONS] SLOT
=====================================

Delete a key from a PIV slot on the YubiKey.

Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``SLOT``         | PIV slot of the key.                                   |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +-------------------------------+-------------------------------------------+
   | Option                        | Description                               |
   +===============================+===========================================+
   | ``-h, --help``                | Show this message and exit.               |
   +-------------------------------+-------------------------------------------+
   | ``-m, --management-key TEXT`` | The management key. TEXT=identifier.      |
   +-------------------------------+-------------------------------------------+
   | ``-P, --pin TEXT``            | PIN code.                                 |
   +-------------------------------+-------------------------------------------+


ykman piv keys export [OPTIONS] SLOT PUBLIC-KEY
================================================

Export a public key corresponding to a stored private key. 

This command uses several different mechanisms for exporting the public key corresponding to a stored private key, which might fail. If a certificate is stored in the slot it is assumed to contain the correct public key. If this is not the case, the wrong public key is returned. 

Use the ``--verify`` flag to verify that the public key being returned matches the private key, by using the slot to create and verify a signature. This might require the PIN be provided.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``PUBLIC-KEY``   || File containing the generated public key. Use ``-``   |
   |                  || to use ``stdout``.                                    |
   +------------------+--------------------------------------------------------+
   | ``SLOT``         | PIV slot of the private key.                           |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +----------------------------+----------------------------------------------+
   | Option                     | Description                                  |
   +============================+==============================================+
   | ``-h, --help``             | Show this message and exit.                  |
   +----------------------------+----------------------------------------------+
   | ``-F, --format [PEM|DER]`` | Encoding format.  Default: ``PEM``           |
   +----------------------------+----------------------------------------------+
   | ``-P, --pin TEXT``         || PIN code. Used with ``--verify``.           |
   +----------------------------+----------------------------------------------+
   | ``-v, --verify``           || Verify that the public key matches the      |
   |                            || private key in the slot.                    |
   +----------------------------+----------------------------------------------+


ykman piv keys generate [OPTIONS] SLOT PUBLIC-KEY
=================================================

Generate an asymmetric key pair. The private key is generated on the YubiKey and written to one of the slots.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``PUBLIC-KEY``   || File containing the generated public key. Use ``-``   |
   |                  || to use ``stdout``.                                    |
   +------------------+--------------------------------------------------------+
   | ``SLOT``         | PIV slot of the private key.                           |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +-------------------------------+-------------------------------------------+
   | Option                        | Description                               |
   +===============================+===========================================+
   | ``-h, --help``                | Show this message and exit.               |
   +-------------------------------+-------------------------------------------+
   || ``-a, --algorithm [RSA1024`` || Algorithm to use in key generation.      |
   || ``|RSA2048|RSA3072|RSA4096`` || Default: ``RSA2048``                     |
   || ``ECCP256|ECCP384|ED25519``  ||                                          |
   || ``X25519]``                  ||                                          |
   +-------------------------------+-------------------------------------------+
   | ``-F, --format [PEM|DER]``    | Encoding format.  Default: ``PEM``        |
   +-------------------------------+-------------------------------------------+
   | ``-m, --management-key TEXT`` | The management key. TEXT=identifier.      |
   +-------------------------------+-------------------------------------------+
   | ``-P, --pin TEXT``            | PIN code.                                 |
   +-------------------------------+-------------------------------------------+
   || ``--pin-policy [DEFAULT``    | PIN policy for slot.                      |
   || ``|NEVER|ONCE|ALWAYS``       |                                           |
   || ``|MATCH-ONCE|MATCH-ALWAYS]``|                                           |
   +-------------------------------+-------------------------------------------+
   || ``--touch-policy [DEFAULT``  | Touch policy for slot.                    |
   || ``|NEVER|ALWAYS|CACHED]``    |                                           |
   +-------------------------------+-------------------------------------------+


ykman piv keys import [OPTIONS] SLOT PRIVATE-KEY
================================================

Import a private key from file. Write a private key to one of the PIV slots on the YubiKey.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``PRIVATE-KEY``  || File containing the private key. Use ``-`` to use     |
   |                  || ``stdin``.                                            |
   +------------------+--------------------------------------------------------+
   | ``SLOT``         | PIV slot of the private key.                           |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +----------------------------------+----------------------------------------+
   | Option                           | Description                            |
   +==================================+========================================+
   | ``-h, --help``                   | Show this message and exit.            |
   +----------------------------------+----------------------------------------+
   | ``-m, --management-key TEXT``    | The management key. TEXT=identifier.   |
   +----------------------------------+----------------------------------------+
   || ``--pin-policy [DEFAULT|NEVER`` | PIN policy for slot.                   |
   || ``ONCE|ALWAYS|MATCH-ONCE``      |                                        |
   || ``MATCH-ALWAYS]``               |                                        |
   +----------------------------------+----------------------------------------+
   | ``-p, --password TEXT``          || Password used to decrypt the private  |
   |                                  || key.                                  |
   +----------------------------------+----------------------------------------+
   | ``-P, --pin TEXT``               | PIN code.                              |
   +----------------------------------+----------------------------------------+
   || ``--touch-policy [DEFAULT|``    | Touch policy for slot.                 |
   || ``NEVER|ALWAYS|CACHED]``        |                                        |
   +----------------------------------+----------------------------------------+



ykman piv keys info [OPTIONS] SLOT
===================================

Show metadata about a private key. This shows:

* what type of key is stored in a specific slot
* whether the key was imported into the YubiKey or generated on-chip
* the PIN and Touch policies for using the key

Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``SLOT``         | PIV slot of the private key.                           |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +----------------------------------+----------------------------------------+
   | Option                           | Description                            |
   +==================================+========================================+
   | ``-h, --help``                   | Show this message and exit.            |
   +----------------------------------+----------------------------------------+


ykman piv keys move [OPTIONS] SOURCE DEST
==========================================

Moves a key from one PIV slot into another.

Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``SOURCE``       | PIV slot of the key to move.                           |
   +------------------+--------------------------------------------------------+
   | ``DEST``         | PIV slot to move the key into.                         |
   +------------------+--------------------------------------------------------+

Options
-------

.. table::

   +----------------------------------+----------------------------------------+
   | Option                           | Description                            |
   +==================================+========================================+
   | ``-h, --help``                   | Show this message and exit.            |
   +----------------------------------+----------------------------------------+
   | ``-m, --management-key TEXT``    | The management key. TEXT=identifier.   |
   +----------------------------------+----------------------------------------+
   | ``-P, --pin TEXT``               | PIN code.                              |
   +----------------------------------+----------------------------------------+


ykman piv objects [OPTIONS] COMMAND [ARGS]...
=============================================

Manage PIV data objects.


Examples
---------

**Write** the contents of a file to data object with ID: ``abc123``

.. code-block::

   $ ykman piv objects import abc123 myfile.txt

**Read** into a file, the contents of the data object with ID: ``abc123``

.. code-block::

   $ ykman piv objects export abc123 myfile.txt

**Generate** a random value for CHUID:

.. code-block::

   $ ykman piv objects generate chuid


Options
-------

.. table::

   +----------------------------------+----------------------------------------+
   | Option                           | Description                            |
   +==================================+========================================+
   | ``-h, --help``                   | Show this message and exit.            |
   +----------------------------------+----------------------------------------+


Commands
---------

.. table::

   +------------------+--------------------------------------------------------+
   | Command          | Description                                            |
   +==================+========================================================+
   | ``export``       | Export an arbitrary PIV data object.                   |
   +------------------+--------------------------------------------------------+
   | ``generate``     | Generate and write data for a supported data object.   |
   +------------------+--------------------------------------------------------+
   | ``import``       | Write an arbitrary PIV object.                         |
   +------------------+--------------------------------------------------------+



ykman piv objects export [OPTIONS] OBJECT OUTPUT
================================================

Export an arbitrary PIV data object.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``OBJECT``       | Name of PIV data object or ID in HEX.                  |
   +------------------+--------------------------------------------------------+
   | ``OUTPUT``       | File to write object to. Use ``-`` to use ``stdout``.  |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +----------------------------+----------------------------------------------+
   | Option                     | Description                                  |
   +============================+==============================================+
   | ``-h, --help``             | Show this message and exit.                  |
   +----------------------------+----------------------------------------------+
   | ``-P, --pin TEXT``         | PIN code.                                    |
   +----------------------------+----------------------------------------------+



ykman piv objects generate [OPTIONS] OBJECT
===========================================

Generate and write data for a supported data object.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``OBJECT``       || Name of PIV data object or ID in HEX.                 |
   |                  || Supported data objects are:                           |
   |                  ||  ``CHUID`` (Card Holder Unique ID)                    |
   |                  ||  ``CCC`` (Card Capability Container)                  |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +--------------------------------+------------------------------------------+
   | Option                         | Description                              |
   +================================+==========================================+
   | ``-h, --help``                 | Show this message and exit.              |
   +--------------------------------+------------------------------------------+
   | ``-m, --management-key TEXT``  | The management key. TEXT=identifier.     |
   +--------------------------------+------------------------------------------+
   | ``-P, --pin TEXT``             | PIN code.                                |
   +--------------------------------+------------------------------------------+




ykman piv objects import [OPTIONS] OBJECT DATA
==============================================

Write an arbitrary PIV object. Write a PIV object by providing the object ID. Yubico writable PIV objects are available in the range 5f0000 - 5fffff.


Arguments
----------

.. table::

   +------------------+--------------------------------------------------------+
   | Argument         | Description                                            |
   +==================+========================================================+
   | ``DATA``         || File containing the data to be written. Use ``-`` to  |
   |                  || use ``stdin``.                                        |
   +------------------+--------------------------------------------------------+
   | ``OBJECT``       | Name of PIV data object or ID in HEX.                  |
   +------------------+--------------------------------------------------------+


Options
-------

.. table::

   +--------------------------------+------------------------------------------+
   | Option                         | Description                              |
   +================================+==========================================+
   | ``-h, --help``                 | Show this message and exit.              |
   +--------------------------------+------------------------------------------+
   | ``-m, --management-key TEXT``  | The management key. TEXT = identifier.   |
   +--------------------------------+------------------------------------------+
   | ``-P, --pin TEXT``             | PIN code.                                |
   +--------------------------------+------------------------------------------+



ykman piv reset [OPTIONS]
=========================

Reset all PIV data. This action wipes all data and restores factory settings for the PIV application on your YubiKey.

This option is not available in ykman CLI version 5.4.0.

Options
-------

.. table::

   +-----------------------+---------------------------------------------------+
   | Option                | Description                                       |
   +=======================+===================================================+
   | ``-h, --help``        | Show this message and exit.                       |
   +-----------------------+---------------------------------------------------+
   | ``-f, --force``       | Confirm the action without prompting.             |
   +-----------------------+---------------------------------------------------+




----

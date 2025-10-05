here are some example outputs from ykman

git:(main) ✗ ykman info
ERROR: Multiple YubiKeys detected. Use --device SERIAL to specify which one to use.


git:(main) ✗ ykman list
YubiKey 5 NFC (5.2.7) [OTP+FIDO+CCID] Serial: 16021303
YubiKey 5 NFC (5.4.3) [OTP+FIDO+CCID] Serial: 9681620


git:(main) ✗ ykman --device 16021303 info
Device type: YubiKey 5 NFC
Serial number: 16021303
Firmware version: 5.2.7
Form factor: Keychain (USB-A)
Enabled USB interfaces: OTP, FIDO, CCID
NFC transport is enabled

Applications    USB             NFC          
Yubico OTP      Enabled         Enabled
FIDO U2F        Enabled         Enabled
FIDO2           Enabled         Enabled
OATH            Enabled         Enabled
PIV             Enabled         Enabled
OpenPGP         Enabled         Enabled
YubiHSM Auth    Not available   Not available


ykman config
Usage: ykman config [OPTIONS] COMMAND [ARGS]...

  Configure the YubiKey, enable or disable applications.

  The applications may be enabled and disabled independently over
  different transports (USB and NFC). The configuration may also
  be protected by a lock code.

  Examples:

    Disable PIV over NFC:
    $ ykman config nfc --disable PIV

    Enable all applications over USB:
    $ ykman config usb --enable-all

    Generate and set a random application lock code:
    $ ykman config set-lock-code --generate

Options:
  -h, --help  show this message and exit

Commands:
  mode           manage connection modes (USB Interfaces)
  nfc            enable or disable applications over NFC
  reset          reset all YubiKey data
  set-lock-code  set or change the configuration lock code
  usb            enable or disable applications over USB


✗ ykman fido
Usage: ykman fido [OPTIONS] COMMAND [ARGS]...

  Manage the FIDO applications.

  Examples:

    Reset the FIDO (FIDO2 and U2F) applications:
    $ ykman fido reset

    Change the FIDO2 PIN from 123456 to 654321:
    $ ykman fido access change-pin --pin 123456 --new-pin 654321

Options:
  -h, --help  show this message and exit

Commands:
  info          display general status of the FIDO2 application
  reset         reset all FIDO applications
  access        manage the PIN for FIDO
  config        manage FIDO configuration
  credentials   manage discoverable (resident) credentials
  fingerprints  manage fingerprints


ykman oath
Usage: ykman oath [OPTIONS] COMMAND [ARGS]...

  Manage the OATH application.

  Examples:

    Generate codes for accounts starting with 'yubi':
    $ ykman oath accounts code yubi

    Add an account with the secret key f5up4ub3dw and the name yubico,
    which requires touch:
    $ ykman oath accounts add yubico f5up4ub3dw --touch

    Set a password for the OATH application:
    $ ykman oath access change

Options:
  -h, --help  show this message and exit

Commands:
  info      display general status of the OATH application
  reset     reset all OATH data
  access    manage password protection for OATH
  accounts  manage and use OATH accounts


git:(main) ✗ ykman openpgp
Usage: ykman openpgp [OPTIONS] COMMAND [ARGS]...

  Manage the OpenPGP application.

  Examples:

    Set the retries for PIN, Reset Code and Admin PIN to 10:
    $ ykman openpgp access set-retries 10 10 10

    Require touch to use the authentication key:
    $ ykman openpgp keys set-touch aut on

Options:
  -h, --help  show this message and exit

Commands:
  info          display general status of the OpenPGP
  reset         reset all OpenPGP data
  access        manage PIN, Reset Code, and Admin PIN
  certificates  manage certificates
  keys          manage private keys


ykman otp
Usage: ykman otp [OPTIONS] COMMAND [ARGS]...

  Manage the YubiOTP application.

  The YubiKey provides two keyboard-based slots which can each be
  configured with a credential. Several credential types are
  supported.

  A slot configuration may be write-protected with an access code.
  This prevents the configuration to be overwritten without the
  access code provided. Mode switching the YubiKey is not possible
  when a slot is configured with an access code. To provide an
  access code to commands which require it, use the --access-code
  option. Note that this option must be given directly after the
  "otp" command, before any sub-command.

  Examples:

    Swap the configurations between the two slots:
    $ ykman otp swap

    Program a random challenge-response credential to slot 2:
    $ ykman otp chalresp --generate 2

    Program a Yubico OTP credential to slot 1, using the serial as public id:
    $ ykman otp yubiotp 1 --serial-public-id

    Program a random 38 characters long static password to slot 2:
    $ ykman otp static --generate 2 --length 38

    Remove a currently set access code from slot 2):
    $ ykman otp --access-code 0123456789ab settings 2 --delete-access-code

Options:
  --access-code HEX  6 byte access code (use "-" as a value to
                     prompt for input)
  -h, --help         show this message and exit

Commands:
  calculate  perform a challenge-response operation
  chalresp   program a challenge-response credential
  delete     deletes the configuration stored in a slot
  hotp       program an HMAC-SHA1 OATH-HOTP credential
  info       display general status of the YubiKey OTP slots
  ndef       configure a slot to be used over NDEF (NFC)
  settings   update the settings for a slot
  static     configure a static password
  swap       swaps the two slot configurations
  yubiotp    program a Yubico OTP credential


ykman piv
Usage: ykman piv [OPTIONS] COMMAND [ARGS]...

  Manage the PIV application.

  Examples:

    Generate an ECC P-256 private key and a self-signed certificate in
    slot 9a:
    $ ykman piv keys generate --algorithm ECCP256 9a pubkey.pem
    $ ykman piv certificates generate --subject "CN=yubico" 9a pubkey.pem

    Change the PIN from 123456 to 654321:
    $ ykman piv access change-pin --pin 123456 --new-pin 654321

    Reset all PIV data and restore default settings:
    $ ykman piv reset

Options:
  -h, --help  show this message and exit

Commands:
  info          display general status of the PIV application
  reset         reset all PIV data
  access        manage PIN, PUK, and Management Key
  certificates  manage certificates
  keys          manage private keys
  objects       manage PIV data objects

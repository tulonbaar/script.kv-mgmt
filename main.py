import sys
import os
import shutil
from datetime import datetime
from colorama import init, Fore, Style
from src import get, create, delete, edit, auth

# Initialize colorama
init(autoreset=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    print(Fore.CYAN + Style.BRIGHT + f"\n--- {text} ---" + Style.RESET_ALL)

def pause():
    input(Fore.YELLOW + "\nPress Enter to continue..." + Style.RESET_ALL)

def input_with_esc(prompt):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    buffer = []
    
    if os.name == 'nt':
        import msvcrt
        while True:
            ch = msvcrt.getch()
            if ch == b'\x1b': # Esc
                print('')
                return None
            elif ch == b'\r': # Enter
                print('')
                return ''.join(buffer)
            elif ch == b'\x08': # Backspace
                if buffer:
                    buffer.pop()
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                try:
                    char = ch.decode('utf-8')
                    buffer.append(char)
                    sys.stdout.write(char)
                    sys.stdout.flush()
                except:
                    pass
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                ch = sys.stdin.read(1)
                if ord(ch) == 27: # Esc
                    print('')
                    return None
                elif ord(ch) == 10: # Enter
                    print('')
                    return ''.join(buffer)
                elif ord(ch) == 127: # Backspace
                    if buffer:
                        buffer.pop()
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                else:
                    buffer.append(ch)
                    sys.stdout.write(ch)
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def get_input_with_list(prompt, item_type):
    """
    Displays a prompt on the left and a list of items on the right.
    item_type: 'key', 'secret', 'certificate'
    """
    items = []
    header = ""
    if item_type == 'key':
        items = get.get_all_keys()
        header = "Available Keys"
    elif item_type == 'secret':
        items = get.get_all_secrets()
        header = "Available Secrets"
    elif item_type == 'certificate':
        items = get.get_all_certificates()
        header = "Available Certificates"
    
    item_names = [item.name for item in items]
    
    # Get terminal size
    columns, lines = shutil.get_terminal_size()
    
    # Calculate layout
    # We want to print the list on the right side.
    # Let's say right column takes 1/3 of screen or fixed width.
    # Fixed width of 40 chars seems reasonable for names.
    sidebar_width = 40
    main_width = columns - sidebar_width - 5 # 5 for padding/separator
    
    if main_width < 20: # Fallback for small screens
        print(Fore.MAGENTA + f"\n--- {header} ---" + Style.RESET_ALL)
        for name in item_names:
            print(f"- {name}")
        print("-" * 20)
        print(Fore.YELLOW + "(Press Esc to go back)" + Style.RESET_ALL)
        val = input_with_esc(prompt)
        if val is None:
            return None
        return val

    # Prepare sidebar lines
    sidebar_lines = [Fore.MAGENTA + f"--- {header} ---" + Style.RESET_ALL]
    for name in item_names:
        sidebar_lines.append(f"- {name}")
    
    # We need to clear screen to draw this properly? 
    # Or just print it below the current menu.
    # The prompt usually comes after some menu text.
    # To make it look "right side", we should probably reprint the screen or just print the list.
    # But the user asked for "right side".
    # Let's try to print the list aligned to the right, starting from current line?
    # No, we can't move cursor up easily without curses.
    
    # Strategy: Clear screen, reprint a simple header/instruction, then the split view.
    clear_screen()
    print_header(f"Select {item_type.capitalize()}")
    
    # Content for main area (left)
    main_lines = [
        f"Please enter the name of the {item_type}.",
        "You can see the available items on the right.",
        "",
        prompt
    ]
    
    max_lines = max(len(main_lines), len(sidebar_lines))
    
    print("\n")
    for i in range(max_lines):
        left = main_lines[i] if i < len(main_lines) else ""
        right = sidebar_lines[i] if i < len(sidebar_lines) else ""
        
        # Strip ansi codes for length calculation (simplified, assuming no ansi in left for now except prompt)
        # Actually prompt might have color.
        # Let's just pad spaces.
        
        padding = " " * (main_width - len(left)) # This is naive if left has colors
        # Better: use f-string with width, but color codes mess up length.
        # Let's just print right aligned.
        
        # Construct the line
        # We need to move cursor to the right column.
        # Or just print padding.
        
        # Simple approach:
        # Left content | Right content
        
        # Since 'left' might contain the prompt which we want to be the last thing,
        # we can't print the prompt line here if we want `input()` to be at the end.
        # `input()` must be the last call.
        
        # So we print everything EXCEPT the prompt line.
        pass

    # Revised Strategy:
    # Print the list on the right side of the screen, line by line.
    # Then print the prompt at the bottom.
    
    # Header
    print(f"{' ':<{main_width}} | {Fore.MAGENTA}{header}{Style.RESET_ALL}")
    print(f"{' ':<{main_width}} | {'-'*20}")
    
    for name in item_names:
        print(f"{' ':<{main_width}} | {name}")
    
    print("\n" + "-" * columns)
    print(Fore.YELLOW + "(Press Esc to go back)" + Style.RESET_ALL)
    val = input_with_esc(prompt)
    if val is None:
        return None
    return val

def main_menu():
    while True:
        clear_screen()
        print_header("Azure Key Vault Management")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "List Items")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Create Item")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Delete Item")
        print(Fore.GREEN + "4. " + Style.RESET_ALL + "Edit Item")
        print(Fore.GREEN + "5. " + Style.RESET_ALL + "Version Management")
        print(Fore.RED + "0. " + Style.RESET_ALL + "Exit")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            list_menu()
        elif choice == '2':
            create_menu()
        elif choice == '3':
            delete_menu()
        elif choice == '4':
            edit_menu()
        elif choice == '5':
            version_menu()
        elif choice == '0':
            print(Fore.MAGENTA + "Exiting..." + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)
            pause()

def version_menu():
    while True:
        clear_screen()
        print_header("Version Management")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "Key Versions")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Secret Versions")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Certificate Versions")
        print(Fore.YELLOW + "0. " + Style.RESET_ALL + "Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            manage_key_versions()
        elif choice == '2':
            manage_secret_versions()
        elif choice == '3':
            manage_certificate_versions()
        elif choice == '0':
            return
        else:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            pause()

def manage_key_versions():
    name = get_input_with_list("Enter key name: ", 'key')
    if not name: return
    while True:
        clear_screen()
        print_header(f"Versions for Key: {name}")
        versions = get.list_key_versions(name)
        
        print(Fore.GREEN + "\nActions:" + Style.RESET_ALL)
        print("1. Enable/Disable Version")
        print("2. Create New Version (Rotate)")
        print("3. Disable all but newest one")
        print("0. Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            if not versions:
                print("No versions to manage.")
                pause()
                continue
            try:
                idx = int(input("Enter version index (from list above): ")) - 1
                if 0 <= idx < len(versions):
                    version = versions[idx]
                    print(f"Selected Version: {version.version}")
                    enabled_input = input(f"Enable version? (current: {version.enabled}) (y/n): ")
                    if enabled_input.lower() == 'y':
                        edit.update_key_version_properties(name, version.version, True)
                    elif enabled_input.lower() == 'n':
                        edit.update_key_version_properties(name, version.version, False)
                    pause()
                else:
                    print("Invalid index.")
                    pause()
            except ValueError:
                print("Invalid input.")
                pause()
        elif choice == '2':
            print("Creating new version (Rotation)...")
            # Re-use create logic but maybe simplified or just call create_key
            # For simplicity, let's just call create_key with default or ask for params?
            # Usually rotation implies keeping same params but new key material.
            # Let's ask for basic/advanced again or just basic.
            # For now, let's just call create.create_key(name) which creates a new version.
            create.create_key(name)
            pause()
        elif choice == '3':
            edit.disable_all_but_newest_key_version(name)
            pause()
        elif choice == '0':
            break

def manage_secret_versions():
    name = get_input_with_list("Enter secret name: ", 'secret')
    if not name: return
    while True:
        clear_screen()
        print_header(f"Versions for Secret: {name}")
        versions = get.list_secret_versions(name)
        
        print(Fore.GREEN + "\nActions:" + Style.RESET_ALL)
        print("1. Enable/Disable Version")
        print("2. Create New Version (Set Value)")
        print("3. Disable all but newest one")
        print("0. Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            if not versions:
                print("No versions to manage.")
                pause()
                continue
            try:
                idx = int(input("Enter version index (from list above): ")) - 1
                if 0 <= idx < len(versions):
                    version = versions[idx]
                    print(f"Selected Version: {version.version}")
                    enabled_input = input(f"Enable version? (current: {version.enabled}) (y/n): ")
                    if enabled_input.lower() == 'y':
                        edit.update_secret_version_properties(name, version.version, True)
                    elif enabled_input.lower() == 'n':
                        edit.update_secret_version_properties(name, version.version, False)
                    pause()
                else:
                    print("Invalid index.")
                    pause()
            except ValueError:
                print("Invalid input.")
                pause()
        elif choice == '2':
            value = input("Enter new secret value: ")
            create.create_secret(name, value)
            pause()
        elif choice == '3':
            edit.disable_all_but_newest_secret_version(name)
            pause()
        elif choice == '0':
            break

def manage_certificate_versions():
    name = get_input_with_list("Enter certificate name: ", 'certificate')
    if not name: return
    while True:
        clear_screen()
        print_header(f"Versions for Certificate: {name}")
        versions = get.list_certificate_versions(name)
        
        print(Fore.GREEN + "\nActions:" + Style.RESET_ALL)
        print("1. Enable/Disable Version")
        print("2. Create New Version (Renew)")
        print("3. Disable all but newest one")
        print("0. Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            if not versions:
                print("No versions to manage.")
                pause()
                continue
            try:
                idx = int(input("Enter version index (from list above): ")) - 1
                if 0 <= idx < len(versions):
                    version = versions[idx]
                    print(f"Selected Version: {version.version}")
                    enabled_input = input(f"Enable version? (current: {version.enabled}) (y/n): ")
                    if enabled_input.lower() == 'y':
                        edit.update_certificate_version_properties(name, version.version, True)
                    elif enabled_input.lower() == 'n':
                        edit.update_certificate_version_properties(name, version.version, False)
                    pause()
                else:
                    print("Invalid index.")
                    pause()
            except ValueError:
                print("Invalid input.")
                pause()
        elif choice == '2':
            subject = input("Enter subject name for renewal (e.g. mycert): ")
            create.create_certificate(name, subject)
            pause()
        elif choice == '3':
            edit.disable_all_but_newest_certificate_version(name)
            pause()
        elif choice == '0':
            break

def list_menu():
    while True:
        clear_screen()
        print_header("List Items")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "List Keys")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "List Secrets")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "List Certificates")
        print(Fore.YELLOW + "0. " + Style.RESET_ALL + "Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            get.list_keys()
            pause()
        elif choice == '2':
            get.list_secrets()
            pause()
        elif choice == '3':
            get.list_certificates()
            pause()
        elif choice == '0':
            return
        else:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            pause()

def create_menu():
    while True:
        clear_screen()
        print_header("Create Item")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "Create Key")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Create Secret")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Create Certificate")
        print(Fore.YELLOW + "0. " + Style.RESET_ALL + "Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            name = input("Enter key name: ")
            print(Fore.CYAN + "\nKey Creation Mode:" + Style.RESET_ALL)
            print("1. Basic (RSA, Default)")
            print("2. Advanced (Custom Type, Size, Dates)")
            mode = input("Select mode (1/2): ")
            
            if mode == '2':
                # Advanced
                kty_input = input("Key Type (RSA/EC) [RSA]: ").upper()
                kty = kty_input if kty_input in ['RSA', 'EC'] else 'RSA'
                
                size = None
                curve = None
                
                if kty == 'RSA':
                    size_input = input("Key Size (2048/3072/4096) [2048]: ")
                    size = int(size_input) if size_input.isdigit() else 2048
                else:
                    curve_input = input("Curve (P-256/P-384/P-521/P-256K) [P-256]: ")
                    curve = curve_input if curve_input else 'P-256'
                
                not_before = None
                nb_input = input("Activation Date (YYYY-MM-DD) [None]: ")
                if nb_input:
                    try:
                        not_before = datetime.strptime(nb_input, "%Y-%m-%d")
                    except ValueError:
                        print(Fore.RED + "Invalid date format. Skipping." + Style.RESET_ALL)

                expires_on = None
                exp_input = input("Expiration Date (YYYY-MM-DD) [None]: ")
                if exp_input:
                    try:
                        expires_on = datetime.strptime(exp_input, "%Y-%m-%d")
                    except ValueError:
                        print(Fore.RED + "Invalid date format. Skipping." + Style.RESET_ALL)

                create.create_key(name, kty=kty, size=size, curve=curve, not_before=not_before, expires_on=expires_on)
            else:
                # Basic
                create.create_key(name)
            pause()
        elif choice == '2':
            name = input("Enter secret name: ")
            value = input("Enter secret value: ")
            create.create_secret(name, value)
            pause()
        elif choice == '3':
            name = input("Enter certificate name: ")
            subject = input("Enter subject name (e.g. mycert): ")
            create.create_certificate(name, subject)
            pause()
        elif choice == '0':
            return
        else:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            pause()

def delete_menu():
    while True:
        clear_screen()
        print_header("Delete Item")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "Delete Key")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Delete Secret")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Delete Certificate")
        print(Fore.YELLOW + "0. " + Style.RESET_ALL + "Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            name = get_input_with_list("Enter key name: ", 'key')
            if name:
                delete.delete_key(name)
                pause()
        elif choice == '2':
            name = get_input_with_list("Enter secret name: ", 'secret')
            if name:
                delete.delete_secret(name)
                pause()
        elif choice == '3':
            name = get_input_with_list("Enter certificate name: ", 'certificate')
            if name:
                delete.delete_certificate(name)
                pause()
        elif choice == '0':
            return
        else:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            pause()

def edit_menu():
    while True:
        clear_screen()
        print_header("Edit Item")
        print(Fore.GREEN + "1. " + Style.RESET_ALL + "Key: Update Properties (Enable, Ops, Dates)")
        print(Fore.GREEN + "2. " + Style.RESET_ALL + "Key: Add/Update Tags")
        print(Fore.GREEN + "3. " + Style.RESET_ALL + "Secret: Update Value")
        print(Fore.GREEN + "4. " + Style.RESET_ALL + "Secret: Add/Update Tags")
        print(Fore.GREEN + "5. " + Style.RESET_ALL + "Certificate: Add/Update Tags")
        print(Fore.YELLOW + "0. " + Style.RESET_ALL + "Back")
        
        choice = input(Fore.BLUE + "\nSelect an option: " + Style.RESET_ALL)
        
        if choice == '1':
            name = get_input_with_list("Enter key name: ", 'key')
            if not name: continue
            
            # Fetch key to check type
            key = get.get_key(name)
            if not key:
                pause()
                continue
            
            kty = key.key_type
            print(f"Key Type: {kty}")

            # Enabled
            enabled = None
            enabled_input = input("Change enabled status? (y/n/skip) [skip]: ")
            if enabled_input.lower() == 'y':
                enabled = True
            elif enabled_input.lower() == 'n':
                enabled = False
            
            # Key Ops
            key_ops = None
            ops_input = input("Update permitted operations? (y/n) [n]: ")
            if ops_input.lower() == 'y':
                print("Select operations (comma separated):")
                
                ops_map = {}
                if kty in ['RSA', 'RSA-HSM']:
                    print("1. encrypt")
                    print("2. decrypt")
                    print("3. sign")
                    print("4. verify")
                    print("5. wrapKey")
                    print("6. unwrapKey")
                    ops_map = {
                        '1': 'encrypt', '2': 'decrypt', '3': 'sign', 
                        '4': 'verify', '5': 'wrapKey', '6': 'unwrapKey'
                    }
                elif kty in ['EC', 'EC-HSM']:
                    print("1. sign")
                    print("2. verify")
                    ops_map = {
                        '1': 'sign', '2': 'verify'
                    }
                else:
                    print("Unknown key type, showing all options.")
                    print("1. encrypt")
                    print("2. decrypt")
                    print("3. sign")
                    print("4. verify")
                    print("5. wrapKey")
                    print("6. unwrapKey")
                    ops_map = {
                        '1': 'encrypt', '2': 'decrypt', '3': 'sign', 
                        '4': 'verify', '5': 'wrapKey', '6': 'unwrapKey'
                    }

                ops_selection = input("Selection: ")
                selected_ops = []
                for op in ops_selection.split(','):
                    op = op.strip()
                    if op in ops_map:
                        selected_ops.append(ops_map[op])
                if selected_ops:
                    key_ops = selected_ops

            # Dates
            not_before = None
            nb_input = input("Update Activation Date (YYYY-MM-DD) [skip]: ")
            if nb_input:
                try:
                    not_before = datetime.strptime(nb_input, "%Y-%m-%d")
                except ValueError:
                    print(Fore.RED + "Invalid date format. Skipping." + Style.RESET_ALL)

            expires_on = None
            exp_input = input("Update Expiration Date (YYYY-MM-DD) [skip]: ")
            if exp_input:
                try:
                    expires_on = datetime.strptime(exp_input, "%Y-%m-%d")
                except ValueError:
                    print(Fore.RED + "Invalid date format. Skipping." + Style.RESET_ALL)

            edit.update_key_properties(name, enabled=enabled, key_ops=key_ops, not_before=not_before, expires_on=expires_on)
            pause()
        elif choice == '2':
            name = get_input_with_list("Enter key name: ", 'key')
            if not name: continue
            tag_key = input("Enter tag key: ")
            tag_value = input("Enter tag value: ")
            edit.update_key_tags(name, {tag_key: tag_value})
            pause()
        elif choice == '3':
            name = get_input_with_list("Enter secret name: ", 'secret')
            if not name: continue
            value = input("Enter new secret value: ")
            edit.update_secret_value(name, value)
            pause()
        elif choice == '4':
            name = get_input_with_list("Enter secret name: ", 'secret')
            if not name: continue
            tag_key = input("Enter tag key: ")
            tag_value = input("Enter tag value: ")
            edit.update_secret_tags(name, {tag_key: tag_value})
            pause()
        elif choice == '5':
            name = get_input_with_list("Enter certificate name: ", 'certificate')
            if not name: continue
            tag_key = input("Enter tag key: ")
            tag_value = input("Enter tag value: ")
            edit.update_certificate_tags(name, {tag_key: tag_value})
            pause()
        elif choice == '0':
            return
        else:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            pause()

if __name__ == "__main__":
    try:
        print("Initializing authentication...")
        auth.validate_connection()
    except Exception:
        print(Fore.RED + "Authentication failed. Exiting." + Style.RESET_ALL)
        sys.exit(1)
    main_menu()

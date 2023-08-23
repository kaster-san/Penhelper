
from ftplib import FTP
import telnetlib3
from smbprotocol.connection import Connection



def connect_ftp(ip_address, port):
    try:
        with FTP() as ftp:
            ftp.connect(ip_address, port)
            ftp.login()
            
            server_info = ftp.getwelcome()  # Get server information
            print(f"Server Information for FTP server ({ip_address}:{port}):")
            print(server_info)
            
            # Get the list of files in the FTP root directory
            file_list = ftp.nlst()
            print(f"\nList of files in FTP server ({ip_address}:{port}):")
            for file in file_list:
                print(file)
            
            # Download each file from the server
            for remote_filename in file_list:
                local_filename = "downloaded_" + remote_filename  # Adjust the local file name if needed
                
                try:
                    with open(local_filename, "wb") as local_file:
                        ftp.retrbinary("RETR " + remote_filename, local_file.write)
                        print(f"\nFile '{remote_filename}' downloaded and saved as '{local_filename}'")
                except Exception as download_error:
                    print(f"\nError downloading file '{remote_filename}': {download_error}")
            
            ftp.quit()
            return True
    except Exception as e:
        return False
def connect_telnet(ip_address, port):
    try:
        conn = telnetlib3.open_connection(ip_address, port)
        conn.wait_for_close()
        return True
    except Exception as e:
        return False
def connect_smb(ip_address, port):
    try:
        # Créer une instance de SMBConnection
        smb_connection = Connection('username', 'password', 'client_name', 'server_name', use_ntlm_v2=True)

        # Se connecter au serveur SMB
        if smb_connection.connect(ip_address, port):
            print(f"SMB connection succeeded for {ip_address}:{port}")

            # Exemple : Lister les fichiers dans un répertoire partagé
            share_name = 'ShareName'
            directory = '\\'
            file_list = smb_connection.listPath(share_name, directory)

            print(f"List of files in SMB share {share_name} on {ip_address}:{port}:")
            for file_info in file_list:
                print(file_info.filename)
 # Se déconnecter du serveur SMB
            smb_connection.close()
            return True
        else:
            print(f"SMB connection failed for {ip_address}:{port}")
            return False
    except Exception as e:
        print(f"Error during SMB connection for {ip_address}:{port}: {str(e)}")
        return False
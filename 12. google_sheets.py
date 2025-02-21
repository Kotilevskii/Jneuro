"""
SPECIFICATION

Purpose:
The script handles interaction with Google Sheets API for creating and managing spreadsheets.

Features:
1. Spreadsheet Creation:
   - Creates new Google Sheets
   - Sets up initial formatting
   - Handles data insertion

2. Permission Management:
   - Sets up access rights for files
   - Manages public and user-specific permissions
   - Configures sharing settings

3. File Organization:
   - Moves files to specified folders
   - Manages file hierarchy
   - Maintains proper file structure

4. Error Handling:
   - Comprehensive logging system
   - Detailed error tracking
   - Operation status monitoring

Input Format:
- Template data with sheet content
- Configuration parameters
- Access credentials

Output Format:
{
    "status": "success/error",
    "folder_url": "https://drive.google.com/...",
    "spreadsheet_url": "https://docs.google.com/..."
}
"""

import requests
from google.oauth2 import service_account
import google.auth.transport.requests
from datetime import datetime

# Service account configuration
SERVICE_ACCOUNT_CREDS = {
    "type": "service_account",
    "project_id": "valiant-circuit-427111-c3",
    "private_key_id": "75e57d9c273833fa860a0f79ae7493d15bedce20",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCqGRrn/CiCpXqj\nfFCbSFgZW4j1b1BP20CnLACyiL1mCMPK1XzeWS0OORirIggbfKKzKYm9U0BLXXkj\niFpGDumkSi48iQMGIwDi9+lrOrdsh8Sfi1F01D2UOUvy1YcbmS0f8I/+rHP/IjGM\nIWWKdQGtI4fs9xVqnJFMmJU7+kW54WyiMErW7Ui2tdkUFjhtHVKTJsyPxieUXIiq\nqMTuO/QaqiLl+rxjw5ZyoPPXut6ouNL/fphY6WFRBRw1EBp92lqR4NtEd0Xqd9no\nlkfaNq6CZcRzEFGcSEgluVDs+aQIzVDWGSV48qO+dhvOXbIExYKrf3IbaHfY8LRr\nK5uNXhyrAgMBAAECggEABIRzKvsO5l1XsvTPvTgAIvhD3GTO6LgFcQshn5wzD30n\nGgFudgc/Q5PvnEfkmDpIpeJyBoWp/PZoC7II17h4qwTPUos++dA/K0fzOoZOLcMz\nTRtpl+U1F3UoF7RlCK4aPTFp2ZUh5YI2d6bBaBpwZ3U8nGX5eyHaWALrX7LnXCbd\nx6PXgUaQ/611sXhUbHd7k4v5mmlbTqLflC7D3czd/s1mvBX+iqiBzSXkfPdV1u7H\n7QZr02dIMZSMa25TN1/Fv9DXfjmOArybSG3uDAnWV73NqYq61aGcEBApMtBJTIUB\nbkScp/sDe396Adk5uIGTIrM3VxCD5LiIb3RegK54eQKBgQDvkeLRViugAz13aUbV\np8Ki4Uayzon6OblLUSPLkleJ9ljhp8MMz27vtOSIKXoDbnOgW+n+Ew+/1TtCGGSJ\nYkxj95lDFEeqL9c7rZJoCsRYZ8mojtBiscstRcNzOuDQwF0DdSG4h/R5mYY7zO53\n3fm71aQqD0jL13/DgeLtSY1LAwKBgQC1w4G94Tuy0GDd9rO/57ZQO5y2yKsxjAgI\nwkQtH3rWl20MXj+JPdaIWHCm+fRBC0JZt+aM6fruWvP920FZs36AVYEh7DnenARD\nxLpowBflpYJiJaT/jpG95GngfnkAd2MlQhKS4CBw0QgR0b63ST5ocMIM86fN8oXg\nqQlw2Y0jOQKBgAL+bLo2/HaUc8kxPJxg61LDw/FqGVlSLVmemvbpTkTAGl4/jXV0\nhititFRrSEYQtEs1utfc/x5jmMj7qw34d4HsTzMCZt7emC77vU+lisycB24e0sXY\n+PQI4idnffW94auwZAp9UHXQkFfg+L3wvTU2t0V7SWqat9MGpYJXn/dnAoGBAJcF\nHeNaJHPp1tIVjDvCliQLo6XrDPJZ2sMMRgEHytRJdH12QWwSSRF4CgFyZJM2e6Z3\nucMTFT69q0QczCtvi4etg2FgGKTxFEoKRqeKE1DnN3G8vV7oYgdYpO+1pWvRxjrK\nrwwB1HJn+0By+PbokEXOiiygtafT/ZAwYnu1BiNhAoGBAObPccJu98qs8iUC2l7y\nP+O3zA2QNn6KaxgP2EnM5fpOcjsfMr839r7yEdkEiks4CI3kNavx6nzm9AivxNFg\nR9Hp5g9MMNTn2ixrMoc0tYJNTS05lc2R60UC4oEN5UFvSEEbi8168zMFNS4FO4PL\n+VvcaepsmFNakfdWG9kmGWGq\n-----END PRIVATE KEY-----\n",
    "client_email": "dify-trancsrib-analyzing-resul@valiant-circuit-427111-c3.iam.gserviceaccount.com",
    "client_id": "116848026776812596140",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dify-trancsrib-analyzing-resul%40valiant-circuit-427111-c3.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

def create_spreadsheet(token, file_name, sheet_data):
    """Creates a Google spreadsheet and returns its ID"""
    # Log input data
    with open('/opt/sheet-service/spreadsheet_create.log', 'w') as f:
        f.write(f"Creating spreadsheet at {datetime.now()}\n")
        f.write(f"File name: {file_name}\n")
        f.write(f"Sheet data: {str(sheet_data)}\n")

    try:
        # Create spreadsheet request
        spreadsheet_response = requests.post(
            "https://sheets.googleapis.com/v4/spreadsheets",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "properties": {
                    "title": file_name
                },
                "sheets": [
                    {
                        "properties": {
                            "title": file_name,
                            "gridProperties": {
                                "frozenRowCount": 2
                            }
                        },
                        "data": [
                            {
                                "rowData": sheet_data
                            }
                        ]
                    }
                ]
            }
        )

        # Log response
        with open('/opt/sheet-service/spreadsheet_response.log', 'w') as f:
            f.write(f"Spreadsheet response at {datetime.now()}\n")
            f.write(f"Status code: {spreadsheet_response.status_code}\n")
            f.write(f"Response: {spreadsheet_response.text}\n")

        if spreadsheet_response.status_code != 200:
            raise Exception(f"Failed to create spreadsheet: {spreadsheet_response.text}")

        spreadsheet_id = spreadsheet_response.json().get('spreadsheetId')
        if not spreadsheet_id:
            raise Exception("Spreadsheet ID not found in the response")

        return spreadsheet_id

    except Exception as e:
        # Log error
        with open('/opt/sheet-service/spreadsheet_error.log', 'w') as f:
            f.write(f"Error creating spreadsheet at {datetime.now()}\n")
            f.write(f"Error: {str(e)}\n")
        raise e

def set_permissions(token, file_id, user_email=None):
    """Sets access permissions for the file"""
    try:
        # Log permission setting start
        with open('/opt/sheet-service/permissions_setting.log', 'w') as f:
            f.write(f"Setting permissions at {datetime.now()}\n")
            f.write(f"File ID: {file_id}\n")
            f.write(f"User email: {user_email if user_email else 'None'}\n")

        # Set public link access
        anyone_permission = requests.post(
            f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "role": "reader",
                "type": "anyone",
                "allowFileDiscovery": False
            }
        )
        
        # Log public permission response
        with open('/opt/sheet-service/permissions_response.log', 'w') as f:
            f.write(f"Anyone permissions response at {datetime.now()}\n")
            f.write(f"Status code: {anyone_permission.status_code}\n")
            f.write(f"Response: {anyone_permission.text}\n")
        
        if user_email:
            # Set specific user permissions
            user_permission = requests.post(
                f"https://www.googleapis.com/drive/v3/files/{file_id}/permissions",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "role": "writer",
                    "type": "user",
                    "emailAddress": user_email
                }
            )
            
            # Log user permission response
            with open('/opt/sheet-service/user_permissions_response.log', 'w') as f:
                f.write(f"User permissions response at {datetime.now()}\n")
                f.write(f"Status code: {user_permission.status_code}\n")
                f.write(f"Response: {user_permission.text}\n")
            
            if not (anyone_permission.status_code in [200, 201] and user_permission.status_code in [200, 201]):
                raise Exception("Failed to set permissions")
        else:
            if not anyone_permission.status_code in [200, 201]:
                raise Exception("Failed to set permissions")
        
        return True

    except Exception as e:
        # Log error
        with open('/opt/sheet-service/permissions_error.log', 'w') as f:
            f.write(f"Error setting permissions at {datetime.now()}\n")
            f.write(f"Error: {str(e)}\n")
        raise e

def move_spreadsheet_to_folder(token, spreadsheet_id, folder_id):
    """Moves spreadsheet to specified folder"""
    try:
        # Log move operation start
        with open('/opt/sheet-service/move_spreadsheet.log', 'w') as f:
            f.write(f"Moving spreadsheet at {datetime.now()}\n")
            f.write(f"Spreadsheet ID: {spreadsheet_id}\n")
            f.write(f"Folder ID: {folder_id}\n")

        # Execute move request
        move_response = requests.patch(
            f"https://www.googleapis.com/drive/v3/files/{spreadsheet_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            params={
                'addParents': folder_id,
                'fields': 'id, parents'
            }
        )

        # Log move response
        with open('/opt/sheet-service/move_response.log', 'w') as f:
            f.write(f"Move response at {datetime.now()}\n")
            f.write(f"Status code: {move_response.status_code}\n")
            f.write(f"Response: {move_response.text}\n")
        
        if move_response.status_code != 200:
            raise Exception(f"Failed to move spreadsheet: {move_response.text}")
            
        return True

    except Exception as e:
        # Log error
        with open('/opt/sheet-service/move_error.log', 'w') as f:
            f.write(f"Error moving spreadsheet at {datetime.now()}\n")
            f.write(f"Error: {str(e)}\n")
        raise e

def process_sheet_data(template_data):
    """Main data processing function"""
    try:
        # Log process start
        with open('/opt/sheet-service/process_start.log', 'w') as f:
            f.write(f"Starting process at {datetime.now()}\n")
            f.write(f"Template data: {str(template_data)}\n")

        # Generate timestamp for file naming
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"CustomerStories_{timestamp}"

        # Log credentials creation
        with open('/opt/sheet-service/credentials.log', 'w') as f:
            f.write(f"Creating credentials at {datetime.now()}\n")

        # Initialize credentials
        credentials = service_account.Credentials.from_service_account_info(
            SERVICE_ACCOUNT_CREDS,
            scopes=['https://www.googleapis.com/auth/drive.file', 
                   'https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Refresh token
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        token = credentials.token
        
        if not token:
            with open('/opt/sheet-service/token_error.log', 'w') as f:
                f.write(f"Failed to obtain token at {datetime.now()}\n")
            raise Exception("Failed to obtain access token")

        # Log folder creation
        with open('/opt/sheet-service/folder_create.log', 'w') as f:
            f.write(f"Creating folder at {datetime.now()}\n")
            f.write(f"Folder name: {file_name}\n")

        # Create folder
        folder_response = requests.post(
            "https://www.googleapis.com/drive/v3/files",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={
                "name": file_name,
                "mimeType": "application/vnd.google-apps.folder"
            }
        )
        
        # Log folder response
        with open('/opt/sheet-service/folder_response.log', 'w') as f:
            f.write(f"Folder response at {datetime.now()}\n")
            f.write(f"Status code: {folder_response.status_code}\n")
            f.write(f"Response: {folder_response.text}\n")
        
        if folder_response.status_code != 200:
            raise Exception(f"Failed to create folder: {folder_response.text}")
        
        folder_id = folder_response.json().get('id')
        if not folder_id:
            raise Exception("Folder ID not found in the response")
        
        # Set folder permissions
        set_permissions(token, folder_id)
        
        # Get sheet data from template
        if isinstance(template_data, dict) and 'output' in template_data:
            sheet_data = template_data['output']
        else:
            raise Exception("Invalid template data format")
        
        # Create spreadsheet
        spreadsheet_id = create_spreadsheet(token, file_name, sheet_data)
        
        # Move spreadsheet to folder
        move_spreadsheet_to_folder(token, spreadsheet_id, folder_id)
        
        # Set spreadsheet permissions
        set_permissions(token, spreadsheet_id)

        # Log successful completion
        with open('/opt/sheet-service/process_complete.log', 'w') as f:
            f.write(f"Process completed at {datetime.now()}\n")
            f.write(f"Folder URL: https://drive.google.com/drive/folders/{folder_id}\n")
            f.write(f"Spreadsheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/view\n")
        
        return {
            "status": "success",
            "folder_url": f"https://drive.google.com/drive/folders/{folder_id}",
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/view"
        }

    except Exception as e:
        # Log error
        with open('/opt/sheet-service/process_error.log', 'w') as f:
            f.write(f"Error at {datetime.now()}\n")
            f.write(f"Error: {str(e)}\n")
            f.write(f"Template data: {str(template_data)}\n")
        return {
            "status": "error",
            "message": str(e)
        }
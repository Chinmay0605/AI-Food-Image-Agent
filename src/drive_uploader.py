import os

from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


load_dotenv()


SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


CREDENTIALS_FILE = os.path.join(
    "credentials",
    "credentials.json"
)


TOKEN_FILE = os.path.join(
    "credentials",
    "token.json"
)


def get_drive_service():

    creds = None

    if os.path.exists(TOKEN_FILE):

        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not creds or not creds.valid:

        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):

            creds.refresh(
                Request()
            )

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        with open(
            TOKEN_FILE,
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    return service


def find_existing_file(
    service,
    folder_id,
    file_name
):

    query = (
        f"'{folder_id}' in parents "
        f"and name = '{file_name}' "
        f"and trashed = false"
    )

    results = service.files().list(
        q=query,
        spaces="drive",
        fields="files(id,name,webViewLink)",
        pageSize=10
    ).execute()

    files = results.get(
        "files",
        []
    )

    if files:

        return files[0]

    return None


def upload_file(
    file_path,
    file_name=None
):

    folder_id = os.getenv(
        "GOOGLE_DRIVE_FOLDER_ID"
    )

    if not folder_id:

        raise ValueError(
            "GOOGLE_DRIVE_FOLDER_ID is missing from .env"
        )

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_name is None:

        file_name = os.path.basename(
            file_path
        )

    service = get_drive_service()


    # -------------------------------------------------
    # Check whether the file already exists
    # -------------------------------------------------

    existing_file = find_existing_file(
        service,
        folder_id,
        file_name
    )


    media = MediaFileUpload(
        file_path,
        mimetype="image/jpeg",
        resumable=True
    )


    # -------------------------------------------------
    # UPDATE existing file
    # -------------------------------------------------

    if existing_file:

        print(
            f"Updating existing Drive file: "
            f"{file_name}"
        )

        updated_file = service.files().update(
            fileId=existing_file["id"],
            media_body=media,
            fields="id,name,webViewLink"
        ).execute()

        return {
            "id": updated_file.get("id"),
            "name": updated_file.get("name"),
            "url": updated_file.get(
                "webViewLink"
            ),
            "action": "updated"
        }


    # -------------------------------------------------
    # CREATE new file
    # -------------------------------------------------

    print(
        f"Uploading new Drive file: "
        f"{file_name}"
    )

    file_metadata = {
        "name": file_name,
        "parents": [
            folder_id
        ]
    }


    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,name,webViewLink"
    ).execute()


    return {
        "id": uploaded_file.get("id"),
        "name": uploaded_file.get("name"),
        "url": uploaded_file.get(
            "webViewLink"
        ),
        "action": "created"
    }
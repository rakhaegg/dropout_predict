# test_gdrive_google_api.py

"""
Test koneksi Google Drive menggunakan Service Account tanpa PyDrive2,
melainkan langsung menggunakan googleapiclient dan google-auth.

Pastikan Anda sudah menginstal paket berikut di virtual environment:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Skrip ini akan:
1. Memuat kredensial Service Account dari file JSON.
2. Membuat instance Drive API client.
3. Menampilkan daftar file di dalam folder tertentu (FOLDER_ID).
4. Mengunggah file teks kecil ("dvc_test.txt") ke folder tersebut.
"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ===================================================================
# 1) Ganti path ke file JSON Service Account Anda:
SERVICE_ACCOUNT_FILE = "seismic-octane-441403-b9-51d554db6971.json"
# ===================================================================

# ===================================================================
# 2) Ganti dengan Folder ID Google Drive yang dipakai untuk DVC:
#    Contoh URL folder: https://drive.google.com/drive/folders/1AbCdEfGHijKlmNoPQRsT
FOLDER_ID = "1slQ2wu0Lz_DPKCeKE0kZ-mge1qhUAM3e"
# ===================================================================

# Ruang lingkup (scope) akses yang dibutuhkan: penuh untuk Drive
SCOPES = ["https://www.googleapis.com/auth/drive"]

def main():
    # Cek apakah file Service Account JSON ada
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"ERROR: File JSON '{SERVICE_ACCOUNT_FILE}' tidak ditemukan.")
        return

    # Muat kredensial Service Account dan buat Drive API client
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        drive_service = build("drive", "v3", credentials=creds)
        print(f"✅ Berhasil autentikasi Service Account dari '{SERVICE_ACCOUNT_FILE}'")
    except Exception as e:
        print("❌ Gagal autentikasi Service Account:", e)
        return

    # 3. List file di dalam folder target
    print(f"\n📂 Daftar file di folder ID '{FOLDER_ID}':")
    try:
        # Query untuk mencari file yang parent-nya adalah FOLDER_ID
        response = drive_service.files().list(
            q=f"'{FOLDER_ID}' in parents and trashed=false",
            spaces="drive",
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()

        files = response.get("files", [])
        if not files:
            print("  (Kosong: folder belum berisi file apa pun.)")
        else:
            for f in files:
                print(f"  • {f['name']}  (ID: {f['id']})")

    except Exception as e:
        print("❌ Gagal menampilkan daftar file:", e)
        return

    # 4. Buat file uji "dvc_test.txt" secara lokal
    test_filename = "dvc_test.txt"
    with open(test_filename, "w") as f:
        f.write("Ini hanya file uji untuk memverifikasi akses Google Drive API.\n")
    print(f"\n⬆️  Mencoba upload '{test_filename}' ke folder GDrive...")

    try:
        file_metadata = {
            "name": test_filename,
            "parents": [FOLDER_ID],
        }
        media = MediaFileUpload(test_filename, mimetype="text/plain")

        uploaded = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id",
            supportsAllDrives=True
        ).execute()

        file_id = uploaded.get("id")
        print(f"✅ Sukses mengupload '{test_filename}' dengan ID: {file_id}")

        # (Opsional) Hapus file uji setelah upload
        # drive_service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
        # print(f"🗑️  File '{test_filename}' dihapus dari Drive.")

    except Exception as e:
        print("❌ Gagal upload file uji:", e)

if __name__ == "__main__":
    main()

from supabase import create_client
import uuid

SUPABASE_URL = "https://eejusguyovqragrxpknv.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVlanVzZ3V5b3ZxcmFncnhwa252Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY5NjQ5NTksImV4cCI6MjA5MjU0MDk1OX0.1nXECp10CTBnVevdyp9JJRte4rALEW_b0QQIaOW3M4E"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_file(file):
    file_ext = file.name.split('.')[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"

    file_bytes = file.read()

    supabase.storage.from_("media").upload(file_name, file_bytes)

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/media/{file_name}"

    return public_url

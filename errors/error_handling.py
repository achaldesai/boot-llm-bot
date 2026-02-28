from google.genai import errors


def error_handler(e: Exception):
    if isinstance(e, errors.ClientError):
        if e.code == 429:
            print("🛑 Intercepted 429: Quota exceeded.")
            print(f"Message: {e.message}")
            exit(69)
        else:
            print(f"⚠️ Client Error ({e.code}): {e.message}")
    elif isinstance(e, errors.APIError):
        print(f"🌐 Server API Error ({e.code}): {e.message}")
        raise (e)
    else:
        print(f"❌ Unexpected Error: {e}")
        raise e

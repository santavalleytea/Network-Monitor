# used to test download and upload speed 
import speedtest

'''
Function to measure download and upload speed

'''
def run_speed_test():
    try:
        st = speedtest.Speedtest(secure=True)
        st.get_best_server()

        download_speed = st.download() / 1000000
        upload_speed = st.upload() / 1000000
        ping = st.results.ping

        return {
            "download_speed": round(download_speed, 2),
            "upload_speed": round(upload_speed, 2),
            "ping": round(ping, 2)
        }
    
    except Exception as e:
        print(f"[ERROR] Speed test failed: {e}")
        return {
            "download_speed": 0,  # Ensure these values exist
            "upload_speed": 0,
            "ping": "N/A"  # Use "N/A" if ping fails
        }
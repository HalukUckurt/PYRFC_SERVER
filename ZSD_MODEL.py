'''
Created on 15 Ara 2025

@author: halukuckurt

son eklemeler yapıldı.
'''
import os

from pyrfc import RCStatus, Server, set_ini_file_directory


# server function
def my_stfc_connection(
    request_context=None,
    REQUTEXT="",
):
    print("stfc invoked")
    print("request_context", request_context)
    print(f"REQUTEXT: {REQUTEXT}")

    return {
        "ECHOTEXT": REQUTEXT,
        "RESPTEXT": "Python server here",
    }


# server authorisation check
def my_auth_check(
    func_name=False,
    request_context=None,
):
    print(f"authorization check for '{func_name}'")
    print("request_context", request_context or {})
    # Burada istersen ileride fonksiyon bazlı yetki kontrolü ekleyebilirsin
    return RCStatus.OK


def main():
    # Python betiğinin çalıştığı dizini bulur
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # sapnwrfc.ini dosyasının aranacağı dizini ayarlar
    set_ini_file_directory(dir_path)

    # server instance oluştur
    server = Server(
        server_params={"dest": "gateway"},
        client_params={"dest": "MME"},
        config={
            "port": 8081,
            "server_log": False,
        },
    )

    # Python fonksiyonunu ABAP STFC_CONNECTION fonksiyonu olarak publish et
    server.add_function("STFC_CONNECTION", my_stfc_connection)

    try:
        server.start()
        print("✅ Server started.")
        try:
            attrs = server.get_server_attributes()
            print("Server attributes:", attrs)
        except Exception as attr_ex:
            print("⚠️ Server attributes okunamadı:", attr_ex)

        input("Press Enter to stop server...\n")

    except KeyboardInterrupt:
        print("\n🛑 KeyboardInterrupt alındı, server durduruluyor...")
    except Exception as ex:
        print("❌ Server çalışırken hata oluştu:", ex)
    finally:
        try:
            server.stop()
            print("✅ Server stopped.")
        except Exception as stop_ex:
            print("⚠️ Server durdurulurken hata oluştu:", stop_ex)


if __name__ == "__main__":
    main()

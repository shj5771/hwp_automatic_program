import win32com.client as win32
import pythoncom

def extract_hwp_text(hwp_path, output_path=None):
    pythoncom.CoInitialize()
    try:
        hwp = win32.DispatchEx("HWPFrame.HwpObject")
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        hwp.RegisterModule("Clipboard", "")
        hwp.Open(hwp_path, "", "forceopen:true")

        # 🔸 문서 텍스트 추출
        text = hwp.GetTextFile("TEXT", "")

        # 🔸 출력 파일 저장
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"✅ 텍스트 추출 완료: {output_path}")
        else:
            print("✅ 추출된 텍스트:")
            print(text)

        hwp.Quit()
        return text

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    finally:
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    # 테스트용 파일 경로
    HWP_PATH = r"C:\Users\ST\Desktop\10_23\10_23_test.hwp"
    TXT_PATH = r"C:\Users\ST\Desktop\10_23\10_23_test.txt"

    extract_hwp_text(HWP_PATH, TXT_PATH)

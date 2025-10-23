import win32com.client as win32
import pythoncom
import os

def hwp_open(frame_path: str, view: bool = False):
    pythoncom.CoInitialize()
    try:
        hwp = win32.DispatchEx("HWPFrame.HwpObject")
        hwp.XHwpWindows.Item(0).Visible = view

        # 모듈 등록
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        hwp.RegisterModule("Clipboard", "")

        # 파일 열기
        hwp.Open(frame_path, "", "forceopen:true")
        print(f"✅ 한글 문서 열기 성공: {frame_path}")
        return hwp

    except Exception as e:
        print(f"❌ HWP 열기 실패: {e}")
        pythoncom.CoUninitialize()
        raise


if __name__ == "__main__":
    FRAME_PATH = r"C:\Users\ST\Desktop\10_23\10_23_test.hwp"
    SAVE_PATH = r"C:\Users\ST\Desktop\10_23\result\result_test.hwp"

    hwp = hwp_open(FRAME_PATH, view=True)

    try:
        # 🔸 호환성 처리 (버전에 따라 다르게 시도)
        try:
            hwp.SaveAs(SAVE_PATH, "HWP", "forceopen:true")
        except:
            try:
                hwp.SaveAs(SAVE_PATH, "HWP")
            except:
                hwp.SaveAs(SAVE_PATH)

        print(f"💾 저장 완료: {SAVE_PATH}")

    except Exception as e:
        print(f"❌ 저장 오류: {e}")

    finally:
        hwp.Quit()
        pythoncom.CoUninitialize()

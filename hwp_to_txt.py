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

def normalize_text_blocks(text: str) -> str:
    """
    줄바꿈이 많은 HWP 표형 텍스트를 한 줄 단위로 정리
    예: '성명\n\n' → '성명 : ( )'
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    merged = []
    skip_next = False

    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        # '성명' 다음줄이 빈칸인 경우 자동 병합
        if i + 1 < len(lines) and len(lines[i+1]) <= 3:
            merged.append(f"{line} : ( )")
            skip_next = True
        else:
            merged.append(line)
    return "\n".join(merged)


if __name__ == "__main__":
    # 테스트용 파일 경로
    HWP_PATH = r"C:\Users\ST\Desktop\10_23\10_23_test.hwp"
    TXT_PATH = r"C:\Users\ST\Desktop\10_23\doc_text.txt"

    extract_hwp_text(HWP_PATH, TXT_PATH)
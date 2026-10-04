import fitz
import glob
import os
import subprocess
import shutil
import time

def run_batch_ocr():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, '교과서_기출')
    output_dir = os.path.join(base_dir, '교과서_기출_OCR')
    temp_dir = os.path.join(base_dir, '_temp_ocr_pages')

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    # Find target files: scanned PDFs except 장기중학교 and textbooks
    all_pdfs = sorted(glob.glob(os.path.join(input_dir, '*.pdf')))
    target_pdfs = []

    for f in all_pdfs:
        fname = os.path.basename(f)
        if '장기중학교' in fname:
            continue
        if '교과서' in fname or '핵심요약' in fname:
            continue
        target_pdfs.append(f)

    print(f"Total Target PDFs for OCR: {len(target_pdfs)}")
    print("=" * 80)

    total_start = time.time()
    summary_report = []

    for idx, pdf_path in enumerate(target_pdfs, 1):
        fname = os.path.basename(pdf_path)
        base_name = os.path.splitext(fname)[0]
        md_name = f"{base_name}_OCR.md"
        out_md_path = os.path.join(output_dir, md_name)

        print(f"\n[{idx}/{len(target_pdfs)}] Starting OCR: {fname}")
        file_start = time.time()

        # Clean temp directory
        for old_f in glob.glob(os.path.join(temp_dir, '*.png')):
            try:
                os.remove(old_f)
            except Exception:
                pass

        doc = fitz.open(pdf_path)
        page_count = len(doc)
        print(f"  - Rendering {page_count} pages to PNG (DPI 200)...")

        for p_idx in range(page_count):
            page = doc[p_idx]
            pix = page.get_pixmap(dpi=200)
            png_path = os.path.join(temp_dir, f"page_{p_idx+1:02d}.png")
            pix.save(png_path)

        # Call PowerShell OCR worker
        temp_txt_out = os.path.join(temp_dir, 'ocr_raw.txt')
        if os.path.exists(temp_txt_out):
            os.remove(temp_txt_out)

        ps_cmd = [
            'powershell',
            '-ExecutionPolicy', 'Bypass',
            '-File', os.path.join(base_dir, 'ocr_worker.ps1'),
            '-ImageDir', temp_dir,
            '-OutputFile', temp_txt_out
        ]

        print("  - Running Windows Media OCR Engine...")
        res = subprocess.run(ps_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')

        if not os.path.exists(temp_txt_out) or os.path.getsize(temp_txt_out) == 0:
            print(f"  [ERROR] OCR Failed for {fname}: {res.stderr}")
            continue

        with open(temp_txt_out, 'r', encoding='utf-8') as tf:
            ocr_text = tf.read()

        # Format Final Markdown with Header Metadata
        header = f"""# [기출문제 OCR 전문] {base_name}

- **원천 파일**: `{fname}`
- **총 페이지 수**: {page_count}면
- **추출 엔진**: Windows.Media.Ocr (Microsoft Korean OCR)
- **추출 일시**: 2026-09-21
- **문서 용도**: 2026학년도 중1 국어 중간고사 대비 출제 분석 및 원천 지문 데이터

================================================================================

"""
        with open(out_md_path, 'w', encoding='utf-8') as mf:
            mf.write(header + ocr_text)

        elapsed = time.time() - file_start
        char_count = len(ocr_text)
        print(f"  -> SUCCESS: Saved {md_name} ({char_count} chars, {elapsed:.1f}s)")
        summary_report.append({
            'name': fname,
            'md_name': md_name,
            'pages': page_count,
            'chars': char_count,
            'time': elapsed
        })

    # Clean up temp directory
    shutil.rmtree(temp_dir, ignore_errors=True)

    total_elapsed = time.time() - total_start
    print("\n" + "=" * 80)
    print(f"All {len(summary_report)} PDFs OCR Completed in {total_elapsed:.1f}s!")
    print(f"Output Directory: {output_dir}")
    print("=" * 80)

if __name__ == '__main__':
    run_batch_ocr()

"""
pdf_to_md.py — Portable PDF to Markdown via Marker.

Usage (from anywhere):
    uv run --project <skill_dir> <skill_dir>/pdf_to_md.py input.pdf
    uv run --project <skill_dir> <skill_dir>/pdf_to_md.py input.pdf --output-dir /tmp/
    uv run --project <skill_dir> <skill_dir>/pdf_to_md.py input.pdf --force-ocr
"""

import argparse
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("pdf_to_md")

COPILOT_BASE_URL = "http://localhost:4141/v1"


def validate_dependencies():
    try:
        import marker  # noqa: F401
        log.info("Marker detected")
        return True
    except ImportError as e:
        log.error(f"Marker not installed: {e}")
        log.error("Run: cd <skill_dir> && uv sync")
        return False


def convert_pdf_to_markdown(
    input_pdf_path: str,
    use_llm: bool = False,
    force_ocr: bool = False,
    page_range: str | None = None,
    output_dir: str | None = None,
    copilot_model: str | None = None,
) -> str:
    """
    Convert a PDF to Markdown with Marker.

    Args:
        input_pdf_path: Path to the PDF file.
        use_llm: Use LLM for better quality (tables, math).
        force_ocr: Force OCR even if text is extractable.
        page_range: Pages to convert. Ex: "0,5-10,20". None = all.
        output_dir: Output folder. None = same folder as PDF.
        copilot_model: copilot-api model to use (e.g. gpt-4o).

    Returns:
        Markdown content as string.
    """
    pdf_path = Path(input_pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"File not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF: {pdf_path.suffix}")

    from marker.converters.pdf import PdfConverter
    from marker.models import create_model_dict
    from marker.output import text_from_rendered
    from marker.config.parser import ConfigParser

    config: dict = {
        "output_format": "markdown",
        "languages": ["en", "fr"],
        "max_pages": None,
        "parallel_factor": 1,
    }

    if force_ocr:
        config["force_ocr"] = True
        log.info("OCR forced")

    if page_range:
        config["page_range"] = page_range
        log.info(f"Pages: {page_range}")

    config["disable_image_extraction"] = True

    if copilot_model:
        use_llm = True

    if use_llm:
        config["use_llm"] = True
        if copilot_model:
            config["llm_service"] = "marker.services.openai.OpenAIService"
            config["openai_base_url"] = COPILOT_BASE_URL
            config["openai_model"] = copilot_model
            config["openai_api_key"] = "copilot"
            log.info(f"LLM via copilot-api: {copilot_model}")
        else:
            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if api_key:
                config["gemini_api_key"] = api_key
            else:
                log.warning("use_llm=True but no GOOGLE_API_KEY found.")

    dest_dir = Path(output_dir) if output_dir else pdf_path.parent
    dest_dir.mkdir(parents=True, exist_ok=True)
    md_path = dest_dir / f"{pdf_path.stem}.md"

    log.info(f"Converting: {pdf_path.name}")
    log.info(f"Options: llm={use_llm}, ocr={force_ocr}, pages={page_range or 'all'}")
    log.info(f"Output: {md_path}")

    try:
        config_parser = ConfigParser(config)
        config_dict = config_parser.generate_config_dict()

        converter = PdfConverter(
            artifact_dict=create_model_dict(),
            config=config_dict,
            processor_list=config_parser.get_processors() if not use_llm else None,
            renderer=config_parser.get_renderer() if not use_llm else None,
            llm_service=config_parser.get_llm_service() if use_llm else None,
        )

        log.info("Starting conversion...")
        rendered = converter(str(pdf_path))
        text, _, _ = text_from_rendered(rendered)

    except Exception as e:
        log.error(f"Conversion error: {e}")
        log.error("Try: --force-ocr, --pages, or --copilot gpt-4o")
        raise RuntimeError(f"Conversion failed: {e}") from e

    if not text or not text.strip():
        raise RuntimeError(f"Empty result for {pdf_path.name}")

    md_path.write_text(text, encoding="utf-8")
    log.info(f"Saved: {md_path}")

    log.info(f"Done: {len(text):,} chars")
    return text


def main():
    if not validate_dependencies():
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description="Convert a PDF to Markdown via Marker (SOTA).",
        epilog="Examples:\n"
        "  pdf_to_md.py report.pdf\n"
        "  pdf_to_md.py report.pdf --force-ocr --output-dir /tmp/\n"
        "  pdf_to_md.py report.pdf --copilot gpt-4o\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", help="Path to a PDF file.")
    parser.add_argument("--use-llm", action="store_true", help="Use Gemini LLM (needs GOOGLE_API_KEY).")
    parser.add_argument("--force-ocr", action="store_true", help="Force OCR. Fixes garbled text, converts math to LaTeX.")
    parser.add_argument("--pages", type=str, default=None, help='Pages to convert. Ex: "0,5-10,20".')
    parser.add_argument("--output-dir", type=str, default=None, help="Output directory.")
    parser.add_argument("--copilot", type=str, metavar="MODEL", default=None, help="LLM via copilot-api (localhost:4141).")

    args = parser.parse_args()
    input_path = Path(args.input).resolve()

    if not input_path.is_file():
        log.error(f"Not a file: {input_path}")
        sys.exit(1)

    try:
        convert_pdf_to_markdown(
            str(input_path),
            use_llm=args.use_llm,
            force_ocr=args.force_ocr,
            page_range=args.pages,
            output_dir=args.output_dir,
            copilot_model=args.copilot,
        )
        log.info("Conversion complete!")

    except KeyboardInterrupt:
        log.info("\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        log.error(f"Fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

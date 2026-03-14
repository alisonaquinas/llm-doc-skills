"""Tests for text-first document and diagram wrapper scripts.

These tests exercise pure command-building logic and missing-tool failures
without requiring Pandoc, a TeX distribution, Typst, cmark-gfm, Mermaid CLI,
PlantUML, Graphviz, Java, or Asciidoctor in the local environment.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_module(rel_path: str):
    module_path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(module_path.stem.replace("-", "_"), module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestPandocWrapper(unittest.TestCase):
    def test_build_command_includes_common_options(self):
        mod = _load_module("pandoc/scripts/convert.py")
        cmd = mod.build_command(
            pandoc="pandoc",
            input_path="input.md",
            to_format="docx",
            output_path="output.docx",
            from_format="gfm",
            standalone=True,
            toc=True,
            citeproc=True,
            pdf_engine="xelatex",
            metadata=["title=Report"],
        )
        self.assertEqual(
            cmd,
            [
                "pandoc",
                "input.md",
                "--to",
                "docx",
                "--from",
                "gfm",
                "--output",
                "output.docx",
                "--standalone",
                "--toc",
                "--citeproc",
                "--pdf-engine",
                "xelatex",
                "--metadata",
                "title=Report",
            ],
        )

    def test_find_pandoc_reports_install_hint(self):
        mod = _load_module("pandoc/scripts/convert.py")
        with mock.patch.object(mod.shutil, "which", return_value=None):
            with self.assertRaises(FileNotFoundError) as ctx:
                mod.find_pandoc()
        self.assertIn("pandoc.org", str(ctx.exception))


class TestLatexWrappers(unittest.TestCase):
    def test_build_command_uses_engine_and_outdir(self):
        mod = _load_module("latex/scripts/build.py")
        cmd = mod.build_command(
            latexmk="latexmk",
            input_path="paper.tex",
            engine="xelatex",
            bib_tool="bibtex",
            outdir="build",
            clean_intermediates=False,
        )
        self.assertEqual(
            cmd,
            [
                "latexmk",
                "-xelatex",
                "-interaction=nonstopmode",
                "-file-line-error",
                "-bibtex",
                "-outdir=build",
                "paper.tex",
            ],
        )

    def test_clean_targets_cover_common_aux_files(self):
        mod = _load_module("latex/scripts/clean.py")
        targets = mod.collect_cleanup_targets("report.tex", "build")
        self.assertIn(Path("build") / "report.aux", targets)
        self.assertIn(Path("build") / "report.fdb_latexmk", targets)


class TestTypstWrapper(unittest.TestCase):
    def test_build_command_includes_root_pages_and_ppi(self):
        mod = _load_module("typst/scripts/compile.py")
        cmd = mod.build_command(
            typst="typst",
            input_path="deck.typ",
            target_format="png",
            output_path="deck.png",
            root="project",
            ppi=144,
            pages="1-2",
        )
        self.assertEqual(
            cmd,
            ["typst", "compile", "--root", "project", "--pages", "1-2", "--ppi", "144", "deck.typ", "deck.png"],
        )


class TestMarkdownWrapper(unittest.TestCase):
    def test_html_command_prefers_cmark_output_shape(self):
        mod = _load_module("markdown/scripts/render.py")
        cmd = mod.build_command(
            renderer="cmark-gfm",
            input_path="README.md",
            target_format="html",
            output_path="README.html",
            gfm=True,
            toc=False,
        )
        self.assertEqual(cmd, ["cmark-gfm", "README.md"])

    def test_choose_renderer_reports_helpful_error(self):
        mod = _load_module("markdown/scripts/render.py")
        with mock.patch.object(mod, "find_tool", return_value=None):
            with self.assertRaises(FileNotFoundError) as ctx:
                mod.choose_renderer("html")
        self.assertIn("cmark-gfm", str(ctx.exception))
        self.assertIn("pandoc", str(ctx.exception))


class TestGithubFlavoredMarkdownWrapper(unittest.TestCase):
    def test_build_command_defaults_to_gfm_for_pandoc(self):
        mod = _load_module("github-flavored-markdown/scripts/render.py")
        cmd = mod.build_command(
            renderer="pandoc",
            input_path="README.md",
            target_format="pdf",
            output_path="README.pdf",
            gfm=True,
            toc=True,
        )
        self.assertEqual(
            cmd,
            ["pandoc", "README.md", "--to", "pdf", "--from", "gfm", "--output", "README.pdf", "--toc"],
        )


class TestGitlabFlavoredMarkdownWrapper(unittest.TestCase):
    def test_build_command_uses_gfm_for_export(self):
        mod = _load_module("gitlab-flavored-markdown/scripts/render.py")
        cmd = mod.build_command(
            renderer="pandoc",
            input_path="page.md",
            target_format="docx",
            output_path="page.docx",
            toc=False,
        )
        self.assertEqual(
            cmd,
            ["pandoc", "page.md", "--from", "gfm", "--to", "docx", "--output", "page.docx"],
        )


class TestMermaidWrapper(unittest.TestCase):
    def test_build_command_includes_theme_and_config(self):
        mod = _load_module("mermaid/scripts/render.py")
        cmd = mod.build_command(
            mermaid="mmdc",
            input_path="flow.mmd",
            target_format="svg",
            output_path="flow.svg",
            theme="neutral",
            background="white",
            config_file="mermaid.json",
        )
        self.assertEqual(
            cmd,
            ["mmdc", "--input", "flow.mmd", "--output", "flow.svg", "--theme", "neutral", "--backgroundColor", "white", "--configFile", "mermaid.json"],
        )

    def test_find_mermaid_reports_install_hint(self):
        mod = _load_module("mermaid/scripts/render.py")
        with mock.patch.object(mod.shutil, "which", return_value=None):
            with mock.patch.dict(mod.os.environ, {}, clear=True):
                with self.assertRaises(FileNotFoundError) as ctx:
                    mod.find_mermaid()
        self.assertIn("mermaid", str(ctx.exception).lower())


class TestPlantumlWrapper(unittest.TestCase):
    def test_build_command_supports_theme_and_output_dir(self):
        mod = _load_module("plantuml/scripts/render.py")
        cmd = mod.build_command(
            plantuml_cmd=["plantuml"],
            input_path="diagram.puml",
            target_format="svg",
            output_dir="out",
            theme="plain",
            config_file="plantuml.cfg",
        )
        self.assertEqual(
            cmd,
            ["plantuml", "-tsvg", "-o", "out", "-config", "plantuml.cfg", "-theme", "plain", "diagram.puml"],
        )


class TestGraphvizWrapper(unittest.TestCase):
    def test_build_command_uses_layout_specific_binary(self):
        mod = _load_module("graphviz/scripts/render.py")
        cmd = mod.build_command(
            layout_tool="neato",
            input_path="graph.dot",
            target_format="svg",
            output_path="graph.svg",
        )
        self.assertEqual(cmd, ["neato", "-Tsvg", "graph.dot", "-o", "graph.svg"])

    def test_find_layout_tool_reports_install_hint(self):
        mod = _load_module("graphviz/scripts/render.py")
        with mock.patch.object(mod.shutil, "which", return_value=None):
            with mock.patch.dict(mod.os.environ, {}, clear=True):
                with self.assertRaises(FileNotFoundError) as ctx:
                    mod.find_layout_tool("dot")
        self.assertIn("graphviz", str(ctx.exception).lower())


class TestAsciiDocWrapper(unittest.TestCase):
    def test_build_command_uses_backend_and_attributes(self):
        mod = _load_module("asciidoc/scripts/build.py")
        cmd = mod.build_command(
            tool="asciidoctor",
            input_path="guide.adoc",
            target_format="docbook",
            output_path="guide.xml",
            safe_mode="server",
            attributes=["sectnums", "toc=left"],
        )
        self.assertEqual(
            cmd,
            [
                "asciidoctor",
                "guide.adoc",
                "--safe-mode",
                "server",
                "--backend",
                "docbook",
                "--attribute",
                "sectnums",
                "--attribute",
                "toc=left",
                "--out-file",
                "guide.xml",
            ],
        )


if __name__ == "__main__":
    unittest.main()

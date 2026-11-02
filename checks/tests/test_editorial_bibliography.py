"""The note, its data-driven entry and both PDF directions disappear together."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import fitz

ROOT = Path(__file__).resolve().parents[2]


class EditorialBibliography(unittest.TestCase):
    def test_data_backlinks_and_no_notes_edition(self):
        original = (ROOT / 'editorial.bib').read_bytes()
        with tempfile.TemporaryDirectory(prefix='kirillov-editorial-',
                                         dir='/tmp') as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / 'content', root / 'content')
            shutil.copytree(ROOT / 'assets/fonts', root / 'assets/fonts')
            shutil.copy2(ROOT / 'references.bib', root / 'references.bib')
            data = root / 'editorial.bib'
            data.write_bytes(original)
            source = root / 'sample.typ'
            source.write_text(
                '#import "content/book-style.typ": book-style\n'
                '#import "content/main-defs.typ": *\n'
                '#show: book-style\n'
                '#set page(numbering: "1")\n'
                'Основной текст.#ed-note[Контрольное упоминание: '
                '@bib:Gardner1995, § 3.]\n'
                '#if editorial-notes {\n'
                '  pagebreak()\n'
                '  include "content/81-editorial-bibliography.typ"\n'
                '}\n')

            def compile_pdf(name, notes=True):
                output = root / name
                command = ['typst', 'compile', '--root', str(root),
                           '--ignore-system-fonts', '--font-path',
                           str(root / 'assets/fonts')]
                if not notes:
                    command += ['--input', 'editorial-notes=off']
                result = subprocess.run(command + [str(source), str(output)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                return fitz.open(output)

            with compile_pdf('with.pdf') as document:
                self.assertGreaterEqual(len(document), 2)
                note = document[0].search_for('Контрольное упоминание:')[0]
                targets = [(page, hits[0]) for page in document
                           if (hits := page.search_for('Geometric Tomography'))]
                self.assertEqual(len(targets), 1)
                target_page, target = targets[0]
                forwards = [link for link in document[0].get_links()
                            if link.get('page') == target_page.number]
                self.assertTrue(forwards)
                for link in forwards:
                    self.assertLess(link['to'].y, target.y0)
                backwards = [link for link in target_page.get_links()
                             if link.get('page') == 0]
                self.assertEqual(len(backwards), 1)
                self.assertLess(backwards[0]['to'].y, note.y0)
                self.assertLess(note.y0 - backwards[0]['to'].y, 30)
                self.assertIn('Р1.', target_page.get_text())

            changed = original.decode().replace(
                'title = {Geometric Tomography}',
                'title = {Editorial data mutation probe}', 1)
            changed = changed.replace(
                'year = {1995},',
                'year = {1995},\n  doi = {10.1234/editorial-probe},', 1)
            data.write_text(changed)
            with compile_pdf('changed.pdf') as document:
                self.assertIn('Editorial data mutation probe',
                              ''.join(page.get_text() for page in document))
                self.assertIn('https://doi.org/10.1234/editorial-probe',
                              [link.get('uri')
                               for page in document
                               for link in page.get_links()])

            with compile_pdf('without.pdf', notes=False) as document:
                self.assertEqual(len(document), 1)
                text = document[0].get_text()
                self.assertIn('Основной текст.', text)
                self.assertNotIn('Контрольное', text)
                self.assertNotIn('Редакционная литература', text)
                self.assertNotIn('Gardner', text)
                self.assertNotIn('Прим. ред.', text)
                self.assertEqual(document[0].get_links(), [])
        self.assertEqual((ROOT / 'editorial.bib').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()

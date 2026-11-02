"""Compile data mutations and verify their text and PDF destinations."""
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

import fitz

ROOT = Path(__file__).resolve().parents[2]


class BibliographySource(unittest.TestCase):
    def test_data_changes_and_internal_links(self):
        original = (ROOT / 'references.bib').read_bytes()
        with tempfile.TemporaryDirectory(prefix='kirillov-bib-',
                                         dir='/tmp') as temporary:
            root = Path(temporary)
            shutil.copytree(ROOT / 'content', root / 'content')
            shutil.copytree(ROOT / 'assets/fonts', root / 'assets/fonts')
            shutil.copy2(ROOT / 'editorial.bib', root / 'editorial.bib')
            source = root / 'references.bib'
            source.write_bytes(original)
            sample = root / 'sample.typ'
            sample.write_text(
                '#import "content/book-style.typ": book-style\n'
                '#show: book-style\n'
                '#set page(numbering: "1")\n'
                'Первое упоминание: @bib:KolmogorovFomin1976.\n'
                '#pagebreak()\n'
                'Второе упоминание: @bib:KolmogorovFomin1976.\n'
                '#pagebreak()\n'
                '#include "content/80-bibliography.typ"\n')

            def compile_pdf(name):
                output = root / name
                result = subprocess.run([
                    'typst', 'compile', '--root', str(root),
                    '--ignore-system-fonts', '--font-path',
                    str(root / 'assets/fonts'), str(sample), str(output)],
                    cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '', result.stderr)
                return fitz.open(output)

            def text(document):
                result = ' '.join(page.get_text() for page in document)
                return ' '.join(result.replace('\u00ad\n', '')
                                .replace('\u00ad', '').split())

            def replace_record(data, key, old, new):
                start = data.index('{' + key + ',')
                end = data.index('\n}', start)
                entry = data[start:end]
                self.assertIn(old, entry)
                return data[:start] + entry.replace(old, new, 1) + data[end:]

            with compile_pdf('before.pdf') as before:
                baseline = text(before)
                links_before = [link.get('uri') for page in before
                                for link in page.get_links()]
            self.assertIn('Элементы теории функций', baseline)
            self.assertIn('https://doi.org/10.2307/1970694', links_before)

            changed = replace_record(
                original.decode(), 'KolmogorovFomin1976',
                'title = {Элементы теории функций и функционального анализа}',
                'title = {Bibliography mutation probe}')
            changed = replace_record(
                changed, 'AtiyahBott1967', 'doi = {10.2307/1970694}',
                'doi = {10.1234/mutation-probe}')
            changed = replace_record(
                changed, 'Kac1965', 'pages = {84--113}',
                'pages = {9001--9002}')
            source.write_text(changed)
            with compile_pdf('changed.pdf') as after:
                rendered = text(after)
                links_after = [link.get('uri') for page in after
                               for link in page.get_links()]
            self.assertIn('Bibliography mutation probe', rendered)
            self.assertNotIn('Элементы теории функций', rendered)
            self.assertIn('9001–9002', rendered)
            self.assertIn('https://doi.org/10.1234/mutation-probe', links_after)
            self.assertNotIn('https://doi.org/10.2307/1970694', links_after)

            # Add an internal reference to the twice-mentioned record.
            # The unmodified list also has Langlands -> ArithmeticGroups,
            # where the target has no textual mentions at all.
            data = original.decode()
            start = data.index('{Cohen1969,')
            end = data.index('\n}', start)
            entry = data[start:end]
            entry = re.sub(
                r'(annotation = \{)(.*)(\},)',
                lambda match: match[1] + match[2]
                + ' Внутренняя ссылка [{ref:KolmogorovFomin1976}].'
                + match[3], entry)
            source.write_text(data[:start] + entry + data[end:])
            with compile_pdf('backlinks.pdf') as document:
                rendered = text(document)
                found = re.search(r'32\. Колмогоров(.+?)33\. Коэн',
                                  rendered, re.S)
                self.assertIsNotNone(found)
                self.assertEqual(re.findall(r'\[(\d+(?:, \d+)*)\]',
                                            found[1]), ['1, 2'])
                page = next(page for page in document
                            if '32. Колмогоров' in page.get_text())
                area = page.search_for('[1, 2]')
                self.assertEqual(len(area), 1)
                backlinks = [link for link in page.get_links()
                             if link['from'].intersects(area[0])]
                self.assertEqual(sorted(link['page'] for link in backlinks),
                                 [0, 1])
                # Both links must point above their actual mention.
                for link in backlinks:
                    target = document[link['page']]
                    mention = target.search_for('упоминание:')[0]
                    self.assertLess(link['to'].y, mention.y0)
                    self.assertGreaterEqual(mention.y0 - link['to'].y, 8)
                    self.assertLess(mention.y0 - link['to'].y, 30)
                internal_page = next(page for page in document
                                     if 'Внутренняя ссылка'
                                     in page.get_text())
                internal_area = internal_page.search_for(
                    'Внутренняя ссылка')[0]
                internal = [link for link in internal_page.get_links()
                            if link.get('page') == page.number
                            and abs(link['from'].y0 - internal_area.y0) < 25]
                self.assertTrue(internal)
                unmentioned = re.search(
                    r'2\. Арифметические(.+?)3\. Атья', rendered, re.S)
                self.assertIsNotNone(unmentioned)
                self.assertNotRegex(unmentioned[1], r'\[\d')
        self.assertEqual((ROOT / 'references.bib').read_bytes(), original)

    def test_author_list_contains_only_structure_and_keys(self):
        source = (ROOT / 'content/80-bibliography.typ').read_text()
        entries = re.findall(r'#bib-description\(\s*"([A-Za-z0-9]+)"\s*,?\s*\)',
                             source)
        supplementary = re.findall(
            r'#bib-item\(\s*supplementary:\s*true', source)
        self.assertEqual(len(entries) - len(supplementary), 242)
        self.assertEqual(len(set(entries)), len(entries))
        labels = re.findall(r'<bib:([A-Za-z0-9]+)>', source)
        self.assertEqual(entries, labels)
        self.assertNotIn('Элементы теории функций', source)
        self.assertNotIn('doi.org', source)


if __name__ == '__main__':
    unittest.main()

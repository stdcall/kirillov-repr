from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

import fitz

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_links import check_links, check_hint_links
PREFIX = '''#import "/content/book-style.typ": book-style
#import "/content/main-defs.typ": *
#import "/content/statements.typ": *
#show: book-style
#set page(numbering: "1")
'''


def typst(source, command, *arguments):
    args = ['typst', command, '--root', str(ROOT), '--ignore-system-fonts',
            '--font-path', str(ROOT/'assets/fonts')]
    if command == 'eval':
        args += [arguments[0], '--in', '-', '--format', 'json']
    else:
        args += ['-', *arguments]
    result = subprocess.run(
        args,
        input=PREFIX + source, capture_output=True, text=True)
    if result.returncode or result.stderr.strip():
        raise AssertionError(result.stderr)
    return result.stdout


class Numbering(unittest.TestCase):
    def test_colon_introduction_stays_with_the_formulation(self):
        source = '''#set page(height: 100mm, margin: 10mm)
== Параграф
=== Подраздел
#block(height: 145pt)[Предыдущий текст.]
#problem[
  Выведите следующую _формулировку_:

  _Если условие выполнено, заключение верно._
] <pr:colon-introduction>
'''
        with tempfile.TemporaryDirectory(prefix='kirillov-introduction-',
                                         dir='/tmp') as temporary:
            output = Path(temporary) / 'fixture.pdf'
            typst(source, 'compile', str(output))
            with fitz.open(output) as document:
                intros = [(page.number, rect) for page in document
                          for rect in page.search_for('формулировку')]
                bodies = [(page.number, rect) for page in document
                          for rect in page.search_for('Если условие')]
                self.assertEqual(len(intros), 1)
                self.assertEqual(len(bodies), 1)
                self.assertEqual(intros[0][0], bodies[0][0])
                self.assertGreater(bodies[0][1].y0, intros[0][1].y1 + 1)
                text = ' '.join(document[intros[0][0]].get_text().split())
                self.assertIn('следующую формулировку', text)

    def test_numbered_example_list_follows_the_common_counter(self):
        source = '''== Параграф
=== Подраздел
#example(numbered: true)[Отдельный пример.] <exm:before>
#examples([#example-item[Первый в перечне.] <exm:first>],
  [#example-item[Второй в перечне.] <exm:second>])
Ссылки: @exm:first, @exm:second.
'''
        values = json.loads(typst(source, 'eval',
                                  'query(metadata).map(it => it.value)'))
        refs = [v['printed'] for v in values if isinstance(v, dict)
                and v.get('kind') == 'cross-reference']
        self.assertEqual(refs, ['2', '3'])
        with tempfile.TemporaryDirectory(prefix='kirillov-examples-',
                                         dir='/tmp') as temporary:
            output = Path(temporary) / 'fixture.pdf'
            typst(source, 'compile', str(output))
            text = ''.join(page.get_text() for page in fitz.open(output))
            self.assertIn('2. Первый', text)
            self.assertIn('3. Второй', text)

    def test_hint_and_answer_both_return_to_the_problem(self):
        source = '''== Параграф
=== Подраздел
#problem[Условие с двумя решениями.] <pr:both>
#pagebreak()
#hint[@pr:both][Текст указания.]
#pagebreak()
#answer[@pr:both][Текст ответа.]
#problem[Условие только с ответом.] <pr:answer-only>
#pagebreak()
#answer[@pr:answer-only][Единственный ответ.]
'''
        values = json.loads(typst(source, 'eval',
                                  'query(metadata).map(it => it.value)'))
        links = [v for v in values if isinstance(v, dict)
                 and v.get('kind') == 'hint-link']
        problems = [v for v in links if v['from'] == 'problem']
        self.assertEqual([v['target-position']['page'] for v in problems],
                         [2, 4])
        with tempfile.TemporaryDirectory(prefix='kirillov-solutions-',
                                         dir='/tmp') as temporary:
            output = Path(temporary) / 'fixture.pdf'
            typst(source, 'compile', str(output))
            report = check_hint_links(check_links(output, []), links)
        self.assertEqual(report['problems_with_hint'], 2)
        self.assertEqual(report['hint_numbers'], 1)
        self.assertEqual(report['answer_numbers'], 2)

    def records(self, inserted):
        source = '''#heading(level: 1, numbering: none)[Первая]
<part:first>
== Первый параграф
=== Первый подраздел
#problem[Первое условие.] <pr:first>
#hint[@pr:first][Указание.]
''' + inserted + '''
#problem[Последнее условие.] <pr:last>
Ссылка: @pr:last.
=== Второй подраздел
#problem[Новое условие.] <pr:next>
#heading(level: 1, numbering: none)[Вторая]
<part:second>
== Второй параграф
=== Первый подраздел
#problem[Другое условие.] <pr:second>
'''
        values = json.loads(typst(source, 'eval',
                                  'query(metadata).map(it => it.value)'))
        problems = [x['number'] for x in values if isinstance(x, dict)
                    and x.get('kind') == 'numbered' and x.get('family') == 'pr']
        references = [x['printed'] for x in values if isinstance(x, dict)
                      and x.get('kind') == 'cross-reference'
                      and x.get('target') == 'pr:last']
        return problems, references

    def test_insertion_renumbers_the_target_and_its_native_reference(self):
        before, before_ref = self.records('')
        after, after_ref = self.records('#problem[Вставленное условие.] <pr:inserted>')
        self.assertEqual(before, [[1, 1, 1], [1, 1, 2], [1, 2, 1], [2, 1, 1]])
        self.assertEqual(after, [[1, 1, 1], [1, 1, 2], [1, 1, 3],
                                 [1, 2, 1], [2, 1, 1]])
        self.assertEqual(before_ref, ['2'])
        self.assertEqual(after_ref, ['3'])

    def test_statement_starts_a_new_paragraph_and_display_has_clearance(self):
        source = '''== Параграф
=== Подраздел
Предыдущий абзац.

#problem[Самостоятельное условие.] <pr:paragraph>

Вводная строка.
$ (a+b)^2 = a^2 + 2a b + b^2 $
Следующая строка.
'''
        with tempfile.TemporaryDirectory(prefix='kirillov-style-', dir='/tmp') as tmp:
            output = Path(tmp)/'fixture.pdf'
            typst(source, 'compile', str(output))
            doc = fitz.open(output)
            words = [word for page in doc for word in page.get_text('words')]
            previous = next(w for w in words if w[4] == 'абзац.')
            problem = next(w for w in words if w[4] == 'Задача')
            self.assertGreater(problem[1], previous[3])
            intro = next(w for w in words if w[4] == 'Вводная')
            following = next(w for w in words if w[4] == 'Следующая')
            formula = [w for w in words if intro[3] < w[1] < following[1]]
            self.assertTrue(formula)
            self.assertGreater(min(w[1] for w in formula) - intro[3], 1)
            self.assertGreater(following[1] - max(w[3] for w in formula), 1)

    def test_condition_and_displays_share_formula_numbers(self):
        source = '''== Параграф
=== Подраздел
$ a = b $ <eq:first>
#numbered-condition[Для всякого $x$ выполняется условие.] <eq:words>
$ b = c $ <eq:last>
Ссылка на условие: @eq:words.
'''
        values = json.loads(typst(source, 'eval',
                                  'query(metadata).map(it => it.value)'))
        equations = [v['number'] for v in values if isinstance(v, dict)
                     and v.get('kind') == 'numbered' and v.get('family') == 'eq']
        self.assertEqual(equations, [[1, 1, 1], [1, 1, 2], [1, 1, 3]])
        references = [v for v in values if isinstance(v, dict)
                      and v.get('kind') == 'cross-reference'
                      and v.get('target') == 'eq:words']
        self.assertEqual(len(references), 1)
        self.assertTrue(references[0]['resolved'])
        self.assertEqual(references[0]['printed'], '2')
        with tempfile.TemporaryDirectory(prefix='kirillov-formula-', dir='/tmp') as tmp:
            output = Path(tmp)/'fixture.pdf'
            typst(source, 'compile', str(output))
            text = ''.join(p.get_text() for p in fitz.open(output))
            self.assertIn('(2)', text)
            self.assertNotIn('( 2 )', text)

    def test_symbolic_formula_tag_keeps_its_name_across_sections(self):
        source = '''== Параграф
=== Подраздел
$ a = b $ <eq:first>
$ b = c $ <eq:orbit-character-formula>
$ c = d $ <eq:last>
== Другой параграф
=== Подраздел
Ссылка: @eq:orbit-character-formula.
'''
        values = json.loads(typst(source, 'eval',
                                  'query(metadata).map(it => it.value)'))
        equations = [v['number'] for v in values if isinstance(v, dict)
                     and v.get('kind') == 'numbered' and v.get('family') == 'eq']
        self.assertEqual(equations, [[1, 1, 1], [1, 1, 'Φ'], [1, 1, 2]])
        reference = next(v for v in values if isinstance(v, dict)
                         and v.get('kind') == 'cross-reference')
        self.assertTrue(reference['resolved'])
        self.assertEqual(reference['printed'], 'Φ')


if __name__ == '__main__':
    unittest.main()

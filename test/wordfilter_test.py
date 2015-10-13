import os
import unittest
import wordfilter

# Note that tests won't work with "python setup.py develop"
# Installing in a virtualenv to run tests


class wordfilterTest(unittest.TestCase):

    def setUp(self):
        self.wf = wordfilter.Wordfilter()

    def test_detects_bad_words_in_a_string(self):
        self.assertTrue(isinstance(self.wf, object))

        self.assertTrue(self.wf.blacklisted('this string contains the word skank'))
        self.assertTrue(self.wf.blacklisted('this string contains the word SkAnK'))

        self.assertFalse(self.wf.blacklisted('this string is clean!'))

    def test_add_a_word_to_blacklist(self):
        self.wf.add_words(['clean'])

        self.assertTrue('clean' in self.wf.blacklist)
        self.assertTrue(self.wf.blacklisted('this string was clean!'))

    def test_clear_blacklist(self):
        self.wf.clear_list()
        self.assertFalse('skank' in self.wf.blacklist)

        self.assertFalse(self.wf.blacklisted('this string contains the word skank'))

        self.wf.add_words(['skank'])
        self.assertTrue('skank' in self.wf.blacklist)
        self.assertTrue(self.wf.blacklisted('this string contains the word skank'))

    def test_added_words_checked_case_insensitively(self):
        self.wf.add_words(['CLEAN'])

        self.assertTrue('clean' in self.wf.blacklist)
        self.assertTrue(self.wf.blacklisted("this string was clean!"))

    def test_passed_list(self):
        '''Try to add a custom list'''

        blacklist_wordfilter = wordfilter.Wordfilter(blacklist=['custom', 'word', 'list'])

        self.assertTrue(blacklist_wordfilter.blacklisted('custom'))
        self.assertFalse(blacklist_wordfilter.blacklisted('skank'))

    def test_add_words_in_iterable(self):
        def word_generator():
            yield 'test'

        self.wf.add_words(word_generator())

        self.assertTrue('test' in self.wf.blacklist)
        self.assertTrue(self.wf.blacklisted('test'))

    def test_add_string_to_blacklist(self):
        self.wf.add_words('test')

        self.assertTrue('test' in self.wf.blacklist)
        self.assertTrue(self.wf.blacklisted("this string was tested!"))

        self.assertRaises(TypeError, self.wf.add_words, 9)
        self.assertFalse(self.wf.blacklisted("9"))

    def test_custom_blacklist(self):
        '''Try to pass a txt file'''
        txt = 'dummy.txt'

        with open(txt, 'w') as f:
            f.write(u"custom\nword\nlist")

        datafile_wordfilter = wordfilter.Wordfilter(datafile=txt)

        self.assertTrue(datafile_wordfilter.blacklisted('custom'))
        self.assertFalse(datafile_wordfilter.blacklisted('skank'))

        os.remove(txt)

    def test_remove_words(self):
        self.wf.remove_words('biatch')
        self.assertFalse(self.wf.blacklisted('biatch'))


    def test_module_instance(self):
        self.assertTrue(wordfilter.blacklisted('this string contains mustard.'))

        wordfilter.clear_list()
        self.assertFalse(wordfilter.blacklisted('this string contains mustard.'))

        wordfilter.add_words(['custom'])
        self.assertTrue(wordfilter.blacklisted('you can use a custom blacklist.'))


def main():
    unittest.main()

if __name__ == '__main__':
    main()

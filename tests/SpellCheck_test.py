import time
import unittest

from srbai.SintaktickiOperatori.spellcheck import SpellCheck


class SpellCheckTests(unittest.TestCase):
    def test_spellcheck(self):

        sc = SpellCheck('sr-latin')
        print('done reading dic and initializing')
        word = "predetori"
        start_time = time.time()
        correction = sc.spellcheck(word)
        if correction:
            print(f"Did you mean '{correction}'?")
        else:
            print("No close match found.")
        end_time = time.time()
        duration = end_time - start_time
        print("duration was:" + str(duration))

        word = "rdnici"
        start_time = time.time()
        correction = sc.spellcheck(word)
        if correction:
            print(f"Did you mean '{correction}'?")
        else:
            print("No close match found.")
        end_time = time.time()
        duration = end_time - start_time
        print("duration was:" + str(duration))


if __name__ == '__main__':
    unittest.main()
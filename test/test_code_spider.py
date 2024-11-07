# test_code_spider.py
import sys
import os
import unittest

# 获取当前文件的目录
# 计算上一级目录的路径
# 将上一级目录添加到sys.path中

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import code_spider

class TestCodeSpiderOperations(unittest.TestCase):

    def test_add_integers(self):
        self.assertEqual(add(1, 2), 3)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)

    def test_add_floats(self):
        self.assertAlmostEqual(add(1.1, 2.2), 3.3, places=1)
        self.assertAlmostEqual(add(-1.1, 1.1), 0.0, places=1)

    def test_add_strings(self):
        with self.assertRaises(TypeError):
            add("hello", "world")
        with self.assertRaises(TypeError):
            add("1", 2)

if __name__ == '__main__':
    unittest.main()

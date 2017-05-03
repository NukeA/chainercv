import numpy as np
import unittest

import chainer
from chainer import testing

from chainercv.utils import ConstantStubLink


@testing.parameterize(
    {'outputs': {'shape': (3, 4), 'dtype': np.float32}},
    {'outputs': ({'shape': (3, 4), 'dtype': np.float32},)},
    {'outputs': (
        {'shape': (3, 4), 'dtype': np.float32},
        {'shape': (3,), 'dtype': np.int32})},
)
class TestConstantStubLink(unittest.TestCase):

    def setUp(self):
        if isinstance(self.outputs, tuple):
            self.outputs = tuple(np.empty(**output) for output in self.outputs)
        else:
            self.outputs = np.empty(**self.outputs)
        self.link = ConstantStubLink(self.outputs)

    def test_cpu(self):
        self.assertIsInstance(self.link, chainer.Link)

        outputs = self.link('ignored', -1, 'inputs', 1.0)

        if isinstance(self.outputs, tuple):
            originals = self.outputs
            outputs = outputs
        else:
            originals = self.outputs,
            outputs = outputs,

        self.assertEquals(len(originals), len(outputs))

        for orig, out in zip(originals, outputs):
            self.assertIsInstance(out, chainer.Variable)
            self.assertEqual(out.shape, orig.shape)
            self.assertEqual(out.dtype, orig.dtype)

            self.assertEqual(
                chainer.cuda.get_array_module(out.data), np)
            np.testing.assert_equal(out.data, orig)


class TestConstantStubLinkInvalidArgument(unittest.TestCase):

    def test_string(self):
        with self.assertRaises(ValueError):
            ConstantStubLink('invalid')

    def test_list(self):
        with self.assertRaises(ValueError):
            ConstantStubLink([np.empty((3, 4))])


testing.run_module(__name__, __file__)

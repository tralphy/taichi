import pytest
from taichi.lang.exception import TaichiRuntimeError

import taichi as ti
from tests import test_utils


def _test_pow_f(dt):
    z = ti.field(dt, shape=())

    @ti.kernel
    def func(x: dt, y: dt):
        z[None] = x**y

    for x in [0.5, 1, 1.5, 2, 6.66]:
        for y in [-2, -1, -0.3, 0, 0.5, 1, 1.4, 2.6]:
            func(x, y)
            assert abs(z[None] / x**y - 1) < 0.00001


def _test_pow_i(dt):
    z = ti.field(dt, shape=())

    @ti.kernel
    def func(x: dt, y: ti.template()):
        z[None] = x**y

    for x in range(-5, 5):
        for y in range(0, 4):
            func(x, y)
            assert z[None] == x**y


@test_utils.test()
def test_pow_f32():
    _test_pow_f(ti.f32)


@test_utils.test(require=ti.extension.data64)
def test_pow_f64():
    _test_pow_f(ti.f64)


@test_utils.test()
def test_pow_i32():
    _test_pow_i(ti.i32)


@test_utils.test(require=ti.extension.data64)
def test_pow_i64():
    _test_pow_i(ti.i64)


def _ipow_negative_exp(dt):

    z = ti.field(dt, shape=())

    @ti.kernel
    def foo(x: dt, y: ti.template()):
        z[None] = x**y

    with pytest.raises(TaichiRuntimeError):
        foo(10, -10)


@test_utils.test(debug=True,
                 advanced_optimization=False,
                 exclude=[ti.vulkan, ti.opengl, ti.cc])
def test_ipow_negative_exp_i32():
    _ipow_negative_exp(ti.i32)


@test_utils.test(debug=True,
                 advanced_optimization=False,
                 require=ti.extension.data64,
                 exclude=[ti.vulkan, ti.opengl, ti.cc])
def test_ipow_negative_exp_i64():
    _ipow_negative_exp(ti.i64)

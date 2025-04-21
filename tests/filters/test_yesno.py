"""
Adapted from
https://github.com/django/django/blob/5.2/tests/template_tests/filter_tests/test_yesno.py

The official django tests only cover a quite limited set of cases, and only the obvious ones.
We try to cover a lot of edge cases here, to limit the risk of introducing inconsistencies.
"""

import pytest


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_true
def test_yesno_default_true(assert_render):
    template = "{{ var|yesno }}"
    context = {"var": True}
    assert_render(template, context, "yes")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_false
def test_yesno_default_false(assert_render):
    template = "{{ var|yesno }}"
    context = {"var": False}
    assert_render(template, context, "no")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_none
def test_yesno_default_none(assert_render):
    template = "{{ var|yesno }}"
    context = {"var": None}
    assert_render(template, context, "maybe")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_true_arguments
def test_yesno_custom_true(assert_render):
    template = "{{ var|yesno:'certainly,get out of town,perhaps' }}"
    context = {"var": True}
    assert_render(template, context, "certainly")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_false_arguments
def test_yesno_custom_false(assert_render):
    template = "{{ var|yesno:'certainly,get out of town,perhaps' }}"
    context = {"var": False}
    assert_render(template, context, "get out of town")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_none_two_arguments
def test_yesno_two_options_none(assert_render):
    # When no third option is provided, None uses the second option
    template = "{{ var|yesno:'certainly,get out of town' }}"
    context = {"var": None}
    assert_render(template, context, "get out of town")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_three_options_none
def test_yesno_three_options_none(assert_render):
    template = "{{ var|yesno:'certainly,get out of town,perhaps' }}"
    context = {"var": None}
    assert_render(template, context, "perhaps")


# django.tests.template_tests.filter_tests.test_yesno.FunctionTests.test_invalid_value
def test_yesno_invalid_value(assert_render):
    # With invalid value, the filter just passes the input through
    template = "{{ var|yesno:'yes' }}"

    context = {"var": True}
    assert_render(template, context, "True")
    context = {"var": False}
    assert_render(template, context, "False")
    context = {"var": None}
    assert_render(template, context, "None")


def test_yesno_two_options_true(assert_render):
    template = "{{ var|yesno:'yep,nah' }}"
    context = {"var": True}
    assert_render(template, context, "yep")


def test_yesno_two_options_false(assert_render):
    template = "{{ var|yesno:'yep,nah' }}"
    context = {"var": False}
    assert_render(template, context, "nah")


@pytest.mark.parametrize(
    "value",
    [
        "value",  # non-empty string
        ["item"],  # non-empty list
        1,  # non-zero number
    ],
)
def test_yesno_truthy_values(assert_render, value):
    template = "{{ var|yesno }}"
    context = {"var": value}
    assert_render(template, context, "yes")


@pytest.mark.parametrize(
    "value",
    [
        "",  # empty string
        [],  # empty list
        0,  # zero
    ],
)
def test_yesno_falsy_values(assert_render, value):
    template = "{{ var|yesno }}"
    context = {"var": value}
    assert_render(template, context, "no")


def test_yesno_too_many_commas(assert_render):
    # With more than 3 comma-separated values,
    # Django falls back to using only the first two values.
    template = "{{ var|yesno:'certainly,get out of town,perhaps,something extra' }}"

    context = {"var": True}
    assert_render(template, context, "certainly")
    context = {"var": False}
    assert_render(template, context, "get out of town")
    context = {"var": None}
    assert_render(template, context, "get out of town")


def test_yesno_empty_mapping(assert_render):
    # With empty mapping, values are converted directly to strings
    template = "{{ var|yesno:'' }}"

    context = {"var": True}
    assert_render(template, context, "True")
    context = {"var": False}
    assert_render(template, context, "False")
    context = {"var": None}
    assert_render(template, context, "None")


def test_yesno_with_variable_argument(assert_render):
    template = "{{ var|yesno:mapping }}"
    mapping = "okay,nope,uncertain"

    context = {"var": True, "mapping": mapping}
    assert_render(template, context, "okay")
    context = {"var": False, "mapping": mapping}
    assert_render(template, context, "nope")
    context = {"var": None, "mapping": mapping}
    assert_render(template, context, "uncertain")

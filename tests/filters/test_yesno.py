

def test_yesno_default_true(assert_render):
    template = "{{ var|yesno }}"
    context = {"var": True}
    assert_render(template, context, "yes")


def test_yesno_default_false(assert_render):
    template = "{{ var|yesno }}"
    context = {"var": False}
    assert_render(template, context, "no")


def test_yesno_default_none(assert_render):
    template = "{{ var|yesno }}"
    context = {"var": None}
    assert_render(template, context, "maybe")


def test_yesno_custom_true(assert_render):
    template = "{{ var|yesno:'yeah,nope,perhaps' }}"
    context = {"var": True}
    assert_render(template, context, "yeah")


def test_yesno_custom_false(assert_render):
    template = "{{ var|yesno:'yeah,nope,perhaps' }}"
    context = {"var": False}
    assert_render(template, context, "nope")


def test_yesno_custom_none(assert_render):
    template = "{{ var|yesno:'yeah,nope,perhaps' }}"
    context = {"var": None}
    assert_render(template, context, "perhaps")


def test_yesno_two_options_true(assert_render):
    template = "{{ var|yesno:'yep,nah' }}"
    context = {"var": True}
    assert_render(template, context, "yep")


def test_yesno_two_options_false(assert_render):
    template = "{{ var|yesno:'yep,nah' }}"
    context = {"var": False}
    assert_render(template, context, "nah")


def test_yesno_two_options_none(assert_render):
    # When no third option is provided, None uses the second option
    template = "{{ var|yesno:'yep,nah' }}"
    context = {"var": None}
    assert_render(template, context, "nah")


def test_yesno_empty_string(assert_render):
    # Empty string is falsy
    template = "{{ var|yesno }}"
    context = {"var": ""}
    assert_render(template, context, "no")


def test_yesno_empty_list(assert_render):
    # Empty list is falsy
    template = "{{ var|yesno }}"
    context = {"var": []}
    assert_render(template, context, "no")


def test_yesno_non_empty_list(assert_render):
    # Non-empty list is truthy
    template = "{{ var|yesno }}"
    context = {"var": ["item"]}
    assert_render(template, context, "yes")


def test_yesno_non_empty_string(assert_render):
    # Non-empty string is truthy
    template = "{{ var|yesno }}"
    context = {"var": "value"}
    assert_render(template, context, "yes")


def test_yesno_zero(assert_render):
    # Zero is falsy
    template = "{{ var|yesno }}"
    context = {"var": 0}
    assert_render(template, context, "no")


def test_yesno_nonzero(assert_render):
    # Non-zero number is truthy
    template = "{{ var|yesno }}"
    context = {"var": 1}
    assert_render(template, context, "yes")


def test_yesno_too_many_commas(assert_render):
    # With more than 3 comma-separated values, Django uses the first three values
    # and treats None the same as False (using the "no" value)
    template = "{{ var|yesno:'yes,no,maybe,extra,more_extra' }}"
    
    # Test with True value
    context = {"var": True}
    assert_render(template, context, "yes")
    
    # Test with False value
    context = {"var": False}
    assert_render(template, context, "no")
    
    # Test with None value - should use second option like with 2 args
    context = {"var": None}
    assert_render(template, context, "no")


def test_yesno_empty_mapping(assert_render):
    # With empty mapping, values are converted directly to strings
    template = "{{ var|yesno:'' }}"
    
    # Test with True value
    context = {"var": True}
    assert_render(template, context, "True")
    
    # Test with False value
    context = {"var": False}
    assert_render(template, context, "False")
    
    # Test with None value
    context = {"var": None}
    assert_render(template, context, "None")


def test_yesno_with_custom_boolean(assert_render):
    template = "{{ var|yesno }}"
    
    # Test with an object that has a custom __bool__ method
    class CustomBool:
        def __init__(self, value):
            self.value = value
            
        def __bool__(self):
            return self.value
    
    # Test with True boolean conversion
    context = {"var": CustomBool(True)}
    assert_render(template, context, "yes")
    
    # Test with False boolean conversion
    context = {"var": CustomBool(False)}
    assert_render(template, context, "no")


def test_yesno_with_special_chars(assert_render):
    template = "{{ var|yesno:'y\\e\\s,n\\o' }}"
    
    # Backslashes are treated literally
    context = {"var": True}
    assert_render(template, context, "y\\e\\s")
    
    context = {"var": False}
    assert_render(template, context, "n\\o")


def test_yesno_with_variable_argument(assert_render):
    template = "{{ var|yesno:mapping }}"
    
    # Test using a variable as the argument
    context = {"var": True, "mapping": "okay,nope,uncertain"}
    assert_render(template, context, "okay")
    
    context = {"var": False, "mapping": "okay,nope,uncertain"}
    assert_render(template, context, "nope")
    
    context = {"var": None, "mapping": "okay,nope,uncertain"}
    assert_render(template, context, "uncertain")


def test_yesno_with_none_like_values(assert_render):
    template = "{{ var|yesno:'yes,no,maybe' }}"
    
    # Test with None
    context = {"var": None}
    assert_render(template, context, "maybe")
    
    # Test with a custom None-like object
    class NoneObject:
        def __bool__(self):
            return False  # False but not None
    
    # This is falsey but not None, so should be "no" not "maybe"
    context = {"var": NoneObject()}
    assert_render(template, context, "no")

from django.template import Template, Context
from django.test import SimpleTestCase


class YesNoTests(SimpleTestCase):
    def test_yesno_default(self):
        # Test default mapping (yes, no, maybe)
        template = Template("{{ var|yesno }}")

        # Test with True value
        rendered = template.render(Context({"var": True}))
        self.assertEqual(rendered, "yes")
        
        # Test with False value
        rendered = template.render(Context({"var": False}))
        self.assertEqual(rendered, "no")
        
        # Test with None value
        rendered = template.render(Context({"var": None}))
        self.assertEqual(rendered, "maybe")

    def test_yesno_custom(self):
        # Test custom mapping
        template = Template("{{ var|yesno:'yeah,nope,perhaps' }}")

        # Test with True value
        rendered = template.render(Context({"var": True}))
        self.assertEqual(rendered, "yeah")
        
        # Test with False value
        rendered = template.render(Context({"var": False}))
        self.assertEqual(rendered, "nope")
        
        # Test with None value
        rendered = template.render(Context({"var": None}))
        self.assertEqual(rendered, "perhaps")

    def test_yesno_two_options(self):
        # Test with only two options - None uses the second option
        template = Template("{{ var|yesno:'yep,nah' }}")

        # Test with True value
        rendered = template.render(Context({"var": True}))
        self.assertEqual(rendered, "yep")
        
        # Test with False value
        rendered = template.render(Context({"var": False}))
        self.assertEqual(rendered, "nah")
        
        # Test with None value - should use second option when no third option
        rendered = template.render(Context({"var": None}))
        self.assertEqual(rendered, "nah")

    def test_yesno_empty_string(self):
        # Test with empty string (which is falsy)
        template = Template("{{ var|yesno }}")
        rendered = template.render(Context({"var": ""}))
        self.assertEqual(rendered, "no")

    def test_yesno_empty_list(self):
        # Test with empty list (which is falsy)
        template = Template("{{ var|yesno }}")
        rendered = template.render(Context({"var": []}))
        self.assertEqual(rendered, "no")

    def test_yesno_non_empty_list(self):
        # Test with non-empty list (which is truthy)
        template = Template("{{ var|yesno }}")
        rendered = template.render(Context({"var": ["item"]}))
        self.assertEqual(rendered, "yes")

    def test_yesno_non_empty_string(self):
        # Test with non-empty string (which is truthy)
        template = Template("{{ var|yesno }}")
        rendered = template.render(Context({"var": "value"}))
        self.assertEqual(rendered, "yes")

    def test_yesno_zero(self):
        # Test with zero (which is falsy)
        template = Template("{{ var|yesno }}")
        rendered = template.render(Context({"var": 0}))
        self.assertEqual(rendered, "no")

    def test_yesno_nonzero(self):
        # Test with non-zero number (which is truthy)
        template = Template("{{ var|yesno }}")
        rendered = template.render(Context({"var": 1}))
        self.assertEqual(rendered, "yes")
        
    def test_yesno_too_many_commas(self):
        # Test with too many commas in the argument
        template = Template("{{ var|yesno:'yes,no,maybe,extra,more_extra' }}")
        
        # It should still work, but only use the first three values
        rendered = template.render(Context({"var": True}))
        self.assertEqual(rendered, "yes")
        
        rendered = template.render(Context({"var": False}))
        self.assertEqual(rendered, "no")
        
        # In this implementation, with more than 3 comma-separated values,
        # None uses the second value (like with only 2 options)
        rendered = template.render(Context({"var": None}))
        self.assertEqual(rendered, "no")

    def test_yesno_empty_mapping(self):
        # Test with an empty mapping
        template = Template("{{ var|yesno:'' }}")
        
        # With empty mapping, the implementation converts the value directly to string
        rendered = template.render(Context({"var": True}))
        self.assertEqual(rendered, "True")
        
        rendered = template.render(Context({"var": False}))
        self.assertEqual(rendered, "False")
        
        rendered = template.render(Context({"var": None}))
        self.assertEqual(rendered, "None")

    def test_yesno_with_custom_boolean(self):
        # Test with an object that has a custom __bool__ method
        class CustomBool:
            def __init__(self, value):
                self.value = value
                
            def __bool__(self):
                return self.value
                
        template = Template("{{ var|yesno }}")
        
        # Test with True boolean conversion
        rendered = template.render(Context({"var": CustomBool(True)}))
        self.assertEqual(rendered, "yes")
        
        # Test with False boolean conversion
        rendered = template.render(Context({"var": CustomBool(False)}))
        self.assertEqual(rendered, "no")

    def test_yesno_with_special_chars(self):
        # Test with special characters in the arguments
        template = Template("{{ var|yesno:'y\\e\\s,n\\o' }}")
        
        # Backslashes are treated literally in this implementation
        rendered = template.render(Context({"var": True}))
        self.assertEqual(rendered, "y\\e\\s")
        
        rendered = template.render(Context({"var": False}))
        self.assertEqual(rendered, "n\\o")
        
    def test_yesno_with_variable_argument(self):
        # Test using a variable as the argument to yesno
        template = Template("{{ var|yesno:mapping }}")
        
        # Use a variable for the mapping
        context = Context({
            "var": True,
            "mapping": "okay,nope,uncertain"
        })
        
        rendered = template.render(context)
        self.assertEqual(rendered, "okay")
        
        # Update the variable
        context["var"] = False
        rendered = template.render(context)
        self.assertEqual(rendered, "nope")
        
        # Update the variable
        context["var"] = None
        rendered = template.render(context)
        self.assertEqual(rendered, "uncertain")
        
    def test_yesno_with_none_like_values(self):
        # Test with various None-like values
        template = Template("{{ var|yesno:'yes,no,maybe' }}")
        
        # Test with None
        rendered = template.render(Context({"var": None}))
        self.assertEqual(rendered, "maybe")
        
        # Test with a custom None-like object
        class NoneObject:
            def __bool__(self):
                return False  # False but not None
                
        # This is falsey but not None, so should be "no" not "maybe"
        rendered = template.render(Context({"var": NoneObject()}))
        self.assertEqual(rendered, "no")

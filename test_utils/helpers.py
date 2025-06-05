from django.core.exceptions import ValidationError


def helper_test_boolean_default(field_name, default_value, model, info_data):
    """
    Test that a boolean field has the correct default value.

    Args:
        field_name (str): The name of the boolean field to test.
        default_value (bool): The expected default value of the field.
        model (Model): The Django model class to test.
        info_data (dict): Dictionary of valid model data for required fields.

    Returns:
        bool: True if the field's value matches the default; False otherwise.
    """
    # Amend info_data
    info_data.pop(field_name, None)

    # Create test_object from info_data
    test_object = model.objects.create(**info_data)

    # Check placeholder is recorded as default
    result = getattr(test_object, field_name) == default_value

    # Return result
    return result


def helper_test_required_fields(
    test_case, test_object, field_name, is_required
):
    """
    Assert that a field is correctly assigned as required or optional.

    Args:
        test_case (TestCase): The test case instance calling this helper.
        test_object (Model): The Django model instance to validate.
        field_name (str): The name of the field being tested.
        is_required (bool): Indicates whether field should be required or not

    Raises:
        AssertionError: If field's validation does not match expectations.
    """
    with test_case.assertRaises(ValidationError) as cm:
        test_object.full_clean()
    errors = cm.exception.message_dict

    model_name = test_object.__class__.__name__

    if is_required:
        test_case.assertIn(
            field_name,
            errors,
            msg=f"{field_name} should be required in {model_name}",
        )
    else:
        test_case.assertNotIn(
            field_name,
            errors,
            msg=f"{field_name} should not be required in {model_name}",
        )


def helper_test_max_length(
    test_case, model, info_data, field_name, max_length
):
    """
    Validate that a field enforces its maximum length constraint.

    Args:
        test_case (TestCase): The test case instance calling this helper.
        model (Model): The Django model class to test.
        info_data (dict): Dictionary of valid model data.
        field_name (str): The name of the field being tested.
        max_length (int): The maximum allowed length of the field.

    Raises:
        ValidationError: If the field value exceeds the defined max_length.
    """
    # Create object
    test_object = model(**info_data)

    # Check valid at threshold
    setattr(test_object, field_name, "a" * max_length)
    test_object.full_clean()

    # Check invalid above threshold
    setattr(test_object, field_name, "a" * (max_length + 1))
    with test_case.assertRaises(ValidationError):
        test_object.full_clean()

from typing import Any, Callable

import pytest


class ParamizerItem(dict):
    """Test item argument as dict used by Paramizer."""

    def __init__(self, description: str = None, **items: Any):
        """
        Args:
            description (str): description for test argument, displayed when test is invoked
            items: collection of keyword value arguments
        """
        self.description = description
        super().__init__(**items)


class Paramizer:
    """'Wrapper' class for pytest.mark.parametrize which allows specify items by names.

    Example of usage:

    # import
    from app.tests.utils import Paramizer, ParamizerItem

    # in test class a property of the following structure could be defined
    PARAMIZER = Paramizer(
        ParamizerItem("description 1", param_1=<value_1_1>, param_2=<value_1_2>),
        ParamizerItem("description 2", param_1=<value_2_1>, param_2=<value_2_2>),
        ...
    )

    # apply PARAMIZER to test method
    @PARAMIZER.paramize("param_1, param_2, ...")
    def test_method(self, param_1, param_2, ...):
        ...

    Notes:
        Order of items in call of paramizer decorator should be the same
        as order of parameters in test function signature.
        ParamizerItem object should have all params used in
        paramizer decorator and order of these params can be arbitrary.
    """

    def __init__(self, *paramizer_items: ParamizerItem):
        """
        Args:
            paramizer_items (ParamizerItem): a collection of ParamizerItem objects
        """
        self.paramizer_items = paramizer_items

    def paramize(self, item_names: str, **kwargs: Any) -> Callable:
        """Decorator method as wrapper for pytest.mark.parametrize.

        Method uses collection of items, included in self.paramizer_items,
        to create values passed to pytest.mark.parametrize decorator.

        Args:
            item_names: comma-separated arguments for test items names
            kwargs: additional arguments passed to pytest.mark.parametrize

        Returns:
            Test function decorated by pytest.mark.parametrize decorator.

        """

        def _paramize(test_function: Callable) -> Callable:
            items_names_list = [name.strip() for name in item_names.split(",")]
            items_names_set = set(items_names_list)
            items = []
            for idx, item in enumerate(self.paramizer_items, start=1):
                if not items_names_set == set(item.keys()):
                    assert False, (
                        f"ParamizerItem at position: "
                        f"{idx} [{item.description}] "
                        f"should have specified exactly these "
                        f"fields: {item_names}."
                    )
                values = [item[name] for name in items_names_list]
                items.append(pytest.param(*values, id=item.description))

            # here is a call proper pytest decorator to create paramizer tests
            return pytest.mark.parametrize(item_names, items, **kwargs)(test_function)

        return _paramize

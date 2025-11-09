from PyQt6.QtWidgets import QTableWidgetItem

class NumericTableWidgetItem(QTableWidgetItem if QTableWidgetItem else object):
    """
    QTableWidgetItem subclass that sorts numerically instead of alphabetically.

    This is useful for columns containing numeric data that should be sorted
    in numeric order (1, 2, 10, 20) rather than alphabetic order (1, 10, 2, 20).
    Also supports values with non-numeric suffixes like "10s", "5.5°", "100%".

    Usage:
        table.setItem(row, col, NumericTableWidgetItem(numeric_value))
        table.setItem(row, col, NumericTableWidgetItem("10s"))  # Will sort by 10
        table.setItem(row, col, NumericTableWidgetItem("5.5°")) # Will sort by 5.5
    """

    def __init__(self, value):
        """
        Initialize with a numeric value or string with numeric prefix.

        Parameters:
        -----------
        value : int, float, or str
            The numeric value to store and display. If string, extracts numeric prefix.
        """
        if QTableWidgetItem is None:
            raise ImportError("PyQt6 is required to use NumericTableWidgetItem")

        # Store original value for display
        self.display_value = str(value)

        # Extract numeric value from string
        self.numeric_value = self._extract_numeric_value(value)

        super().__init__(self.display_value)

    def _extract_numeric_value(self, value):
        """
        Extract numeric value from input, handling suffixes.

        Parameters:
        -----------
        value : int, float, or str
            Input value to process

        Returns:
        --------
        float
            Extracted numeric value, or 0 if no numeric part found
        """
        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            # Extract numeric part from beginning of string
            import re
            match = re.match(r'^([+-]?\d*\.?\d+)', value.strip())
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    pass

        # Fallback for non-numeric values
        return 0.0

    def __lt__(self, other):
        """
        Compare items numerically for sorting.

        Parameters:
        -----------
        other : QTableWidgetItem
            The other item to compare against

        Returns:
        --------
        bool
            True if this item's numeric value is less than the other's
        """
        if isinstance(other, NumericTableWidgetItem):
            return self.numeric_value < other.numeric_value
        return super().__lt__(other)
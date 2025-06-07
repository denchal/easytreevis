from typing import Any

class StringWrapper:
    def string_wrap(self, obj: Any) -> str:
        """
        Overwrite this to change behaviour.
        """
        return str(obj)

    def is_string_convertible(self, x: Any) -> bool:
        try:
            self.string_wrap(x)
            return True
        except Exception:
            return False

    def get_label(self, object: Any, node_id: Any) -> str:
        label = (
            self.string_wrap(object)
            if object and self.is_string_convertible(object)
            else (
                self.string_wrap(node_id)
                if self.is_string_convertible(node_id)
                else ""
            )
        )
        return label

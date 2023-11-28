from app.converter.platforms.sigma.models.operator import OR, AND, NOT


class Group:
    parent_group = []
    sub_group = None
    last_field = None

    def __init__(self):
        self._items = None

    def __add__(self, other):
        if self.sub_group:
            self.sub_group += other
        elif isinstance(other, Group) and not other.items and other.last_field:
            self._items += other.last_field
        elif self._items and not self._items.items:
            if self.last_field:
                self._items += self.last_field
            self._items += other
        elif self._items and self._items.items:
            self._items += other
        self.last_field = other
        return self
    
    @property
    def _hash(self):
        return hash(str(self._items))
    
    def __hash__(self):
        return hash(str(self._items))

    def __eq__(self, other):
        if isinstance(other, Group):
            return self._hash == other._hash
        return False

    @property
    def items(self):
        return self._items

    @property
    def is_null(self):
        if not self._items or not self.last_field:
            return True
        return False

    @items.setter
    def items(self, value) -> None:
        if self.items is None:
            self._items = value
        elif isinstance(self.items, type(value)) and not self.sub_group:
            if value.items:
                self.items += value.items
        elif not isinstance(self.items, type(value)) and not self.sub_group:
            if isinstance(value, OR):
                value.items.insert(0, self._items)
                self._items = value
            elif isinstance(value, AND):
                self.items.remove_last_item()
                if self.last_field:
                    value += self.last_field
                self._items += value
                self.sub_group = value
            elif isinstance(value, NOT):
                if self.last_field:
                    self._items += self.last_field
                self._items += value
        elif self.sub_group and isinstance(self.items, type(value)):
            self.sub_group = None
        elif self.sub_group and not isinstance(self.items, type(value)):
            if isinstance(value, NOT):
                self.sub_group += value

    def __repr__(self) -> str:
        return f"GROUP({self.items})"

    def finalize(self) -> None:
        if not self.items and self.last_field:
            self._items = self.last_field

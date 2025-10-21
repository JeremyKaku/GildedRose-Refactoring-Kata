# -*- coding: utf-8 -*-

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            ItemFactory.create(item).update()


# --- Strategy Classes ---
class ItemStrategy:
    def __init__(self, item):
        self.item = item

    def update(self):
        self.update_quality()
        self.update_sell_in()
        self.handle_expired()

    def update_quality(self):
        pass

    def update_sell_in(self):
        if self.item.name != "Sulfuras, Hand of Ragnaros":
            self.item.sell_in -= 1

    def handle_expired(self):
        pass


class NormalItem(ItemStrategy):
    def update_quality(self):
        if self.item.quality > 0:
            self.item.quality -= 1

    def handle_expired(self):
        if self.item.sell_in < 0 and self.item.quality > 0:
            self.item.quality -= 1


class AgedBrie(ItemStrategy):
    def update_quality(self):
        if self.item.quality < 50:
            self.item.quality += 1

    def handle_expired(self):
        if self.item.sell_in < 0 and self.item.quality < 50:
            self.item.quality += 1


class BackstagePass(ItemStrategy):
    def update_quality(self):
        if self.item.quality < 50:
            self.item.quality += 1
            if self.item.sell_in < 11 and self.item.quality < 50:
                self.item.quality += 1
            if self.item.sell_in < 6 and self.item.quality < 50:
                self.item.quality += 1

    def handle_expired(self):
        if self.item.sell_in < 0:
            self.item.quality = 0


class Sulfuras(ItemStrategy):
    def update(self):
        pass  # legendary item, no change


# --- Factory ---
class ItemFactory:
    @staticmethod
    def create(item):
        if item.name == "Aged Brie":
            return AgedBrie(item)
        elif "Backstage passes" in item.name:
            return BackstagePass(item)
        elif item.name == "Sulfuras, Hand of Ragnaros":
            return Sulfuras(item)
        else:
            return NormalItem(item)

import unittest
from random import randrange

class Hashtable(object):
    '''
    A dynamically expanding hash table. 
    It should be functionally identical to a `dict`.
    '''

    def __init__(self, **kwargs):
        """
        Each key:value pair in kwargs must be inserted into the hash table
        """
        self.capacity = 10
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for (k, v) in kwargs.items():
            self.__setitem__(k, v)

    def __contains__(self, key):
        """True if this hash table has key `key`, else False"""
        if self.table[self.hashf(key)]:
            return True

        return False

    def __getitem__(self, key):
        """
        Implementing this lets you do `table['key']`.
        This should raise a KeyError if the key is not in the table.
        """
        for pair in self.table[self.hashf(key)]:
            if pair[0] == key:
                return pair[1]
                
        raise KeyError

    def __len__(self):
        """Returns the number of (key, value) pairs in the hash table"""
        count = 0
        
        for pairs in self.table:
            count += len(pairs) 
        
        return count 
    
    def __setitem__(self, key, value):
        """Implements `table[x] = y`"""
        self.table[self.hashf(key)].append((key, value))

        if len(self.table[self.hashf(key)]) == 1:
            self.size += 1

    def hashf(self, key):
        """Apply the hash function on the key to get its index in the table."""
        return hash(key) % self.capacity

    def resize_table(self):
        """When capcity of table runs out, copy old table into a new table with 
        double capacity; update hash values using size of new table"""

        self.capacity *= 2
        new_table = [[] for _ in range(self.capacity)]
        for slot in self.table:
            if slot:
                for k, v in slot:
                    new_table[hash(k)].append(v)

        self.table = new_table

# Replace Hashtable with `dict` to see the tests pass :)
TEST_TABLE = Hashtable

class TestHashtable(unittest.TestCase):
    """
    Tests the functionality of the Hashtable class.
    """

    def test_init(self):
        """Tests initialization"""
        table = TEST_TABLE(a=25)
        self.assertEqual(len(table), 1)

    def test_put(self):
        """Tests inserting a single element"""
        table = TEST_TABLE()
        table['a'] = 25
        self.assertIn('a', table)

    def test_get(self):
        """Tests inserting a single element"""
        table = TEST_TABLE()
        table['a'] = 25
        self.assertEqual(table['a'], 25)

    def test_get_missing(self):
        """Tests if the hash table raises KeyError if a key is missing"""
        table = TEST_TABLE()
        with self.assertRaises(KeyError):
            _ = table['a']

    def test_put_many(self):
        """Inserts many elements into the hash table"""
        table = TEST_TABLE()
        randoms = dict(zip(
            (randrange(10) for _ in range(10)),
            (str(x) for x in range(10))
        ))
        # Put all the elements in
        for (k, v) in randoms.items():
            table[k] = v

        # Make sure they're all there
        self.assertEqual(len(table), len(randoms))
        for (k, _) in randoms.items():
            self.assertIn(k, table)

        # Make sure they have the right values
        for (k, v) in randoms.items():
            self.assertEqual(table[k], v)

if __name__ == '__main__':
    unittest.main()
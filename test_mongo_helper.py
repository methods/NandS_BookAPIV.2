# pylint: disable=missing-docstring
import pytest
from unittest.mock import patch, MagicMock 
from mongo_helper import insertBookToMongo


@patch('mongo_helper.books_collection')
def test_insertBookToMongo(mock_books_collection):
    #Setup the mock 
    mock_result = MagicMock()
    mock_result.inserted_id = '12345'
    mock_books_collection.insert_one.return_value = mock_result

    # Test data
    new_book = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "synopsis": "A story about the American Dream"
    }

    # Call the function 
    result = insertBookToMongo(new_book)

    # Assertions
    mock_books_collection.insert_one.assert_called_once_with(new_book)
    assert result == '12345'
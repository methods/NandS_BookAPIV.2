#!/bin/bash

mongoimport --db BOOKS_API --collection books --file test_data/sample_books.json --jsonArray
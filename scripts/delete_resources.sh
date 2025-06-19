#!/bin/bash

mongosh BOOKS_API --eval "db.books.deleteMany({})"
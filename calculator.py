#!/usr/bin/env python3
"""
Project Name: WSGI-calculator
File Name: calculator.py
Author: Travis Brackney
Class: Python 230 - Self paced online
Date Created 9/22/2019
Python Version: 3.7.2
"""

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # done: Fill sum with the correct value, based on the
    # args provided.

    total = sum(map(int, args))

    return str(total)

# TODO: Add functions for handling more arithmetic operations.


def subtract(*args):
    """ Returns a STRING with the result of subtraction of the arguments"""
    total = 0
    if args:
        nums = [int(n) for n in args]
        total = nums[0] - sum(nums[1:])

    return str(total)


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    total = 0
    if args:
        nums = [int(n) for n in args]
        total = nums[0]
        for n in nums[1:]:
            total *= n

    return str(total)


def divide(*args):
    """ returns a STRING with the dividend of the arguments """
    total = 0
    if args:
        nums = [int(n) for n in args]
        total = nums[0]
        for n in nums[1:]:
            total /= n

    return str(total)


def main_page(*args):
    body = """
    <h1>WSGI Calculator</h1>
    <p>This calculator can add, subtract, multiply, or divide integers in the URL</p>
    <p>Format /operation/int1/int2
    <h2>Examples</h2>
    <p> /multiply/7/3 returns 7 times 3 = 21 </p>
    <p> /add/25/21 returns 25 plus 21 = 46 </p>
    """

    return body


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # done: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.

    funcs = {
        '': main_page,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }

    path = path.strip("/").split("/")
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        print(traceback.format_exc())
        raise NameError
    return func, args


def application(environ, start_response):
    # done: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # done (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ValueError:
        status = "404 Not Found"
        body = "<h1>Invalid Operand in argument list</h1>"
    except ZeroDivisionError:
        status = "404 Not Found"
        body = "<h1>Cannot divide by Zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    # Done: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

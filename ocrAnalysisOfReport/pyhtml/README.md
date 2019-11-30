# python-html
A simple framework for constructing an HTML document

## Imports
```
from html import *
```

## Basic Structure

Each HTML tag is given its own class of the same name but with the first letter capitalized. There are two types of parent classes: `Tag` for HTML tags that must be closed and `STag` for singleton HTML tags that shouldn't be closed.

HTML tags of type `Tag` have `name`, `content`, and `attrs` member variables. `name` stores the name of the tag: 'div' for a `<div></div>` tag, 'script' for a `<script></script>` tag, and so on. `content` is a list that can store strings, `Tag`, and `STag`. `attrs` is a dictionary of HTML attributes.

HTML singleton tags of type `STag` don't have a `content` member variable.

## Setting up the HTML Document

This creates an html `Tag`, then inserts a head and a body `Tag` into it's `content`.

```
document = Document()
html = Html()
head = html << Head()
body = html << Body()
```

The document can then be printed.

```
print document
```

## Instantiating Tags

A `Tag` can be instantiated with any number of content elements and attributes.

```
mydiv = Div("Hello", "World!", Class="world", Id="hello")
mydiv2 = Div(Class="world", Id="mydiv2")
mydiv3 = Div("Hi There!")
```

For attributes that don't have a value, just set it to True like this:

```
Script(Async=True, Defer=True)
```

An `STag` can't have content elements.

## Insertion

The `Tag` class supports an insertion operator `<<` which does a few things. First, you can use it to insert content to a tag.

```
body << "Hello World!" # insert a string
body << Img(Src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/260px-The_Earth_seen_from_Apollo_17.jpg") # insert an img tag
```

You can also use the insertion operator to insert arrays of elements.

```
body << ["Hello World!", Div(Id="mydiv")]
```

Or use it to add and modify attributes with a dictionary.

```
mydiv = body << Div()
mydiv << {"id": "mydiv2"}
```

`STag` elements also have an assertion operator, but it only allows you to insert attributes. Everything else is ignored.

## Selectors

`Tag` and `STag` also support selection much like in jquery. However, the selection operation always returns a `list`.

```
mydiv = body("#mydiv")
mydiv2 = body("div#mydiv2")
alldivs = body("div")
```

## Parsing

This library also includes an `HTMLParser` implementation that converts directly to an html syntax tree.

```
parser = Parser()
with open(filename, 'r') as fptr:
  parser.feed(fptr.read())
print parser.syntax
```
## Custom Tags

If you find this library lacking a tag, you can instantiate custom tags like so:

```
print Tag("my-tag", ["This is the content", " inside the tag!"], {"id": "mycooltag"})
print STag("my-singleton", {"id": "mycoolsingleton"})
```

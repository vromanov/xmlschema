# -*- coding: utf-8 -*-
#
# Copyright (c), 2016, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
"""
This module contains the exception classes of the 'xmlschema' package.
"""
from .core import PY3, etree_tostring, URLError


class XMLSchemaException(Exception):
    pass


class XMLSchemaOSError(XMLSchemaException, OSError):
    pass


class XMLSchemaLookupError(XMLSchemaException, LookupError):
    pass


class XMLSchemaAttributeError(XMLSchemaException, AttributeError):
    pass


class XMLSchemaTypeError(XMLSchemaException, TypeError):
    pass


class XMLSchemaValueError(XMLSchemaException, ValueError):
    pass


class XMLSchemaKeyError(XMLSchemaException, KeyError):
    pass


class XMLSchemaURLError(XMLSchemaException, URLError):
    pass


class XMLSchemaParseError(XMLSchemaException, ValueError):
    """Raised when an error is found when parsing an XML Schema."""

    def __init__(self, message, elem=None):
        self.message = message or u''
        self.elem = elem

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u''.join([
            self.message,
            u"\n\n  %s\n" % etree_tostring(
                self.elem, max_lines=20
            ) if self.elem is not None else '',
        ])

    if PY3:
        __str__ = __unicode__
    pass


class XMLSchemaRegexError(XMLSchemaParseError):
    """Raised when an error is found when parsing an XML Schema."""
    pass


class XMLSchemaComponentError(XMLSchemaException, ValueError):
    """Raised when an error is found in a XML Schema component."""
    def __init__(self, obj, name, ref=None, message=None):
        """
        :param obj: The object that generate the exception.
        :param name: The attribute/key name.
        :param ref: An object or type that refer to the name.
        :param message: Error text message.
        """
        self.message = message
        self.obj = obj
        if not isinstance(ref, (int, str, type)):
            self.description = 'attribute %r' % name
        elif isinstance(ref, int):
            self.description = 'item %d of %r' % (ref, name)
        elif isinstance(ref, str):
            self.description = '%r: %s' % (name, ref)
        elif issubclass(ref, dict):
                self.description = 'value of dictionary %r' % name
        elif issubclass(ref, list):
            self.description = 'item of list %r' % name
        else:
            self.description = 'instance %r of type %r' % (name, ref)

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u'%r: %s: %s' % (self.obj, self.description, self.message)

    if PY3:
        __str__ = __unicode__


class XMLSchemaBaseValidatorError(XMLSchemaException, ValueError):
    """Base class for errors generated by XML Schema validators."""

    def __init__(self, validator, message):
        self.validator = validator
        self.message = message or u''
        self.reason = None
        self.schema_elem = None
        self.elem = None

    def __str__(self):
        return unicode(self).encode("utf-8")

    def __unicode__(self):
        return u''.join([
            self.message,
            u'\n\nReason: %s\n' % self.reason if self.reason is not None else '\n',
            u"\nSchema:\n\n  %s\n" % etree_tostring(
                self.schema_elem, max_lines=20
            ) if self.schema_elem is not None else '\n',
            u"\nInstance:\n\n  %s\n" % etree_tostring(
                self.elem, max_lines=20
            ) if self.elem is not None else '\n'
        ])

    if PY3:
        __str__ = __unicode__


class XMLSchemaDecodeError(XMLSchemaBaseValidatorError):
    """Raised when an XML data string is not decodable to a Python object."""

    def __init__(self, validator, obj, decoder, reason=None, schema_elem=None, elem=None):
        self.message = u"cannot decode %r using the type %r of validator %r." % (obj, decoder, validator)
        self.validator = validator
        self.obj = obj
        self.decoder = decoder
        self.reason = reason
        self.elem = elem
        self.schema_elem = schema_elem


class XMLSchemaEncodeError(XMLSchemaBaseValidatorError):
    """Raised when an object is not encodable to an XML data string."""

    def __init__(self, validator, obj, encoder, reason=None, elem=None, schema_elem=None):
        self.message = u"cannot encode %r using the type %r of validator %r." % (obj, encoder, validator)
        self.validator = validator
        self.obj = obj
        self.encoder = encoder
        self.reason = reason
        self.elem = elem
        self.schema = schema_elem


class XMLSchemaValidationError(XMLSchemaBaseValidatorError):
    """Raised when the XML data string is not validated with the XSD schema."""

    def __init__(self, validator, value, reason=None, elem=None, schema_elem=None):
        self.message = u"failed validating %r with %r." % (value, validator)
        self.validator = validator
        self.value = value
        self.reason = reason
        self.elem = elem
        self.schema_elem = schema_elem

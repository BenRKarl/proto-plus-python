# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from unittest import mock
import warnings

import proto
from proto.marshal.rules.enums import EnumRule


def test_to_proto():
    class Foo(proto.Enum):
        FOO_UNSPECIFIED = 0
        BAR = 1
        BAZ = 2

    enum_rule = EnumRule(Foo)
    foo_a = enum_rule.to_proto(Foo.BAR)
    foo_b = enum_rule.to_proto(1)
    foo_c = enum_rule.to_proto("BAR")
    # We want to distinguish literal `1` from `Foo.BAR` here
    # (they are equivalent but not identical).
    assert foo_a is foo_b is foo_c is 1  # noqa: F632


def test_to_python():
    class Foo(proto.Enum):
        FOO_UNSPECIFIED = 0
        BAR = 1
        BAZ = 2

    enum_rule = EnumRule(Foo)
    foo_a = enum_rule.to_python(1)
    foo_b = enum_rule.to_python(Foo.BAR)
    assert foo_a is foo_b is Foo.BAR


def test_to_python_unknown_value():
    class Foo(proto.Enum):
        FOO_UNSPECIFIED = 0
        BAR = 1
        BAZ = 2

    enum_rule = EnumRule(Foo)
    with mock.patch.object(warnings, "warn") as warn:
        assert enum_rule.to_python(4) == 4
        warn.assert_called_once_with("Unrecognized Foo enum value: 4")

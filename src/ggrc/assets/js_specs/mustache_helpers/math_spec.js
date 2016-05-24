/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: Aliaksandr_Novik3@epam.com
 Maintained By: Aliaksandr_Novik3@epam.com
 */

describe('can.mustache.helper.math', function () {
  'use strict';

  var helper;

  beforeAll(function () {
    helper = can.Mustache._helpers.math.fn;
  });

  it('return result of add', function () {
    var result;
    result = helper(10, '+', 15);
    expect(result).toEqual(25);
  });

  it('return result of multiply', function () {
    var result;
    result = helper(3, '*', 20);
    expect(result).toEqual(60);
  });

  it('return result of sub', function () {
    var result;
    result = helper(152, '-', 62);
    expect(result).toEqual(90);
  });

  it('return result of divide', function () {
    var result;
    result = helper(150, '/', 50);
    expect(result).toEqual(3);
  });
});
